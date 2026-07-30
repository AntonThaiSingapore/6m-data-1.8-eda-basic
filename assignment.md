# 📝 Assignment: EDA Basic — The May Export Audit

> ⏱️ **Estimated Time:** 60–75 minutes | Complete this **after** your class session.

---

## 🎯 Learning Objectives Revisited

This assignment reinforces what you practised in class:

- Summarising a dataset with descriptive statistics
- Handling missing values, duplicates and impossible values
- Transforming string, categorical and date data
- Reading and writing files

**The four beats apply to every task:** *find it → decide → apply → verify.* Write down your decision
and your reason before you write the fix.

---

## Part 1: Conceptual Check (15 min)

**Question 1:** How do you select the rows of a DataFrame where **any** value in the row exceeds a
given threshold?

**Question 2:** How do you sort a DataFrame by column `A` ascending and column `B` descending at the
same time?

**Question 3:** A takings column contains four `-999` sentinel codes and three genuinely missing
values. You run `df["takings"].fillna(df["takings"].median())` and then remove the -999s. What is
wrong with the result, and what is the correct order?

**Question 4:** What is the difference between *removing* an outlier and *capping* it? When would you
choose each?

**Question 5:** You call `df.fillna(df.mean())` on a DataFrame with both numeric and text columns.
What happens, and what would you do instead?

<details>
<summary>💡 Check Your Answers</summary>

**Q1:** `df[df.max(axis=1) > threshold]` — compute the row-wise maximum, then keep the rows where it
exceeds the threshold. (`axis=1` means "across the columns", i.e. one answer per row.)

**Q2:** `df.sort_values(["A", "B"], ascending=[True, False])` — one entry in the `ascending` list per
column being sorted.

**Q3:** The statistic was computed while the sentinels were still present, and that contaminated figure
was written into the three genuine holes. Removing the -999s afterwards does not undo it. The correct
order is: **mask the sentinels to NaN → compute the statistic → fill.**

How much damage it does depends on which statistic you used. A **median** is barely moved by a handful
of extremes — that is why it is the safer default. A **mean** is wrecked by them. Since you cannot tell
from the outside how many sentinels a file contains, order the steps properly every time. Nothing here
errors, which is exactly why this bug survives into reports.

**Q4:** **Removing** deletes the row, which shrinks your dataset and can bias it (extreme rows are
often not random). **Capping** keeps the row but pulls the value back to a boundary, preserving the
row count while limiting the distortion. Remove when the value is clearly an error and the rest of the
row is unusable; cap when the row is otherwise good and the extreme is real but disruptive. Mark it
missing when you believe the value is wrong but have no defensible replacement.

**Q5:** `.mean()` is only computed for numeric columns, so text columns are silently left with their
holes — you will think you have filled everything. Be explicit instead:
`df.fillna({"takings": df["takings"].median(), "outlet": "Unknown"})`. A dictionary forces you to make
one decision per column, which is the point.

</details>

---

## Part 2: Practical Challenge (45–60 min)

### Scenario: "The May Export Audit"

The owner was impressed with your June clean-up and has sent the **May** export. It is a different
extract from the same till system, so it has the same *kinds* of problems in different places.

Start a new notebook in `notebooks/` and paste this in:

