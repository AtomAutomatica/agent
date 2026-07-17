#!/usr/bin/env python3
"""Generate build/index.html — the Ferox Oil 'Robinson #1' prospectus.

Every exhibit is the untouched scan extracted from the original book
(assets/extracted/robinson). Official/third-party documents inside those scans
(RRC Form W-1, permit plat, surveyor and geologist documents) are reproduced
exactly as they appear in the source; only the surrounding template chrome is
rebranded."""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "index.html")

A = "../assets"
EX = f"{A}/optimized"
LOGO = f"{A}/brand/ferox-logo.png"
PHOTO = f"{A}/optimized/industrial-photo.jpg"

WEBSITE = "www.feroxoil.com"
PHONE = "P: (214) 257 - 0319"

TOC = [
    ("03", "Summary"),
    ("04", "Site Access Map"),
    ("05", "Producing Zones"),
    ("06", "Structure"),
    ("12", "Formations"),
    ("18", "Permit"),
    ("23", "Proven Production"),
    ("25", "Financial Projection"),
    ("26", "Contact Information"),
]

# (page, kicker, title, subtitle, exhibit file, bare)
EXHIBIT_PAGES = [
    (3,  "Overview",   "Summary", "Consulting Geologist &amp; Drilling Superintendent Report", "page02_x3.png", False),
    (4,  "Location",   "Site Access Map", "C.J. Robinson Well #1 &middot; Van Zandt County, Texas", "page03_x10.png", False),
    (5,  "Geology",    "Producing Zones", "Principal Oil-Producing Stratigraphic Units &middot; Gulf Coast &amp; East Texas Basins", "page04_x15.png", False),
    (6,  "Geology",    "Structure", "East Texas Salt Structure Province", "page05_x19.png", False),
    (7,  "Geology",    "Quitman Field", "Neighboring Field, Wood County &middot; Complex Fault System Forming Dozens of Oil Traps", "page06_x24.png", False),
    (8,  "Geology",    "East Texas Basin", "Isometric Block Diagram &middot; Louann Salt Configuration", "page07_x30.png", False),
    (9,  "Geology",    "Structural Elements", "Major Structural Elements of the East Texas Basin", "page08_x34.png", False),
    (10, "Geology",    "Electrical Curves", "Electrical Curves &amp; Lithology", "page09_x40.png", False),
    (11, "Geology",    "Stratigraphic Cross Section", "Kaufman &amp; Van Zandt Counties", "page10_x46.png", False),
    (12, "Formations", "Austin Chalk 3,800&prime;", None, "page11_x50.png", False),
    (13, "Formations", "Paluxy 7,700&prime;", None, "page12_x56.png", False),
    (14, "Formations", "Smackover 15,000&prime;", None, "page13_x60.png", False),
    (15, "Formations", "Myrtle Springs Field", "Van Zandt County, Texas", "page14_x64.png", False),
    (16, "Formations", "Travis Peak Completion", "Fruitvale Field, Van Zandt County, Texas", "page15_x69.png", False),
    (17, "Formations", "Myrtle Springs Field &mdash; Type Section", "Van Zandt County, Texas", "page16_x74.png", False),
    (18, "Permit",     "Permit", "Railroad Commission of Texas &middot; Form W-1 &middot; Approved", "page17_x81.png", False),
    (19, "Permit",     "RRC Map &mdash; Well Site", "Railroad Commission of Texas GIS Viewer", "page18_x92.png", False),
    (20, "Permit",     "Permit Plat", "Ephraim Vansickle Survey, Abstract 885, Van Zandt County, Texas", "page19_x97.png", False),
    (21, "Permit",     "Tobin Ownership Map", "C.J. Robinson &middot; 81 Acres", "page20_x101.png", False),
    (22, "Permit",     "RRC Permit Records", "Railroad Commission of Texas Online System", "page21_x105.png", False),
    # 23 = text page, built separately
    (24, "Reference",  "Geology of Texas", "Bureau of Economic Geology &middot; The University of Texas at Austin", "page23_x114.png", False),
    (25, "Financial",  "Financial Projection", "Potential Monthly Return on 1% &middot; $65 / $75 / $85 Oil Price Scenarios", "page24_x119.png", False),
]

STACKED_PARAGRAPHS = [
    "The East Texas salt structure province covers over eleven (11) counties, "
    "which includes Van Zandt County. There are approximately seventeen (17) "
    "oil and gas bearing formations in Van Zandt County, which include: "
    "Nacatoch, Taylor, Pecan Gap, Austin, Eagle Ford, Woodbine, Buda, Grayson, "
    "Georgetown, Fredericksburg, Paluxy, Glen Rose, Rodessa, Pettet, Travis "
    "Peak, Cotton Valley and Smackover.",

    "Any of these formations could be a potential trap for accumulating "
    "migrating oil and gas. As illustrated in the nearby Quitman Field, where "
    "close drilling occurred, main and secondary faults can be accurately "
    "defined. In this proposed Robinson #1 well, the lack of well control "
    "(number of wells) prevents such close control or mapping of these faults "
    "and structures.",

    "There are four (4) fields surrounding the Robinson #1: the Myrtle Springs "
    "Field, Edgewood Field, Fruitvale East Field and the Fruitvale Field. The "
    "Robinson #1 is considered an extension of the Fruitvale Field. Faults "
    "that are created by the upward migration of the Louann salt bed have cut "
    "through some, if not all, of the formations above this salt and have "
    "created these four (4) surrounding fields as oil and gas became trapped "
    "and accumulated. All of the salt domes in the East Texas salt structure "
    "province have created dozens of fields throughout the province as these "
    "domes push upward in their migration toward the surface. The probability "
    "of undiscovered trapped oil and gas within any of these seventeen (17) "
    "plus formations is high due to this &ldquo;under drilling&rdquo; of the "
    "Robinson lease.",

    "This area is termed a &ldquo;stacked&rdquo; field with potential "
    "production in many, if not all, of the shallower formations. No one (1) "
    "formation makes up these four (4) fields; however, the Smackover "
    "formation is the formation that is sustained, and high production is the "
    "common factor throughout.",
]

