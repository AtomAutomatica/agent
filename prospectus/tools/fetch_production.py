#!/usr/bin/env python3
"""Fetch official cumulative production for the mapped wells around Robinson #1.

Chain (all public RRC systems):
1. EWA wellbore query (webapps2.rrc.texas.gov/EWA/wellboreQueryAction.do):
   API -> current (on-schedule) lease: district, lease/gas-well no, lease name,
   well no, field, operator.
2. PDQ specific-lease query (webapps.rrc.texas.gov/PDQ): monthly lease
   production Jan 1993 - present; summed here for cumulative totals.
   Oil leases report oil BBL + casinghead MCF; gas wells report gas MCF +
   condensate BBL. PDQ coverage begins January 1993.

Writes data/rrc/production.json. Every number is parsed from a fetched RRC
report; nothing is estimated."""
import json
import os
import re
import subprocess
import time

import lxml.html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "rrc", "production.json")
SP = "/tmp/claude-0/-home-user-agent/c9d786d4-fdaa-571d-991a-243da74becde/scratchpad/pdqwork"
os.makedirs(SP, exist_ok=True)
CA = "/root/.ccr/ca-bundle.crt"
RANGE = ("01", "1993", "07", "2026")

WELLS = [
    ("01025", "oil"), ("31143", "oil"), ("01026", "oil"), ("31114", "oil"),
    ("31148", "oil"), ("30086", "oil"), ("31162", "oil"), ("31139", "oil"),
    ("31157", "oil"), ("31152", "oil"), ("31128", "oil"), ("31120", "oil"),
    ("01024", "oil"), ("31117", "oil"), ("31124", "oil"),
    ("31179", "gas"), ("31177", "gas"), ("30061", "gas"), ("31130", "gas"),
    ("01022", "gas"), ("30560", "gas"), ("31169", "gas"), ("31175", "gas"),
    ("30615", "gas"), ("30085", "gas"),
]


def curl(args, out):
    subprocess.run(["curl", "-s", "--cacert", CA, "-o", out] + args, check=True)
    return open(out, encoding="utf-8", errors="replace").read()


def wellbore_lookup(api5):
    """Return the on-schedule lease rows for an API."""
    url = ("https://webapps2.rrc.texas.gov/EWA/wellboreQueryAction.do"
           f"?methodToCall=search&searchArgs.apiNoPrefixArg=467"
           f"&searchArgs.apiNoSuffixArg={api5}")
    h = curl([url], f"{SP}/wb_{api5}.html")
    doc = lxml.html.fromstring(h)
    rows = []
    for tr in doc.xpath("//tr"):
        cells = []
        for c in tr.xpath("./td"):
            txt = re.sub(r"\b(Links|Images|GIS Viewer|Completion)\b", " ",
                         c.text_content())
            txt = re.sub(r"\s+", " ", txt).strip()
            if txt:
                cells.append(txt)
        if not cells or not re.match(r"467\d{5}", cells[0] or ""):
            continue
        rows.append(cells)
    out = []
    for c in rows:
        # API, District, LeaseNo, LeaseName, WellNo, Field, Operator, County, OnSched[, Depth]
        if len(c) >= 9:
            out.append({
                "api": c[0], "district": c[1], "lease_no": c[2],
                "lease_name": c[3], "well_no": c[4], "field": c[5],
                "operator": c[6], "county": c[7], "on_sched": c[8],
            })
    return [r for r in out if r["on_sched"] == "Y"] or out[:1]


