# 📄 SEC 10-K Parser

This project automates the extraction, cleaning, and normalization of balance sheet data from 10-K filings submitted to the [U.S. Securities and Exchange Commission (SEC)](https://www.sec.gov/). It's designed to programmatically pull and process filings (primarily iXBRL HTML), isolate the consolidated balance sheet tables, and convert them into structured CSV files for analysis.

---

## 🔍 Features

- ✅ Parses 10-K filings via SEC’s EDGAR API and archives.
- ✅ Extracts relevant financial tables using keyword-based heuristics.
- ✅ Cleans and normalizes balance sheets for consistent formatting.
- ✅ Handles multiple tables and historical comparisons in a single filing.
- ✅ Outputs structured `.csv` files to a local `/data` folder.

---

## 🛠 Setup

### Requirements

- Python 3.8+
- `pandas`
- `beautifulsoup4`
- `requests`
- `lxml`