DISCLAIMER = (
    "This document constitutes part of an investor kit and should only be read "
    "in conjunction with the subscription agreement and memorandum. This "
    "document is for your private information, and we are not soliciting any "
    "action based upon it. This document is not to be construed as an offer to "
    "sell or as a solicitation of an offer to buy any security in any "
    "jurisdiction. Please review with care the subscription agreement enclosed "
    "within this document. No person is authorized to give any information or "
    "make any representation other than those contained or incorporated by "
    "reference in the subscription agreement and memorandum. If given or made, "
    "any such information or representation must not be relied upon as having "
    "been authorized by Ferox Oil, LLC."
)


def chrome(folio=None):
    parts = [
        '<div class="hdr"><span class="well">ROBINSON #1</span>'
        f'<img class="logo" src="{LOGO}" alt="Ferox Oil"></div>',
        '<div class="hdr-rule"></div>',
    ]
    return "".join(parts)


def footer():
    return (
        '<div class="ftr-rule"></div>'
        f'<div class="ftr"><span>{WEBSITE}</span>'
        '<span class="co">FEROX OIL, LLC</span>'
        f'<span>{PHONE}</span></div>'
    )


def titleblock(folio, kicker, title, subtitle):
    sub = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""
    return (
        '<div class="titleblock">'
        f'<div class="krow"><span class="kicker">{kicker}</span>'
        f'<span class="folio">{folio:02d}</span></div>'
        f'<h1 class="title">{title}</h1>'
        '<div class="title-bar"></div>'
        f'{sub}</div>'
    )


def cover_page():
    return (
        '<section class="page cover">'
        f'<img class="cover-logo" src="{LOGO}" alt="Ferox Oil">'
        '<div class="cover-well">Robinson #1</div>'
        '<div class="cover-county">Van Zandt County, Texas</div>'
        f'<div class="cover-photo"><img src="{PHOTO}" alt=""></div>'
        f'{footer()}'
        '</section>'
    )


def toc_page():
    rows = "".join(
        f'<div class="toc-row"><span class="toc-num">{n}</span>'
        f'<span class="toc-label">{label}</span></div>'
        for n, label in TOC
    )
    return (
        '<section class="page">'
        f'{chrome()}'
        f'{titleblock(2, "Contents", "Table of Contents", None)}'
        '<div class="tocwrap">'
        f'<div class="toc-photo"><img src="{PHOTO}" alt=""></div>'
        f'<div class="toc-list">{rows}</div>'
        '</div>'
        f'{footer()}'
        '</section>'
    )


def exhibit_page(num, kicker, title, subtitle, img, bare):
    cls = "exhibit bare" if bare else "exhibit"
    jpg = img.replace(".png", ".jpg")
    return (
        '<section class="page">'
        f'{chrome()}'
        f'{titleblock(num, kicker, title, subtitle)}'
        f'<div class="content"><img class="{cls}" src="{EX}/{jpg}" alt=""></div>'
        f'{footer()}'
        '</section>'
    )


def text_page():
    paras = "".join(f"<p>{p}</p>" for p in STACKED_PARAGRAPHS)
    return (
        '<section class="page">'
        f'{chrome()}'
        f'{titleblock(23, "Production", "Multiple Stacked Proven Production", "Van Zandt County &middot; East Texas Salt Structure Province")}'
        f'<div class="bodytext">{paras}</div>'
        f'{footer()}'
        '</section>'
    )


def contact_page():
    return (
        '<section class="page">'
        f'{chrome()}'
        f'<img class="contact-logo" src="{LOGO}" alt="Ferox Oil">'
        '<div class="contact-title">Contact Information</div>'
        '<div class="contact-bar"></div>'
        '<div class="contact-block">'
        '<div class="co-name">FEROX OIL, LLC</div>'
        '1910 Pacific Ave., Suite 5015<br>'
        'Dallas, TX 75201<br>'
        'P: (214) 257 - 0319<br>'
        '<a href="https://www.feroxoil.com">www.feroxoil.com</a>'
        '</div>'
        f'<div class="disclaimer">{DISCLAIMER}</div>'
        f'{footer()}'
        '</section>'
    )


def main():
    pages = [cover_page(), toc_page()]
    by_num = {p[0]: p for p in EXHIBIT_PAGES}
    for num in range(3, 26):
        if num == 23:
            pages.append(text_page())
        else:
            n, kicker, title, sub, img, bare = by_num[num]
            pages.append(exhibit_page(n, kicker.upper(), title, sub, img, bare))
    pages.append(contact_page())

    doc = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<title>Ferox Oil — Robinson #1</title>"
        "<link rel='stylesheet' href='../assets/fonts/fonts.css'>"
        "<link rel='stylesheet' href='style.css'>"
        "</head><body>" + "".join(pages) + "</body></html>"
    )
    with open(OUT, "w") as fh:
        fh.write(doc)
    print(f"wrote {OUT} ({len(pages)} pages)")


if __name__ == "__main__":
    main()