```python
import pandas as pd
import numpy as np

may = pd.DataFrame({
    "outlet": ["Raffles Place", "raffles place", "RAFFLES PLACE", "Raffles Pl.",
               "Marina Bay", "marina bay", "Marina Bay ", "Marina Bay",
               "Tampines Mall", "tampines mall", "Holland Village", "Holland V"],
    "date_text": ["01/05/2025", "01/05/2025", "02/05/2025", "02/05/2025",
                  "01/05/2025", "01/05/2025", "02/05/2025", "02/05/2025",
                  "01/05/2025", "02/05/2025", "01/05/2025", "02/05/2025"],
    "daypart": ["Morning", "AM", "morning", "Midday",
                "Lunch", "midday", "Evening", "PM",
                "evening", "Morning", "AM", "Lunch"],
    "revenue_raw": ["S$612.40", " 318.75 ", "-999", "487.10",
                    "S$1,204.60", "296.55", "", "58000",
                    "S$734.20", "421.85", "S$389.90", "-999"],
    "tickets": [74, 39, 55, 58, 141, 36, 21, 112, 88, 51, np.nan, -3],
    "staff_on_shift": [3, 2, np.nan, 2, 5, 2, 1, 4, 4, 2, 2, np.nan],
    "manager": ["  Aisha Rahman ", "aisha rahman", "AISHA RAHMAN", "  Aisha Rahman",
                "Priya  Nair", "priya nair", "Priya Nair ", "Priya Nair",
                "wei ming tan", "Wei Ming Tan", "DANIEL LIM ", "Daniel Lim"],
    "notes": ["", "n/a", "N.A.", "-", "aircon down", "", "-", "", "n/a", "", "N.A.", ""],
})

may
```

---

### Challenge 1: The Health Check

**Tasks:**
1. Run the five-move first look: `.head()`, `.shape`, `.info()`, `.dtypes`, `.describe()`.
2. Which column is missing from `.describe()` output, and why?
3. Use `.isna().sum()` to count missing values per column. Then look at `notes` with
   `.value_counts(dropna=False)` — how many values *look* empty but are not?
4. How many distinct outlets does pandas think there are? How many are there really?

<details>
<summary>💡 Hint</summary>

`.describe()` only sees numeric columns. `revenue_raw` is text, so it is invisible — which is the
single most important finding of the health check, because it means none of the impossible values in
it can be spotted yet.

</details>

<details>
<summary>✅ Solution</summary>

```python
print(may.shape)
may.info()
print(may.describe())

print("\nmissing per column:")
print(may.isna().sum())

print("\nnotes, including the fake blanks:")
print(may["notes"].value_counts(dropna=False))

print("\noutlets pandas sees:", may["outlet"].nunique(), "| real cafés: 4")
```

**What to notice:**

- `.describe()` covers only `tickets` and `staff_on_shift`. `revenue_raw` is text.
- `.isna()` reports 1 missing ticket count and 2 missing staffing figures — and **0 missing notes**,
  because `""` was read as an empty string here (not from a CSV), and `n/a`, `N.A.` and `-` are all
  ordinary text. Eleven of the twelve notes are effectively blank — only `"aircon down"` is a real note — and
  `.isna()` sees none of them.
- **Eleven** distinct outlet strings for four cafés (two rows happen to share a spelling).
- `tickets` has a minimum of **-3**, which is impossible.

</details>

---

### Challenge 2: Clean the Data

**Tasks:**
1. Convert `revenue_raw` into a numeric column called `revenue_sgd`.
2. Replace the fake blanks in `notes` (`""`, `n/a`, `N.A.`, `-`) with `NaN`.
3. Mask the impossible values: negative takings, takings above 20,000, and ticket counts of zero or
   less.
4. Fill the resulting holes in `revenue_sgd` and `tickets` with each column's median — **in the right
   order**.
5. Standardise `outlet` to the four real café names, and `daypart` to Morning / Midday / Evening.
6. Verify: no impossible values left, and `outlet` has exactly four values.

<details>
<summary>✅ Solution</summary>

