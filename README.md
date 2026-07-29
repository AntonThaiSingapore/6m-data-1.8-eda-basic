# 📚 Lesson 1.8: EDA Basic — Exploratory Data Analysis

**Theme:** The Health Check — inspecting, cleaning, and understanding your data

---

## 📅 Lesson Overview

**Total: 150 minutes**, including 2 × 10-minute breaks and one group exercise per section.

| Section | Duration | Topic / Activity |
|---------|----------|-----------------|
| Setup | 5 min | Imports, load `data/patients.csv`, the "why this matters" hook |
| **Part 1: Descriptive Statistics** | 33 min | The 5-move first look (`.head`, `.shape`, `.info`, `.dtypes`, `.describe`); `.value_counts()`; reductions |
| ☕ Break | 10 min | |
| **Part 2: Data Quality** | 42 min | Missing values; duplicates; impossible values & sentinels; fill vs drop vs cap |
| ☕ Break | 10 min | |
| **Part 3: Data Transformation** | 35 min | Mapping; axis labels; strings & regex; categories & binning; dates; `groupby` |
| **Part 4: Reading & Writing** | 15 min | CSV, JSON, Excel, databases |

**One dataset, start to finish.** The whole session works on `data/patients.csv` — 38 rows of
synthetic hospital records with missing values, duplicates, impossible ages, sentinel codes, and
nine spellings of four ward names. Each section improves the same `clean` table; Part 4 saves it as
`data/patients_clean.csv`. Small hand-built tables appear alongside as *drills* that isolate one
method at a time.

---

## 🎯 Learning Objectives

By the end of this lesson, you will be able to:

1. **Summarise** a dataset using descriptive statistics and identify its shape, data types, and distributions.
2. **Handle** missing values, duplicates, and outliers using appropriate Pandas methods.
3. **Transform** data through type conversion, string cleaning, and categorical encoding.
4. **Read and write** data across multiple file formats (CSV, JSON, Excel, databases).

---

## 📂 Course Materials

| Material | Description | Est. Time |
|----------|-------------|-----------|
| [Pre-Class](./pre-class.md) | What EDA is; statistics concepts; regex intro; environment setup | 30–45 min |
| [Lesson Plan](./lesson.md) | Instructor guide: agenda, timings, teaching notes | 150 min |
| [Assignment](./assignment.md) | EDA practice challenges — clean and analyse a messy dataset | 45–60 min |
| [Reference](./reference.md) | Pandas EDA cheat sheet; regex quick reference; deep dives moved out of the notebook | As needed |

---

## 🛠️ Tools & Setup

- **[VS Code](https://code.visualstudio.com)** + Python + Jupyter extensions *(recommended)*.
- **[Google Colab](https://colab.research.google.com)** *(alternative)*.
- **Notebook:** `notebooks/eda_basic.ipynb` — select the `pds` kernel in VS Code.
- **Environment:** `conda env create -f environment.yml` then `conda activate pds`.
- **Dataset:** `data/patients.csv` is the lesson spine; `data/` also holds the smaller example files
  used in Part 4 and the resale-flat workbook and DuckDB database.
- **Pandas version:** the notebook targets the `pds` environment (pandas 1.5). It avoids APIs removed
  in pandas 2.x, so it also runs on Google Colab.
