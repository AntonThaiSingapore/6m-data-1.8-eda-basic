"""
Generate the messy "Daily Grind" POS export used as the spine for Lesson 1.8.

Provenance
----------
Lessons 1.8, 1.9 and 1.10 are three stages of one business problem: a four-outlet café
chain whose revenue has been flat for two quarters.

  * 1.9 works on `daily_sales.csv` — 18 months, already clean.
  * 1.8 works on **one month of the same data, before anyone cleaned it**: the raw till
    export for June 2025, with every problem a real POS export arrives with.

So this script takes the June 2025 slice of Lesson 1.9's clean file and *breaks* it in the
specific ways the lesson teaches learners to fix. Cleaning it in class reproduces (almost
exactly) the June figures that Lesson 1.9 starts from.

What is deliberately wrong with cafe_june_raw.csv
-------------------------------------------------
  outlet          12 free-typed spellings for 4 cafés (case, spacing, abbreviations)
  date_text       dd/mm/yyyy text, so it sorts and filters like words, not dates
  daypart         9 labels for 3 dayparts ("Morning", "morning", "AM", ...)
  revenue_raw     text: "S$1,240.50", " 987.20 ", "1240.5" -> must be parsed to a number
                  + 4 rows carry the sentinel -999 ("till error" in the old system)
                  + 1 row is a decimal-shift typo (x100)
                  + 3 rows are blank
  tickets         2 zeros with non-zero revenue, 1 negative, 2 blanks
  items           3 blanks
  staff_on_shift  5 blanks
  manager         stray leading/trailing spaces and inconsistent case
  manager_email   2 blanks; used for the string/regex section
  notes           mostly empty, with "n/a", "N.A." and "-" used as fake blanks
  + 6 exact duplicate rows (the till re-sent one batch)

Also written (small files for the read/write section):
  ex1.csv  plain csv with a header
  ex2.csv  the same, with no header row
  ex3.txt  whitespace-separated
  ex4.csv  two comment lines before the header
  ex5.csv  missing values spelled five different ways
  cafe_june_workbook.xlsx   two sheets: "June" and "Outlets"
  cafe.db  SQLite: tables `daily_sales_june` and `outlets`

Run:
    python make_cafe_raw.py
    python make_cafe_raw.py --source /path/to/daily_sales.csv
"""

import argparse
import os

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260801)
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SOURCE = os.path.join(
    HERE, "..", "..", "6m-data-1.9-eda-advanced", "data", "daily_sales.csv"
)

# Four cafés, and the many ways staff type their names into the till.
OUTLETS = {
    "OUT-01": ("Raffles Place", ["Raffles Place", "raffles place", "RAFFLES PLACE", "Raffles Pl."]),
    "OUT-02": ("Tampines Mall", ["Tampines Mall", "tampines mall", "Tampines  Mall"]),
    "OUT-03": ("Marina Bay", ["Marina Bay", "marina bay", "Marina Bay "]),
    "OUT-04": ("Holland Village", ["Holland Village", "Holland V"]),
}

MANAGERS = {
    "OUT-01": ("  Aisha Rahman ", "aisha.rahman@dailygrind.sg"),
    "OUT-02": ("wei ming tan", "weiming.tan@dailygrind.sg"),
    "OUT-03": ("Priya  Nair", "priya.nair@dailygrind.sg"),
    "OUT-04": ("DANIEL LIM ", "daniel.lim@dailygrind.com.sg"),
}

DAYPART_LABELS = {
    "Morning": ["Morning", "morning", "AM"],
    "Midday": ["Midday", "midday", "Lunch"],
    "Evening": ["Evening", "evening", "PM"],
}

FAKE_BLANKS = ["n/a", "N.A.", "-", ""]
REAL_NOTES = ["aircon down from 2pm", "public holiday", "new machine installed", "staff short"]


def money_text(value: float) -> str:
    """Format a number the way the till exports it - inconsistently."""
    style = RNG.integers(0, 3)
    if style == 0:
        return f"S${value:,.2f}"
    if style == 1:
        return f" {value:,.2f} "
    return f"{value:.2f}"


def build(source: str) -> pd.DataFrame:
    clean = pd.read_csv(source, parse_dates=["date"])
    june = clean[
        (clean["date"] >= "2025-06-01")
        & (clean["date"] <= "2025-06-30")
        & (clean["outlet_id"] != "OUT-05")
    ].copy()
    june = june.sort_values(["date", "outlet_id", "daypart"]).reset_index(drop=True)

    rows = []
    for _, r in june.iterrows():
        oid = r["outlet_id"]
        spellings = OUTLETS[oid][1]
        manager, email = MANAGERS[oid]
        rows.append(
            {
                "outlet": str(RNG.choice(spellings)),
                "date_text": r["date"].strftime("%d/%m/%Y"),
                "daypart": str(RNG.choice(DAYPART_LABELS[r["daypart"]])),
                "revenue_raw": money_text(float(r["revenue_sgd"])),
                "tickets": int(r["tickets"]),
                "items": int(r["items"]),
                "staff_on_shift": int(np.clip(round(r["tickets"] / 22) + 1, 1, 6)),
                "manager": manager,
                "manager_email": email,
                "notes": str(RNG.choice(FAKE_BLANKS, p=[0.06, 0.04, 0.05, 0.85])),
            }
        )
    df = pd.DataFrame(rows)

    # A few genuine notes, so `notes` is not purely junk.
    for i in RNG.choice(len(df), size=4, replace=False):
        df.loc[i, "notes"] = str(RNG.choice(REAL_NOTES))

    # ---------------------------------------------------------------- break it
    # 4 sentinel values: the old till wrote -999 when a shift failed to close off.
    for i in [37, 104, 221, 298]:
        df.loc[i, "revenue_raw"] = "-999"

    # 1 decimal-shift typo: someone keyed 98000 instead of 980.00.
    df.loc[152, "revenue_raw"] = "98000"

    # 3 blank revenues.
    for i in [64, 190, 333]:
        df.loc[i, "revenue_raw"] = ""

    # Ticket-count problems: 2 zeros with real revenue, 1 negative, 2 blanks.
    df.loc[[71, 245], "tickets"] = 0
    df.loc[188, "tickets"] = -4
    df.loc[[12, 260], "tickets"] = np.nan

    # 3 blank item counts, 5 blank staffing numbers.
    df.loc[[45, 133, 301], "items"] = np.nan
    df.loc[[8, 96, 174, 250, 340], "staff_on_shift"] = np.nan

    # 2 missing manager emails.
    df.loc[[19, 207], "manager_email"] = ""

    # 6 exact duplicate rows: the till re-sent one batch.
    dupe_idx = [30, 31, 32, 155, 156, 289]
    df = pd.concat([df, df.loc[dupe_idx]], ignore_index=True)

    # Sort by the *text* date, which is exactly the wrong thing to do -- and is what an
    # export sorted by a string column actually looks like.
    return df.sort_values("date_text", kind="stable").reset_index(drop=True)


