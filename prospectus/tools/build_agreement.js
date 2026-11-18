// Robinson #1 subscription packet — modeled on Ferox Oil's Lilly #1-H form.
// Unit price $45,000 per 1% WI (.75% NRI), matching the Robinson financial
// projection's payout basis. Well facts from the approved RRC W-1 (vertical,
// 8,900 ft TD) and the geologist's summary (Travis Peak primary target).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType,
  BorderStyle, PageBreak, LevelFormat, convertInchesToTwip,
} = require("docx");

const ROOT = path.join(__dirname, "..");
const LOGO = path.join(ROOT, "assets", "brand", "ferox-logo.png");
const OUT = path.join(ROOT, "agreements", "Ferox-Oil-Robinson-1-Subscription-Agreement.docx");

const FONT = "Times New Roman";
const SZ = 22; // 11pt half-points

const t = (text, opts = {}) => new TextRun({ text, font: FONT, size: SZ, ...opts });
const p = (children, opts = {}) =>
  new Paragraph({ children: Array.isArray(children) ? children : [children], ...opts });
const body = (text, opts = {}) =>
  p(t(text), { spacing: { after: 160 }, ...opts });

const logo = () =>
  p(
    new ImageRun({
      type: "png",
      data: fs.readFileSync(LOGO),
      transformation: { width: 255, height: 70 },
    }),
    { alignment: AlignmentType.CENTER, spacing: { after: 60 } }
  );

const addressBlock = () => [
  p(t("Ferox Oil, LLC"), { spacing: { after: 0 } }),
  p(t("1910 Pacific Ave., Suite 5015"), { spacing: { after: 0 } }),
  p(t("Dallas, TX 75201"), { spacing: { after: 240 } }),
];

const field = (label) => [
  new Paragraph({
    children: [],
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000" } },
    spacing: { after: 60 },
  }),
  p(t(label), { alignment: AlignmentType.CENTER, spacing: { after: 420 } }),
];

const numbered = (ref, text) =>
  p(t(text), {
    numbering: { reference: ref, level: 0 },
    spacing: { after: 160 },
  });

