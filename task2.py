from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
OUT_FILE = DATA_DIR / "pink_morsels_formatted.csv"

def to_number(s: pd.Series) -> pd.Series:
    # Cleans values like "$3.50", "1,200", etc.
    return pd.to_numeric(
        s.astype(str).str.replace(r"[^\d\.\-]", "", regex=True),
        errors="coerce"
    )

def main():
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    # If you re-run, avoid accidentally re-reading your output file
    csv_files = [f for f in csv_files if f.name != OUT_FILE.name]

    if not csv_files:
        raise FileNotFoundError(f"No input CSVs found in {DATA_DIR.resolve()}")

    outputs = []
    for f in csv_files:
        df = pd.read_csv(f)
        df.columns = [c.strip().lower() for c in df.columns]

        required = {"product", "quantity", "price", "date", "region"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{f.name} missing columns {missing}. Found: {list(df.columns)}")

        # Keep only Pink Morsels
        df = df[df["product"].astype(str).str.strip().str.lower() == "pink morsel"].copy()

        # Sales = quantity * price
        df["sales"] = to_number(df["quantity"]) * to_number(df["price"])

        # Keep only required output fields
        out = df[["sales", "date", "region"]].copy()
        outputs.append(out)

    result = pd.concat(outputs, ignore_index=True)

    # Column names exactly as requested + correct order
    result = result.rename(columns={"sales": "Sales", "date": "Date", "region": "Region"})
    result = result[["Sales", "Date", "Region"]]

    result.to_csv(OUT_FILE, index=False)
    print(f"Wrote {len(result)} rows to {OUT_FILE}")

if __name__ == "__main__":
    main()