def pdq_lease(district, lease_no, well_type, tag):
    """Fetch PDQ monthly rows for a lease; return summed totals + metadata."""
    jar = f"{SP}/jar_{tag}"
    if os.path.exists(jar):
        os.remove(jar)
    curl(["-c", jar, "https://webapps.rrc.texas.gov/PDQ/quickLeaseReportBuilderAction.do"],
         f"{SP}/q_{tag}.html")
    sm, sy, em, ey = RANGE
    data = (f"wellType={'Oil' if well_type == 'oil' else 'Gas'}&leaseNumber={lease_no}"
            f"&district={district}&startMonth={sm}&startYear={sy}"
            f"&endMonth={em}&endYear={ey}&submit=Submit")
    curl(["-b", jar, "-c", jar, "-X", "POST",
          "-H", "Referer: https://webapps.rrc.texas.gov/PDQ/quickLeaseReportBuilderAction.do",
          "--data", data,
          "https://webapps.rrc.texas.gov/PDQ/quickLeaseSubmitAction.do"],
         f"{SP}/r_{tag}.html")
    h = curl(["-b", jar, "-c", jar,
              "https://webapps.rrc.texas.gov/PDQ/changePageViewAction.do?pagesize=500"],
             f"{SP}/all_{tag}.html")
    doc = lxml.html.fromstring(h)
    txt = doc.text_content()
    if "is invalid" in txt or "No results" in txt or "no data" in txt.lower():
        return None
    m = re.search(r"Lease Name:\s*(.+?),\s*Lease No:\s*(\S+)", txt)
    lease_name = m.group(1).strip() if m else None
    months, prod1, prod2 = [], 0, 0
    ops, fields = set(), set()
    for tr in doc.xpath("//tr"):
        cells = [re.sub(r"\s+", " ", c.text_content()).strip() for c in tr.xpath("./td")]
        if not cells or not re.match(r"^[A-Z][a-z]{2} \d{4}$", cells[0]):
            continue
        nums = [c for c in cells[1:] if re.match(r"^-?[\d,]+$", c)]
        if len(nums) < 4:
            continue
        months.append(cells[0])
        # columns: [prod1, disp1, prod2, disp2] (oil/casinghead or gas/condensate)
        prod1 += int(nums[0].replace(",", ""))
        prod2 += int(nums[2].replace(",", ""))
        for c in cells:
            if re.match(r"^[A-Z][A-Z .,&'\-]+, (INC|LLC|LP|LTD|CO)", c):
                ops.add(c)
    if not months:
        return None
    return {
        "lease_name": lease_name,
        "months": len(months),
        "first": months[0], "last": months[-1],
        "prod1": prod1, "prod2": prod2,
        "operators_seen": sorted(ops),
    }


def main():
    resolved = {}
    for api5, wtype in WELLS:
        try:
            rows = wellbore_lookup(api5)
        except Exception as e:
            print(f"{api5}: wellbore lookup failed: {e}")
            continue
        if not rows:
            print(f"{api5}: no wellbore record")
            continue
        r = rows[0]
        key = (wtype, r["district"], r["lease_no"])
        entry = resolved.setdefault(key, {**r, "wtype": wtype, "api5s": [], "well_nos": []})
        entry["api5s"].append(api5)
        entry["well_nos"].append(r["well_no"])
        print(f"{api5} -> D{r['district']} lease {r['lease_no']} {r['lease_name']} "
              f"({r['operator']}; {r['field']})")
        time.sleep(0.4)

    oil, gas = [], []
    for (wtype, district, lease_no), e in resolved.items():
        tag = f"{wtype}_{district}_{lease_no}"
        try:
            p = pdq_lease(district, lease_no, wtype, tag)
        except Exception as ex:
            print(f"lease {lease_no}: PDQ failed: {ex}")
            p = None
        rec = {
            "lease_name": (p and p["lease_name"]) or e["lease_name"],
            "lease_no": lease_no, "district": district,
            "operator": e["operator"], "field": e["field"],
            "api5s": e["api5s"], "well_nos": e["well_nos"],
            "source": f"RRC PDQ specific lease query, district {district}, "
                      f"{'oil lease' if wtype == 'oil' else 'gas well ID'} {lease_no}",
        }
        if p:
            rec["period"] = f"{p['first']} - {p['last']}"
            rec["months_reported"] = p["months"]
            if wtype == "oil":
                rec["cum_oil_bbl"] = p["prod1"]
                rec["cum_gas_mcf"] = p["prod2"]  # casinghead gas
                rec["gas_is_casinghead"] = True
            else:
                rec["cum_gas_mcf"] = p["prod1"]
                rec["cum_oil_bbl"] = p["prod2"]  # condensate
                rec["oil_is_condensate"] = True
        else:
            rec["no_pdq_data"] = True
        (oil if wtype == "oil" else gas).append(rec)
        print(f"lease {lease_no} {rec['lease_name']}: "
              f"{rec.get('cum_oil_bbl', '-')} bbl / {rec.get('cum_gas_mcf', '-')} mcf "
              f"({rec.get('period', 'NO PDQ DATA')})")
        time.sleep(0.4)

    oil.sort(key=lambda r: -(r.get("cum_oil_bbl") or 0))
    gas.sort(key=lambda r: -(r.get("cum_gas_mcf") or 0))
    out = {
        "retrieved": "July 17, 2026",
        "range_queried": "Jan 1993 - Jul 2026",
        "oil": oil,
        "gas": gas,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"wrote {OUT}: {len(oil)} oil leases, {len(gas)} gas wells")


if __name__ == "__main__":
    main()
