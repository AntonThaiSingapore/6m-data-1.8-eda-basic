# Reference

- [Interactive EDA Concept Map](https://su-ntu-ctp.github.io/6m-data-1.8-eda-basic/)
- [Beginner's Guide to Statistics](https://www.analyticsvidhya.com/blog/2021/08/a-beginners-guide-to-statistics-for-machine-learning/)
- [Introduction to Regular Expressions in Python](https://developers.google.com/edu/python/regular-expressions)
- [Regex Cheatsheet](https://www.dataquest.io/blog/regex-cheatsheet/)
- [Pandas String Cheatsheet](https://www.datacamp.com/cheat-sheet/text-data-in-python-cheat-sheet)
- [Importing Data Cheatsheet](https://www.datacamp.com/cheat-sheet/importing-data-in-python-cheat-sheet)

---

## 📦 Moved out of the lesson notebook

Everything below was in the notebook and is still correct — it was moved here to keep the
150-minute session focused on the four learning outcomes. Copy any block into a notebook cell
to run it. Variable names match the notebook's, so run the block above it first where relevant.

### Categorical internals — codes and the lookup table

How pandas stores a categorical: a list of small integer codes plus one lookup table of labels. Useful to know, not needed in order to use `astype('category')`.

**Under the hood:** Categoricals are stored as integers referencing a dictionary of values.

```python
# 👉 Under the hood a categorical is two pieces: a list of small integer codes...
#    ...and a lookup table of the actual labels.
fruit_s = pd.Series([0, 1, 0, 0] * 2)

dim = pd.Series(["apple", "orange"])

fruit_s
```

```python
# 👉 The lookup table: position 0 is 'apple', position 1 is 'orange'.
dim
```

```python
# 👉 `.take()` reads the codes as positions in the lookup table and rebuilds the text.
#    That is the whole trick -- store 0s and 1s, keep the words only once.
dim.take(fruit_s)
```

The values for `fruit_cat` are now an instance of `pandas.Categorical`, which you can access via the `.array` attribute:

```python
# 👉 `.array` exposes the underlying storage object so we can look inside it.
c = fruit_cat.array

type(c)
```

```python
# 👉 The lookup table of distinct labels.
c.categories
```

```python
# 👉 The integer codes -- one small number per row instead of a full string.
c.codes
```

```python
# 👉 Pair each code with its label to see the mapping. `enumerate` numbers the items 0, 1, 2...
dict(enumerate(c.categories))
```

---

### Building categoricals by hand (`from_codes`, `ordered=`)

Construct a categorical from codes and labels yourself, and give the categories a rank so sorting and comparisons follow it.

**Creating from Codes:**

```python
# 👉 You can also build a categorical from scratch: give the labels and the codes yourself.
categories = ['foo', 'bar', 'baz']
codes = [0, 1, 2, 0, 0, 1]

my_cats = pd.Categorical.from_codes(codes, categories)

my_cats
```

**Ordered Categoricals:** Useful for Likert scales or sizes (Small < Medium < Large).

```python
# 👉 `ordered=True` records that the categories have a rank (foo < bar < baz).
#    Use this for sizes or Likert scales, so comparisons and sorting behave sensibly.
ordered_cats = pd.Categorical.from_codes(codes, categories, ordered=True)

ordered_cats
```

---

### The `.cat` accessor — inspecting and editing categories

`.cat` is to categoricals what `.str` is to text. Most useful when you must declare categories that no row currently uses.

**Categorical Methods (.cat):**

```python
# 👉 A categorical Series to demo the `.cat` toolbox.
s = pd.Series(['a', 'b', 'c', 'd'] * 2)
cat_s = s.astype('category')

cat_s
```

```python
# 👉 `.cat` is the accessor for category-specific tools, the way `.str` is for text.
#    Here: the integer code behind each row.
cat_s.cat.codes
```

```python
# 👉 The labels those codes point to.
cat_s.cat.categories
```

Modifying categories:

```python
# 👉 Declare that a category 'e' exists even though no row uses it. Useful when you know
#    the full set of valid values in advance.
actual_categories = ['a', 'b', 'c', 'd', 'e']
cat_s2 = cat_s.cat.set_categories(actual_categories)

cat_s2
```

```python
# 👉 Counting the original: four categories.
cat_s.value_counts()
```

```python
# 👉 Counting the version with the extra category: 'e' appears with a count of 0.
#    Handy -- it makes the missing group visible instead of silently absent.
cat_s2.value_counts()
```

```python
# 👉 The reverse operation: throw away categories that no row actually uses.
cat_s2.cat.remove_unused_categories()
```

---

### Awkward CSV files — irregular separators and junk rows

Reach for these when a file is not comma-separated, or has comments and metadata above the real data.

Irregular/regex separators are an edge case — most files you meet are plain CSVs.

**Irregular Separators:** Sometimes data isn't separated by commas. It might be tabs, spaces, or a variable amount of whitespace. We can use Regular Expressions (Regex) to handle this.

```python
# 👉 This file lines things up with spaces, not commas.
# Inspect a file with messy whitespace
!cat ../data/ex3.txt
```

```python
# 👉 `sep=` tells pandas what separates the values. `\s+` is a regex meaning
#    'one or more spaces', which handles the uneven gaps.
# sep="\s+" is a regex that means "one or more whitespace characters"
result = pd.read_csv("../data/ex3.txt", sep="\s+")

result
```

**Skipping Rows:** Sometimes files contain comments or metadata at the top that we want to ignore.

```python
# 👉 This file has comment lines mixed in with the data.
!cat ../data/ex4.csv
```

```python
# 👉 `skiprows=` throws away the given line numbers before parsing. Counting starts at 0.
# Skip specific rows by index (0, 2, and 3 here) to get to the clean data
pd.read_csv("../data/ex4.csv", skiprows=[0, 2, 3])
```

---

### Pickle — Python's own binary save format

Fast, but only Python can read it and only similar versions. Fine for a scratch file, wrong for sharing data with anyone else.

Binary/pickle files are a niche topic. Read this only when you actually need to save Python objects.

4.4: Binary files (Pickle)

`pickle` is Python's native serialization format. Good for short-term storage, but not for sharing data between different languages.

```python
# 👉 Pickle is Python's own save format: fast, but only Python can read it, and only the
#    same-ish version. Good for temporary files, bad for sharing.
result.to_pickle('../data/out.pkl')
```

```python
# 👉 Read it straight back. The DataFrame comes back exactly as it was.
data = pd.read_pickle('../data/out.pkl')

data
```
