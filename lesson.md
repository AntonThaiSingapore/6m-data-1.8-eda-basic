# 📚 Lesson 1.8: EDA Basic — Exploratory Data Analysis

## Session Overview

| | |
|---|---|
| **Duration** | 150 minutes (including 2 × 10-min breaks) |
| **Format** | Flipped Classroom + Guided Coding in Jupyter |
| **Tools** | VS Code + `pds` conda environment |
| **Notebook** | `notebooks/eda_basic.ipynb` |
| **Dataset** | `data/patients.csv` — one messy file, used from start to finish |

## Agenda

| Time | Part | Topic |
|------|------|-------|
| 0:00 – 0:05 | Setup | Imports, load `patients.csv`, the "why this matters" hook |
| 0:05 – 0:38 | Part 1 | Descriptive Statistics — the 5-move first look, then `.describe()` unpacked *(incl. 8-min Group Exercise 1)* |
| 0:38 – 0:48 | ☕ | **Break** |
| 0:48 – 1:30 | Part 2 | Data Quality — missing values, duplicates, impossible values *(incl. 12-min Group Exercise 2)* |
| 1:30 – 1:40 | ☕ | **Break** |
| 1:40 – 2:15 | Part 3 | Transformation — mapping, labels, strings/regex, categories, dates, grouping *(incl. 10-min Group Exercise 3)* |
| 2:15 – 2:30 | Part 4 | Reading & writing — CSV, JSON, Excel, databases |

**The notebook follows the four learning outcomes in order.** Reading files is deliberately *last*:
nothing in Parts 1–3 depends on file I/O, so learners meet cleaning before parsing.

### Instructor notes

- **Do not skip the hook** in Part 1. Nine wards for a four-ward hospital, and a 150-year-old
  patient. It costs 2 minutes and pays for the rest of the session.
- **Each section is spine-then-drills.** The spine block works on `patients` / `clean` and carries
  the narrative; the small hand-built tables that follow are mechanics. If you are running late,
  cut drills — never the spine.
- **The payoff is section 3.5** — the `groupby` ward summary, shown beside the same summary on the
  dirty data (where the average stay is negative).
- **Breaks are load-bearing**, not padding. Both break cells state where the class is and what is next.
- Deep dives (categorical internals, `.cat`, awkward CSV parsing, pickle) live in `reference.md`.
  Point learners there rather than teaching them live.
- Group exercises fade: (a) is worked or blank-filling, later parts are from scratch. Expected
  outputs are stated, so groups self-check without waiting for you.

## 🎯 Learning Objectives

By the end of this session, you will be able to:

1. Summarise a dataset using descriptive statistics and identify its shape, data types, and distributions.
2. Handle missing values, duplicates, and outliers using appropriate Pandas methods.
3. Transform data through type conversion, string cleaning, and categorical encoding.
4. Read and write data across multiple file formats (CSV, JSON, Excel, databases).

---

## Before You Start

**Have you completed the pre-class reading?**
- ✓ Understand what EDA is and why it matters
- ✓ Review basic statistics concepts (mean, median, standard deviation)
- ✓ Familiar with regex basics
- ✓ `pds` conda environment is set up

Open the notebook in VSCode by double-clicking on `notebooks/eda_basic.ipynb`, then select the `pds` conda environment for the kernel.

---

## 🏃 Part 1: Descriptive Statistics (33 min)

Open the notebook and follow along with **Part 1**.

This part covers the "Health Check" — understanding what you have before you analyse it.

**1.1 — the five-move first look**, in this order, every time:

| Move | Question it answers |
|---|---|
| `.head()` | What do the rows actually look like? |
| `.shape` | How big is it? |
| `.info()` | What type is each column, and where are the holes? |
| `.dtypes` | Is anything stored as the wrong type? |
| `.describe()` | Are the numbers plausible? |

`.describe(include="object")` for the text columns — that is where spelling variants show up.

**1.2 — the same statistics unpacked** on a tiny table: reductions (`.sum()`, `.mean()`),
`skipna`, `.idxmax()` / `.idxmin()`, `.cumsum()`, `.unique()`, `.value_counts()`.

> The ritual output *is* the Part 2 to-do list. Have the class write down the five problems it
> finds before the break.

---

## 🏃 Part 2: Data Quality (42 min)

Continue in the notebook with **Part 2**. Every fix follows the same four beats:
**find it → decide → apply → verify.** This is the habit worth more than any single method.

**Key topics:**
- Missing values — `isna()`, `dropna()` (`how`, `thresh`, `axis`), `fillna()` (scalar, per-column, `bfill`, median)
- Duplicates — `duplicated()`, `drop_duplicates()` (`subset`, `keep`)
- Impossible values — boolean filtering, `.mask()`, sentinel codes like `-999`, capping vs marking missing

> The decision table in 2.1 is the teaching moment: `contact` stays NaN, `blood_type` becomes
> `"Unknown"`, `days_admitted` gets the median. Three holes, three different right answers.
>
> **Order matters** and the notebook makes it visible: the `-999` sentinels must go *before*
> the median is computed, or the median itself is poisoned.

---

## 🏃 Part 3: Data Transformation (35 min)

Continue in the notebook with **Part 3**.

**Key topics:**
- 3.1 Mapping — `.map()` with a dictionary, `.replace()`; nine ward spellings → four wards
- 3.2 Renaming axis labels — `.rename()`, `.index.map()`
- 3.3 Strings & regex — `.str.strip()`, `.str.title()`, `.str.split()`; regex built up in three steps
- 3.4 Categorical encoding — `astype('category')`, `pd.cut()` bands, `pd.get_dummies()`
- 3.5 Type conversion & grouping — `pd.to_datetime()`, `.dt`, `groupby().agg()`

> `.map()` silently turns unlisted values into NaN; `.replace()` leaves them alone. Make the class
> say which behaviour they want before they pick.
>
> 3.5 is the payoff: a per-ward summary table. Run the same `groupby` on the raw data to show the
> negative average stay. `groupby` returns in Lesson 1.9 in depth — this is the first taste.

---

## 🏃 Part 4: Reading and Writing Data (15 min)

Continue in the notebook with **Part 4**.

**Key topics:**
- CSV in — `read_csv` with `header`, `names`, `index_col`, `na_values`
- CSV out — `to_csv`, and why you almost always want `index=False`
- JSON — `to_json(orient="records")`, `read_json`
- Excel — `pd.ExcelFile`, `.parse()`, `read_excel`, `to_excel`
- Databases — `sqlalchemy.create_engine`, `read_sql`, `to_sql`

> The section closes by saving `clean` to `data/patients_clean.csv` — the session's actual output.
> Point out that CSV and JSON both forget dtypes on the way out; databases and pickle do not.

---

## 🎯 Wrap-Up

**Key Takeaways:**
1. Always run the five-move first look on a new dataset before any analysis — head, shape, info, dtypes, describe.
2. Data cleaning decisions (fill vs. drop vs. cap vs. mark missing) depend on what the value *means*, not on what is convenient.
3. Order of operations matters: remove sentinels before you compute the statistic you impute with.
4. Type conversion and string cleaning are foundational — messy types cause silent errors downstream.
5. A clean table is not the goal; a *trustworthy answer* is. Section 3.5 is what all the cleaning was for.

**Next Steps:**
- Complete the [Assignment](./assignment.md) — EDA practice challenges: clean and analyse a messy dataset.
- Next lesson: Lesson 1.9 covers EDA Advanced — time series, merging datasets, GroupBy, and pivot tables.
