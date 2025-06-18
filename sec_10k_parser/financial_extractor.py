from bs4 import BeautifulSoup
import pandas as pd
import re
from io import StringIO

def extract_target_financials(ixbrl_html):
    soup = BeautifulSoup(ixbrl_html, features="xml")

    tags = soup.find_all(['ix:nonFraction', 'ix:nonNumeric'])
    rows = []

    for tag in tags:
        name = tag.get('name', '').lower()
        context = tag.get('contextRef', '').lower()
        value = tag.text.strip()

        # Look for relevant fields in balance sheet
        if 'asset' in name or 'liabilit' in name or 'equity' in name:
            rows.append({
                "Name": name,
                "Context": context,
                "Value": value
            })

    df = pd.DataFrame(rows)

    if not df.empty:
        print(f"[DEBUG] Found {len(df)} balance sheet-like entries via iXBRL tags.")
        return {"Consolidated Balance Sheet": df}

    return {}