const doc = new Document({
  numbering: {
    config: ["understands", "suitability"].map((ref) => ({
      reference: ref,
      levels: [
        {
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "%1.",
          alignment: AlignmentType.START,
          style: {
            paragraph: {
              indent: { left: convertInchesToTwip(0.75), hanging: convertInchesToTwip(0.3) },
            },
            run: { font: FONT, size: SZ },
          },
        },
      ],
    })),
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: {
            top: convertInchesToTwip(0.8),
            bottom: convertInchesToTwip(0.8),
            left: convertInchesToTwip(1.0),
            right: convertInchesToTwip(1.0),
          },
        },
      },
      children: [
        // ---------------- page 1 ----------------
        logo(),
        ...addressBlock(),
        p(t("The Robinson #1 Prospect", { bold: true }), {
          alignment: AlignmentType.CENTER,
          spacing: { after: 320 },
        }),
        body("Subscription agreement"),
        body(
          "The “Undersigned” / (Non-Operating Participant) understands that Ferox Oil, LLC is " +
          "offering for sale Units of fractional Working Interest (Units) in the above-referenced " +
          "Prospect. I further understand that the Units are being offered to prospective purchasers " +
          "at a price payable in one (1) installment. $45,000.00 for Drilling, Testing and completion " +
          "per Unit. The first installment is due with this Subscription Agreement. There may be " +
          "additional costs associated with the Drilling, Testing and Completion of the Prospect. In " +
          "the event the Prospect exceeds the estimated cost, the notice is given. Failure to pay any " +
          "additional cost could result in the loss of all Working Interest purchased and owned by " +
          "the Undersigned."
        ),
        body("All checks should be made Payable to “Ferox Oil, LLC”", { spacing: { after: 320 } }),
        body(
          "Subscription:  I hereby subscribe and agree to purchase ________ Unit(s), and tender this " +
          "Subscription Agreement, together with a check made payable to Ferox Oil, LLC in the amount " +
          "of $______________ ($45,000.00 x Number of Unit(s) purchased).",
          { spacing: { after: 320 } }
        ),
        p(
          t(
            "Each unit – which represents a 1% Working Interest (.75% of the Net Revenue Interest) " +
            "is priced at $45,000.00 for Drilling and Testing and completion (estimated cost basis)."
          ),
          { indent: { firstLine: convertInchesToTwip(0.5) }, spacing: { after: 320 } }
        ),
        p(t("The Undersigned understands that:"), {
          indent: { firstLine: convertInchesToTwip(0.5) },
          spacing: { after: 200 },
        }),
        numbered(
          "understands",
          "Upon execution of this subscription agreement by the Undersigned, payment by the " +
          "Undersigned for the Unit(s) subscribed shall be due and payable and must accompany the " +
          "delivery of this agreement to Ferox Oil, LLC"
        ),
        numbered(
          "understands",
          "The Unit(s) involve a high degree of risk of loss by the Undersigned of the " +
          "Undersigned’s investment in the Prospect.  There is no assurance or guarantee of any " +
          "income from this Prospect."
        ),
        numbered(
          "understands",
          "One Unit of participation in the Prospect constitutes a 1% Working Interest and .75% Net " +
          "Revenue Interest."
        ),
        numbered(
          "understands",
          "The Prospect will consist of Working Interest in one Well with a vertical depth of " +
          "8,900 ft. +/- to encounter the Travis Peak formation."
        ),
        numbered(
          "understands",
          "There are various risks involved with the exploration and development of oil and gas " +
          "prospects, including those involving normal drilling operations, complication in high " +
          "pressured reservoirs, drilling and production risks (including, but not limited to " +
          "possible loss of circulation, well bore collapses, blowouts, stuck drill pipe, production " +
          "declines and speculative revenues) any of which may affect the economic feasibility of an " +
          "oil and gas well."
        ),
        numbered(
          "understands",
          "The net income, net losses, and distributions, if any, attributable to the Non-Operating " +
          "Participant will be allocated among the Non-Operating Participants in proportion to the " +
          "pro rata participation in the prospect."
        ),
        numbered(
          "understands",
          "The Units in the Prospect are to be held by the Undersigned, will be acquired by the " +
          "Undersigned, for the Undersigned’s own account or benefit and not for the account, in " +
          "whole or part of any other persons or business entity."
        ),
        numbered(
          "understands",
          "The Undersigned is experienced in business matters and has sufficient business acumen to " +
          "analyze and evaluate the merits and risk of participation in the Prospect. The " +
          "Undersigned acknowledges and understands that the Units in the Prospect are not intended " +
          "to be “securities” as defined in any federal, state statute, law or regulation."
        ),
        numbered(
          "understands",
          "The Undersigned understands that this agreement and all other documents prepared for the " +
          "benefit of the person who will likely be acceptable to Ferox Oil, LLC as Non-Operating " +
          "Participants. The Undersigned agrees that the Undersigned will not reproduce or " +
          "distribute, by any means, any of those documents in whole or in part."
        ),
        p(t("Suitability", { bold: true, underline: {} }), {
          alignment: AlignmentType.CENTER,
          spacing: { before: 160, after: 240 },
        }),
        numbered(
          "suitability",
          "Representations and warranties of the Undersigned: I Understand that the units will be " +
          "offered and sold in reliance upon certain exemptions from securities registration " +
          "provisions of the Securities Act of 1933, as amended, and certain non-public offering " +
          "exemptions of the securities acts of the states in which the Units may be offered. As a " +
          "condition to purchasing Units, and for the purposes of the above-mentioned exemptions " +
          "and/or qualifications to the extent applicable, and knowing that you will rely upon the " +
          "statements made herein for such exemptions and in determining my suitability as a Non- " +
          "Operating Participant, I represent and warrant to you that:"
        ),
        body(
          "I am a person who meets one or more of the following categories of Accredited Investor " +
          "as defined in rule 506(b) of Regulation D (initial which category you meet).",
          { spacing: { after: 320 } }
        ),
        p(
          t(
            "________ 1. Any natural person whose individual net worth, or joint net worth with that " +
            "persons spouse, at the time of this purchase exceeds $1,000,000.00"
          ),
          { indent: { left: convertInchesToTwip(0.5) }, spacing: { after: 320 } }
        ),
        p(
          t(
            "________ 2. Any natural person who had an individual income in excess of $200,000.00 in " +
            "each of the two most recent years or joint income with that person’s spouse in excess " +
            "of $300,000.00 in each year of those years and has a reasonable expectation of reaching " +
            "that same income level in the current year."
          ),
          { indent: { left: convertInchesToTwip(0.5) }, spacing: { after: 160 } }
        ),
        // ---------------- page 3: ownership of record ----------------
        new Paragraph({ children: [new PageBreak()] }),
        logo(),
        ...addressBlock(),
        p(t("Ownership of Record", { bold: true, underline: {} }), {
          alignment: AlignmentType.CENTER,
          spacing: { after: 480 },
        }),
        ...field("Printed Name of Non-Operating Participant"),
        ...field("Street Address for all Notices"),
        ...field("City, State and Zip Code"),
        ...field("Social Security or Federal Taxpayer ID Number"),
        ...field("Area Code and Telephone Number"),
        ...field("Email Address"),
        ...field("Signature of Non-Operating Participant"),
        p(
          t(
            "The foregoing subscription is hereby accepted as of: _______________________________"
          ),
          { spacing: { before: 240, after: 320 } }
        ),
        p(t("By: _____________________________________________________________________"), {
          spacing: { after: 0 },
        }),
        p(t("Ferox Oil, LLC"), { spacing: { after: 0 } }),
        p(t("Brandon Chance, President"), { spacing: { after: 0 } }),
      ],
    },
  ],
});

fs.mkdirSync(path.dirname(OUT), { recursive: true });
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT);
});
