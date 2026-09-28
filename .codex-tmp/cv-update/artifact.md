# CV template execution contract

## Reference

- Source: `/Users/linxiao/.codex/skills/artifact-template-linxiao-wu-cv/assets/reference.docx`
- SHA-256: `41b79adab0bdd8be372943236be1716d55e1236684782072a83d4f87a0ea186d`
- Evidence: `reference-render/page-1.png`, `reference-render/reference.pdf`, and `template-style-evidence.json`
- Structure: one page, one section, 45 body paragraphs, no tables, images, fields, content controls, headers, or footers

## Page system

- Portrait page, 8.49 x 10.98 inches, with 0.51-inch margins on all sides
- One continuous body section; no first-page, odd/even header, footer, or recurring page furniture
- Single-column layout with right-aligned tab stops at approximately 7.48 inches for location and date metadata

## Typography and paragraph roles

- Name: centered, bold, 24 pt in the reference; retain the centered high-contrast name block
- Contact line: centered, approximately 9 pt, with pipe separators
- Section heading: bold, approximately 10 pt, black, with a thin black bottom rule
- Institution/company/project heading: bold, approximately 10-10.5 pt, left aligned; right-side location/date on a right tab stop
- Role/degree line: approximately 9 pt with right-aligned dates
- Body and bullets: approximately 9-10 pt, compact single spacing; bullets use a hanging indent
- Skills: three compact label/value rows with bold labels
- Latin text follows the reference's serif/sans-serif hierarchy; Chinese uses a CJK serif face while preserving the same density and alignment

## Components and flow

1. Name and contact line
2. Education
3. Experience, newest first
4. Projects, newest/most relevant first
5. Technical skills

## Slot map

- Name/contact: replace with the current English or Chinese identity line; preserve phone, email, website, and GitHub from the supplied CVs
- Education: replace dates and GPA only as specified; retain supplied honors
- Experience: retain WingSemi and CanSemi/Yuexin in reverse chronological order; include only supplied responsibilities
- Projects: retain Apple CNN accelerator, P6 RISC-V processor, N-Body formal verification, and FIR filter descriptions from supplied CVs
- Skills: replace with the user's exact EDA, programming, and focus-area lists
- Unsupported claims, new awards, publications, positions, and metrics are prohibited

## Package preservation

- Preserve `[Content_Types].xml`, root relationships, theme, settings, numbering, styles, web settings, font table, footnotes, endnotes, and document relationships from the reference copy.
- The editable part is `word/document.xml` body content; section properties and page geometry remain unchanged.
- The reference contains no drawings, external relationships, comments, fields, headers, footers, or content controls requiring preservation.

## Fidelity gates

- Reference SHA-256 must remain unchanged.
- Final documents must remain one page unless content legibility requires two; page geometry and section count must match the reference.
- Render every final DOCX, inspect all page PNGs at full resolution, and verify no clipping, overlap, missing glyphs, orphan headings, or broken right-tab alignment.
- Re-run section/style/heading/image/field/content-control audits and compare package parts before delivery.