```python
clean = may.copy()

# 1. Text -> number. Strip everything that is not a digit, dot or minus sign.
clean["revenue_sgd"] = pd.to_numeric(
    clean["revenue_raw"].str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce"
)

# 2. Fake blanks -> real blanks, so .isna() tells the truth from here on.
clean["notes"] = clean["notes"].replace(["", "n/a", "N.A.", "-"], np.nan)

# 3. Mask the impossible values (find -> decide -> apply).
clean["revenue_sgd"] = clean["revenue_sgd"].mask(
    (clean["revenue_sgd"] < 0) | (clean["revenue_sgd"] > 20000)
)
clean["tickets"] = clean["tickets"].mask(clean["tickets"] <= 0)

# 4. NOW compute the medians -- after the sentinels and the typo are gone.
clean = clean.fillna({
    "revenue_sgd": clean["revenue_sgd"].median(),
    "tickets": clean["tickets"].median(),
    "staff_on_shift": clean["staff_on_shift"].median(),
})

# 5. Standardise the keys.
outlet_map = {
    "Raffles Place": "Raffles Place", "raffles place": "Raffles Place",
    "RAFFLES PLACE": "Raffles Place", "Raffles Pl.": "Raffles Place",
    "Marina Bay": "Marina Bay", "marina bay": "Marina Bay", "Marina Bay ": "Marina Bay",
    "Tampines Mall": "Tampines Mall", "tampines mall": "Tampines Mall",
    "Holland Village": "Holland Village", "Holland V": "Holland Village",
}
daypart_map = {
    "Morning": "Morning", "morning": "Morning", "AM": "Morning",
    "Midday": "Midday", "midday": "Midday", "Lunch": "Midday",
    "Evening": "Evening", "evening": "Evening", "PM": "Evening",
}
clean["outlet_name"] = clean["outlet"].map(outlet_map)
clean["daypart"] = clean["daypart"].map(daypart_map)

# 6. Verify -- every check must come back clean.
print("unmapped outlets:", clean["outlet_name"].isna().sum())
print("unmapped dayparts:", clean["daypart"].isna().sum())
print("cafés:", clean["outlet_name"].nunique())
print("min revenue:", clean["revenue_sgd"].min(), "| max:", clean["revenue_sgd"].max())
print("min tickets:", clean["tickets"].min())
```

**Watch the order in step 4.** Filling before masking would have computed the statistic from a column
still containing two `-999`s and one `58000`. Try both and print the numbers:

| | median | mean |
|---|---|---|
| computed **before** masking (wrong) | \$421.85 | \$5,497.03 |
| computed **after** masking (right) | \$454.48 | \$558.17 |

The **median** survives the mistake with a 7% error — that is the median doing its job. The **mean**
comes out **ten times too big**, and all four filled shifts would have carried it. The lesson is not
"the median gets poisoned"; it is **mask first, then compute**, because the median's robustness is a
safety net rather than a licence to skip the step.

</details>

---

### Challenge 3: Transform & Summarise

**Tasks:**
1. Convert `date_text` to a real datetime column called `date`. Careful: `01/05/2025` is 1 May here.
2. Clean the `manager` column so each manager's name appears exactly once, in Title Case.
3. Add a `shift_size` column with `pd.cut`: 0–350 `"Quiet"`, 350–700 `"Normal"`, 700–1500 `"Busy"`.
4. Build a summary table: one row per café, with total revenue, number of shifts and average revenue
   per shift, sorted by total revenue.

<details>
<summary>✅ Solution</summary>

```python
# 1. dayfirst=True matters: without it, 01/05/2025 could be read as 5 January.
clean["date"] = pd.to_datetime(clean["date_text"], dayfirst=True)

# 2. Strip the spaces off the ENDS, squeeze the doubled spaces in the MIDDLE, then Title Case.
#    `\s+` means "one or more whitespace characters"; replacing them with a single space turns
#    "Priya  Nair" into "Priya Nair". `.str.strip()` alone would not have caught that one.
clean["manager"] = (
    clean["manager"].str.strip().str.replace(r"\s+", " ", regex=True).str.title()
)
print(clean["manager"].unique())

# 3. Bands rather than 12 individual numbers.
clean["shift_size"] = pd.cut(
    clean["revenue_sgd"], bins=[0, 350, 700, 1500], labels=["Quiet", "Normal", "Busy"]
)
print(clean["shift_size"].value_counts())

# 4. The summary the owner would actually read.
summary = clean.groupby("outlet_name", observed=True).agg(
    revenue=("revenue_sgd", "sum"),
    shifts=("revenue_sgd", "size"),
    avg_shift=("revenue_sgd", "mean"),
).round(2).sort_values("revenue", ascending=False)

summary
```

**What to notice — there are three levels of mess here, and they need three different tools.**