def small_files(clean_june: pd.DataFrame) -> None:
    """The little files used by the reading-and-writing section."""
    sample = clean_june.head(4).copy()
    sample.columns = ["date", "outlet_id", "daypart", "tickets", "items", "revenue_sgd"]

    sample.to_csv(os.path.join(HERE, "ex1.csv"), index=False)
    sample.to_csv(os.path.join(HERE, "ex2.csv"), index=False, header=False)

    with open(os.path.join(HERE, "ex3.txt"), "w") as f:
        f.write("date outlet_id daypart tickets items revenue_sgd\n")
        for _, r in sample.iterrows():
            f.write(
                f"{r['date']}   {r['outlet_id']}  {r['daypart']}   "
                f"{r['tickets']}   {r['items']}   {r['revenue_sgd']}\n"
            )

    with open(os.path.join(HERE, "ex4.csv"), "w") as f:
        f.write("# Daily Grind POS export\n")
        f.write("# generated automatically - do not edit\n")
        sample.to_csv(f, index=False)

    with open(os.path.join(HERE, "ex5.csv"), "w") as f:
        f.write("date,outlet_id,daypart,tickets,revenue_sgd\n")
        f.write("2025-06-01,OUT-01,Morning,50,324.52\n")
        f.write("2025-06-01,OUT-02,Morning,,NA\n")
        f.write("2025-06-01,OUT-03,Morning,NULL,241.90\n")
        f.write("2025-06-01,OUT-04,Morning,18,n/a\n")
        f.write("2025-06-01,OUT-04,Midday,-999,155.40\n")


def workbook_and_db(clean_june: pd.DataFrame, outlets: pd.DataFrame) -> None:
    xlsx = os.path.join(HERE, "cafe_june_workbook.xlsx")
    with pd.ExcelWriter(xlsx) as writer:
        clean_june.to_excel(writer, sheet_name="June", index=False)
        outlets.to_excel(writer, sheet_name="Outlets", index=False)

    try:
        import sqlalchemy as sqla
    except ImportError:
        print("sqlalchemy not installed - skipped cafe.db")
        return

    db = os.path.join(HERE, "cafe.db")
    if os.path.exists(db):
        os.remove(db)
    engine = sqla.create_engine(f"sqlite:///{db}")
    clean_june.to_sql("daily_sales_june", engine, index=False, if_exists="replace")
    outlets.to_sql("outlets", engine, index=False, if_exists="replace")
    engine.dispose()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="path to Lesson 1.9's clean daily_sales.csv")
    args = ap.parse_args()

    if not os.path.exists(args.source):
        raise SystemExit(
            f"Cannot find {args.source}.\n"
            "This script derives the messy June export from Lesson 1.9's clean daily_sales.csv.\n"
            "Pass its location with --source, or just use the cafe_june_raw.csv already in data/."
        )

    raw = build(args.source)
    raw.to_csv(os.path.join(HERE, "cafe_june_raw.csv"), index=False)

    clean = pd.read_csv(args.source, parse_dates=["date"])
    june = clean[
        (clean["date"] >= "2025-06-01")
        & (clean["date"] <= "2025-06-30")
        & (clean["outlet_id"] != "OUT-05")
    ].copy()
    june["date"] = june["date"].dt.strftime("%Y-%m-%d")
    june = june.sort_values(["date", "outlet_id"]).reset_index(drop=True)

    outlets = pd.DataFrame(
        [(k, v[0], MANAGERS[k][0].strip().title(), MANAGERS[k][1]) for k, v in OUTLETS.items()],
        columns=["outlet_id", "outlet_name", "manager", "manager_email"],
    )

    small_files(june)
    workbook_and_db(june, outlets)

    print(f"cafe_june_raw.csv : {len(raw)} rows x {raw.shape[1]} columns")
    print(f"  outlet spellings : {raw['outlet'].nunique()}")
    print(f"  daypart labels   : {raw['daypart'].nunique()}")
    print(f"  duplicate rows   : {int(raw.duplicated().sum())}")
    print(f"  blank cells      : {int(raw.isna().sum().sum() + (raw == '').sum().sum())}")
    print()
    print("The clean June total Lesson 1.9 starts from: "
          f"${june['revenue_sgd'].sum():,.2f} across {len(june)} rows")


if __name__ == "__main__":
    main()
