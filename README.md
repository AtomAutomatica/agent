# agent

Your final downloadable file is:

- `dist/owner_distribution_statement_76051_downloadable.csv`

## What changed
- Combined page 1 + page 2 into **one CSV** with a **single consistent schema**.
- Used `record_type` to separate table types:
  - `page1` for production/expense rows
  - `page2_summary` for summary rows from page 2
- Kept output text-only (no binary zip required).

## Rebuild downloadable CSV
```bash
python build_invoice_package.py
```

## Validation
- See `validation_report.txt` for parse status and any problematic rows.
