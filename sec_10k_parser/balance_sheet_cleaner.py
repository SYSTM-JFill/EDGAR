import pandas as pd
import re

def clean_consolidated_balance_sheet(df_raw):
    print("\n[DEBUG] Raw DataFrame Preview:")
    print(df_raw.head(10).to_string(index=False))
    print("=" * 60)

    # Drop fully empty rows and columns, reset index
    df = df_raw.dropna(how='all').dropna(axis=1, how='all').reset_index(drop=True)

    # Identify header row by searching for key terms in the row string
    header_row_idx = None
    for i, row in df.iterrows():
        joined = ' '.join(row.astype(str)).lower()  # fixed .lower() usage here
        # Look for common balance sheet section headers, case insensitive
        if any(x in joined for x in ['assets', 'liabilities', 'equity', 'shareholders']):
            header_row_idx = i
            break

    if header_row_idx is None:
        print("[WARN] Couldn't identify header row in balance sheet.")
        return pd.DataFrame()

    # Set the header row as columns
    df.columns = df.iloc[header_row_idx].astype(str).str.strip()
    df = df.iloc[header_row_idx + 1:].reset_index(drop=True)

    # Drop fully empty columns after resetting headers
    df = df.dropna(axis=1, how='all')

    # Optional: Strip whitespace and normalize headers
    def normalize_col(col_name):
        col_name = str(col_name).strip()
        # Replace ambiguous c-XX headers with Period_XX or drop if desired
        if re.match(r"c-\d+", col_name.lower()):
            # Example: map c-22 → Period_22
            return f"Period_{col_name.split('-')[1]}"
        return col_name

    df.columns = [normalize_col(col) for col in df.columns]

    # Forward-fill main line items in the first column to handle merged cells (common in SEC tables)
    if df.shape[1] > 0:
        df.iloc[:, 0] = df.iloc[:, 0].ffill()

    # Strip whitespace from all string cells to clean formatting
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df

def normalize_balance_sheet(df):
    df = df.copy()

    # Rename first column to 'Line Item'
    if len(df.columns) > 0:
        df.rename(columns={df.columns[0]: "Line Item"}, inplace=True)

    # Clean numeric columns
    for col in df.columns[1:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[\$,)]", "", regex=True)
            .str.replace("(", "-", regex=False)
            .str.replace(",", "")
            .str.strip()
        )

        # Convert to numeric, coercing errors to NaN
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
