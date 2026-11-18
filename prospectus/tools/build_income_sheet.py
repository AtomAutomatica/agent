#!/usr/bin/env python3
"""Generate the Ferox Oil 'Estimated Monthly Income' one-pager (build/income.html).

Terms: $98,000 per 1% working interest unit (.75% NRI), per the user.
Income formula (the company's own): rate x 30 days x price x .75 NRI / 100.
Scenario prices bracket the market as of Nov 2026 (WTI spot ~$90.40 on
Nov 9, 2026 per EIA; Henry Hub front-month ~$2.90 per CME)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "income.html")

A = "../assets"
LOGO = f"{A}/brand/ferox-logo.png"
UNIT_PRICE = 98_000
NRI = 0.0075  # .75% of revenue per 1% unit

OIL_PRICES = [75, 90, 100]
OIL_MARKET = 90
OIL_RATES = [250, 500, 750]
GAS_PRICES = [3.00, 3.50, 7.00]
GAS_MARKET = 3.00
GAS_RATES = [1000, 2000]

DISCLAIMER = (
    "Estimated income figures are illustrative calculations at the stated hypothetical production "
    "rates and prices; they are not a forecast and actual results may differ materially. Oil and gas "
    "investments involve a high degree of risk, including loss of the entire investment. This document "
    "constitutes part of an investor kit and should only be read in conjunction with the subscription "
    "agreement and memorandum. It is not to be construed as an offer to sell or as a solicitation of "
    "an offer to buy any security in any jurisdiction. No person is authorized to give any information "
    "or make any representation other than those contained or incorporated by reference in the "
    "subscription agreement and memorandum, and any such information or representation must not be "
    "relied upon as having been authorized by Ferox Oil, LLC."
)


def money(x, cents=True):
    return f"${x:,.2f}" if cents else f"${x:,.0f}"


def oil_cell(rate, price):
    income = rate * 30 * price * NRI
    payout = UNIT_PRICE / income
    return (f'<td class="num"><div class="inc">{money(income)}</div>'
            f'<div class="sub">payout &asymp; {payout:.1f} mo</div></td>')


def gas_cell(rate, price):
    income = rate * 30 * price * NRI
    return f'<td class="num"><div class="inc">{money(income)}</div></td>'


def price_head(p, market, unit):
    tag = '<span class="mkt">&asymp; market</span>' if p == market else ""
    val = f"${p:,.2f}" if isinstance(p, float) else f"${p:,.0f}"
    return f"<th>{val} {unit} {tag}</th>"


oil_rows = "".join(
    f'<tr><td class="rate">{r:,} BOPD</td>'
    + "".join(oil_cell(r, p) for p in OIL_PRICES) + "</tr>"
    for r in OIL_RATES
)
gas_rows = "".join(
    f'<tr><td class="rate">{r:,} MCFPD</td>'
    + "".join(gas_cell(r, p) for p in GAS_PRICES) + "</tr>"
    for r in GAS_RATES
)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Ferox Oil — Estimated Monthly Income</title>
<link rel="stylesheet" href="../assets/fonts/fonts.css">
<link rel="stylesheet" href="style.css">
<style>
.chips {{ position:absolute; top:2.10in; left:0.6in; right:0.6in; display:flex; gap:0.22in; }}
.chip {{ flex:1; border:1px solid var(--line); border-left:3px solid var(--red);
        padding:0.10in 0.14in; }}
.chip .v {{ font-family:'Barlow Condensed'; font-weight:600; font-size:17pt; color:var(--ink); }}
.chip .l {{ font-size:7pt; font-weight:600; letter-spacing:0.18em; text-transform:uppercase;
           color:var(--gray); margin-top:2px; }}
.sect {{ position:absolute; left:0.6in; right:0.6in; }}
.sect h2 {{ font-weight:700; font-size:8.5pt; letter-spacing:0.26em; text-transform:uppercase;
           color:var(--red); margin-bottom:0.07in; }}
.sect .formula {{ font-size:7.6pt; color:var(--gray); margin-top:0.05in; }}
table.inc {{ width:100%; border-collapse:collapse; }}
.inc th {{ background:var(--red); color:#fff; font-weight:600; font-size:7.5pt;
          letter-spacing:0.08em; text-transform:uppercase; padding:5px 8px; text-align:right;
          border:1px solid #a30000; }}
.inc th:first-child {{ text-align:left; }}
.inc th .mkt {{ display:inline-block; background:#fff; color:var(--red); font-size:5.8pt;
               padding:1px 5px; margin-left:5px; border-radius:2px; letter-spacing:0.08em; }}
.inc td {{ border:1px solid var(--line); padding:6px 8px; }}
.inc td.rate {{ font-weight:700; font-size:9.5pt; }}
.inc td.num {{ text-align:right; }}
.inc .inc {{ font-family:'Barlow Condensed'; font-weight:600; font-size:13.5pt; color:var(--ink); }}
.inc .sub {{ font-size:6.6pt; color:var(--gray); margin-top:1px; }}
.inc tr:nth-child(even) td {{ background:#fafafa; }}
.mktline {{ position:absolute; left:0.6in; right:0.6in; top:7.95in; font-size:7.4pt;
           color:var(--gray); line-height:1.5; }}
.onepager-disclaimer {{ position:absolute; bottom:0.80in; left:0.85in; right:0.85in;
  font-size:6.8pt; font-style:italic; line-height:1.5; color:var(--gray); text-align:justify; }}
</style></head><body>
<section class="page">
  <div class="hdr"><span class="well">FEROX OIL, LLC</span>
  <img class="logo" src="{LOGO}" alt="Ferox Oil"></div>
  <div class="hdr-rule"></div>
  <div class="titleblock">
    <div class="krow"><span class="kicker">Financial</span></div>
    <h1 class="title">Estimated Monthly Income</h1>
    <div class="title-bar"></div>
    <div class="subtitle">Based on 1% Working Interest &middot; .75% Net Revenue Interest</div>
  </div>

  <div class="chips">
    <div class="chip"><div class="v">$98,000.00</div>
      <div class="l">Per 1% Unit &middot; Drilling, Testing &amp; Completion</div></div>
    <div class="chip"><div class="v">1.0%</div>
      <div class="l">Working Interest per Unit</div></div>
    <div class="chip"><div class="v">.75%</div>
      <div class="l">Net Revenue Interest per Unit</div></div>
  </div>

  <div class="sect" style="top:3.05in;">
    <h2>Oil Production &mdash; Estimated Income per Month</h2>
    <table class="inc">
      <tr><th>Oil Rate</th>{"".join(price_head(p, OIL_MARKET, "Oil") for p in OIL_PRICES)}</tr>
      {oil_rows}
    </table>
    <div class="formula">Formula: BOPD &times; 30 days &times; oil price &times; .75 NRI &divide; 100.
    &ldquo;Payout&rdquo; = months of estimated income to recover the $98,000.00 unit price (oil income alone).</div>
  </div>

  <div class="sect" style="top:5.62in;">
    <h2>Natural Gas Production &mdash; Estimated Income per Month</h2>
    <table class="inc">
      <tr><th>Gas Rate</th>{"".join(price_head(p, GAS_MARKET, "Gas") for p in GAS_PRICES)}</tr>
      {gas_rows}
    </table>
    <div class="formula">Formula: MCFPD &times; 30 days &times; gas price &times; .75 NRI &divide; 100.</div>
  </div>

  <div class="mktline"><b>Market reference (November 2026):</b> WTI crude spot &asymp; $90.40/BBL
  (EIA, Nov 9, 2026; recent settlements as high as &asymp; $96); Henry Hub natural gas front-month
  &asymp; $2.90/MMBtu (CME). Scenario prices above are illustrative and bracket the current market.</div>

  <div class="onepager-disclaimer">{DISCLAIMER}</div>

  <div class="ftr-rule"></div>
  <div class="ftr"><span>www.feroxoil.com</span>
  <span class="co">FEROX OIL, LLC</span>
  <span>P: (214) 257 - 0319</span></div>
</section>
</body></html>"""

with open(OUT, "w") as fh:
    fh.write(html)
print("wrote", OUT)