| Mess | Example | Tool |
|---|---|---|
| spaces on the ends, wrong case | `"  Aisha Rahman "`, `"AISHA RAHMAN"` | `.str.strip().str.title()` |
| doubled spaces *inside* the text | `"Priya  Nair"` | `.str.replace(r"\s+", " ", regex=True)` |
| abbreviations | `"Raffles Pl."`, `"Holland V"` | a **mapping** — a business decision |

If you had used only `.str.strip().str.title()` you would have been left with both `"Priya  Nair"` and
`"Priya Nair"` — two managers where there is one, and a summary table that quietly splits her shifts in
half. Always print `.unique()` after a text clean-up. Knowing which tool a problem needs is most of the
skill.

</details>

---

### 🏆 Stretch Challenge (optional)

Do the same audit on the **real** file, `data/cafe_june_raw.csv`, but for one outlet only:

1. Filter to Marina Bay (all three spellings) *before* cleaning. How would you do that safely?
2. Clean it and compute its total June revenue.
3. Export the result to CSV, reload it, and confirm the total and the row count survive the trip.
4. What comes back as a different **type** than it went out as, and why?

<details>
<summary>✅ Solution</summary>

```python
raw = pd.read_csv("../data/cafe_june_raw.csv")

# 1. Filtering on messy text is a trap. `.str.strip().str.lower()` makes the test robust
#    rather than trying to list every spelling you can think of.
is_marina = raw["outlet"].str.strip().str.lower() == "marina bay"
marina = raw[is_marina].copy()
print("rows:", len(marina), "| spellings matched:", marina["outlet"].nunique())

# 2. Clean: text -> number, drop duplicates, mask the impossible, fill.
marina["revenue_sgd"] = pd.to_numeric(
    marina["revenue_raw"].str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce"
)
marina = marina.drop_duplicates()
marina["revenue_sgd"] = marina["revenue_sgd"].mask(
    (marina["revenue_sgd"] < 0) | (marina["revenue_sgd"] > 20000)
)
marina["revenue_sgd"] = marina["revenue_sgd"].fillna(marina["revenue_sgd"].median())
marina["date"] = pd.to_datetime(marina["date_text"], dayfirst=True)

print(f"Marina Bay, June 2025: ${marina['revenue_sgd'].sum():,.2f} across {len(marina)} shifts")

# 3. Round trip.
out = marina[["date", "daypart", "tickets", "revenue_sgd"]]
out.to_csv("../data/marina_june.csv", index=False)
back = pd.read_csv("../data/marina_june.csv")

print("rows back:", len(back), "| total back:", round(back["revenue_sgd"].sum(), 2))
print("date dtype out:", out["date"].dtype, "-> back:", back["date"].dtype)
```

**Expected:** 93 rows match, 90 survive de-duplication (30 days × 3 dayparts), and the total is about
**\$32,058**.

**Why that is not quite the class figure (\$32,452).** In class you filled the masked shifts with the
median of *all four cafés*; here you filled them with Marina Bay's own median, which is lower because
Marina Bay is the quietest outlet. Same data, same method, different grain — about \$400 apart. Neither
is wrong, but you have to be able to say which one you did. The outlet-specific median is the better
choice here, and worth remembering: **impute at the finest grain you can defend.**

**What comes back different:** the `date` column left as `datetime64` and returned as `object`
(text). CSV stores no type information, so every reader has to re-parse dates itself
(`parse_dates=["date"]`). The numbers survive; the *types* do not. This is the single most common
source of quiet breakage in CSV-based pipelines, and it is why databases and pickle files exist.

</details>

---

## 💬 Reflection (5 min)

In 2–3 sentences:

> In class, the raw June file claimed \$267,987 and the truth was \$174,753 — and a single mis-keyed
> shift caused most of the gap. Nothing errored, and nothing looked wrong. What one check will you run
> from now on, *first*, on every file you are given? Be specific enough to write it as a line of code.

---

## 📤 Share Your Work

Post your Challenge 3 summary table and your reflection in the **#peer-reviews** Discord channel. For
questions, post in **#questions**.
