from fetchers.sec_api import get_10k_filings, get_ixbrl_urls, get_with_retries
from parsers.financial_extractor import extract_target_financials
from parsers.balance_sheet_cleaner import clean_consolidated_balance_sheet
from utils.io_utils import save_tables
from config import HEADERS

def run():
    print("[INFO] Starting 10-K filing extraction process...")
    filings = get_10k_filings()

    for filing_url, report_date in filings:
        print(f"\n[INFO] Processing filing URL: {filing_url}")

        ixbrl_url = get_ixbrl_urls(filing_url)
        if not ixbrl_url:
            print(f"[WARN] No iXBRL URL found for filing: {filing_url}")
            continue

        # ✅ Fix: Ensure headers are passed in this request
        html_res = get_with_retries(ixbrl_url, headers=HEADERS)
        if not html_res:
            print(f"[WARN] Failed to fetch iXBRL content from: {ixbrl_url}")
            continue

        financial_tables = extract_target_financials(html_res.text)
        balance_sheet_df = financial_tables.get("Consolidated Balance Sheet")
        if balance_sheet_df is None:
            print(f"[WARN] No Consolidated Balance Sheet found in iXBRL for: {ixbrl_url}")
            continue

        cleaned_df = clean_consolidated_balance_sheet(balance_sheet_df)
        if cleaned_df.empty:
            print(f"[WARN] Cleaned Consolidated Balance Sheet is empty for: {ixbrl_url}")
            continue

        save_tables(cleaned_df, report_date, "Consolidated Balance Sheet")
        print(f"[SUCCESS] Saved cleaned balance sheet for report date {report_date}")

    print("\n[INFO] Processing complete.")


if __name__ == '__main__':
    run()

