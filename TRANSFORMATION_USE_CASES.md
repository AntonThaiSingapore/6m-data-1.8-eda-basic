# Data Transformation Use Cases Reference

This document provides practical use cases and real-world scenarios for the data transformation techniques covered in the EDA Basic lesson.

---

## 1. Summarizing and Computing Descriptive Statistics

### When to Use
- **Initial data exploration**: Get a quick overview of your dataset's distribution
- **Data quality checks**: Identify potential issues through summary statistics
- **Feature engineering**: Create aggregate features for machine learning models
- **Reporting**: Generate summary metrics for stakeholders

### Real-World Scenarios

**Business Analytics**
```python
# Monthly sales analysis
sales_data.groupby('month')['revenue'].agg(['sum', 'mean', 'count'])

# Find best-performing products
products['sales'].idxmax()  # Product ID with highest sales
```

**Scientific Research**
```python
# Summarize experimental results across trials
experiment_df.describe()  # Get statistical overview

# Identify which trial had the maximum effect
results['effect_size'].idxmax()
```

**Financial Analysis**
```python
# Portfolio performance metrics
portfolio['returns'].cumsum()  # Cumulative returns over time
portfolio.groupby('asset_class')['value'].sum()  # Total value by asset class
```

### Key Methods
- `sum()`, `mean()`, `describe()` - Understand distributions
- `idxmax()`, `idxmin()` - Find locations of extremes
- `value_counts()` - Frequency analysis for categorical data
- `cumsum()` - Track accumulation over time

---

## 2. Handling Missing Data

### When to Use
- **Data cleaning**: Before analysis or modeling
- **Data quality assessment**: Understand completeness of your dataset
- **Imputation strategies**: Fill missing values based on domain knowledge
- **Feature selection**: Drop columns/rows with excessive missing data

### Real-World Scenarios

**Healthcare Data**
```python
# Patient records often have missing test results
patient_data.dropna(subset=['critical_vitals'])  # Keep only complete critical data
patient_data['blood_pressure'].ffill()  # Use last known value
```

**Survey Data**
```python
# Respondents skip questions
survey.dropna(thresh=10)  # Keep responses with at least 10 answers
survey.fillna({'age': survey['age'].mean()})  # Impute age with average
```

**Sensor Data**
```python
# IoT sensors may fail to report
sensor_data.fillna(method='bfill', limit=3)  # Fill short gaps with next reading
sensor_data.dropna(how='all')  # Remove completely dead sensor periods
```

**E-commerce**
```python
# Optional product attributes
products.fillna({'discount': 0})  # No discount means 0%
products['rating'].fillna(products['rating'].mean())  # Use average rating
```

### Key Methods
- `isna()`, `notna()` - Identify missing values
- `dropna()` - Remove incomplete data (use `thresh` for minimum data requirements)
- `fillna()` - Impute with constants, statistics, or forward/backward fill
- Consider: Is data missing at random? Does missingness carry meaning?

---

## 3. Handling Duplicates

### When to Use
- **Data integrity**: Ensure uniqueness in datasets
- **Deduplication**: Remove redundant records after data merges
- **Data validation**: Identify unexpected duplicates that may indicate errors
- **Unique constraint enforcement**: Before database insertion

### Real-World Scenarios

**Customer Databases**
```python
# Remove duplicate customer registrations
customers.drop_duplicates(subset=['email'], keep='last')  # Keep most recent entry
```

**Transaction Logs**
```python
# Identify duplicate transactions (possible system errors)
duplicates = transactions.duplicated(subset=['transaction_id', 'timestamp'])
suspicious = transactions[duplicates]  # Investigate these
```

**Web Scraping**
```python
# Remove duplicate articles scraped from multiple pages
articles.drop_duplicates(subset=['title', 'url'], keep='first')
```

**Data Warehousing**
```python
# ETL pipeline - ensure no duplicate records after merge
merged_data.drop_duplicates()  # Check all columns
merged_data.drop_duplicates(subset=['id'], keep='last')  # Keep latest version
```

### Key Methods
- `duplicated()` - Find duplicate rows
- `drop_duplicates()` - Remove duplicates (control which to keep with `keep` parameter)
- Use `subset` parameter to check specific columns for uniqueness

---

## 4. Transforming Data with Mapping and Replacement

### When to Use
- **Categorical recoding**: Transform categories into new groupings
- **Data standardization**: Convert codes to meaningful labels
- **Feature engineering**: Create derived features from existing ones
- **Data cleaning**: Replace error codes or sentinel values

### Real-World Scenarios

**Data Standardization**
```python
# Standardize country codes
country_mapping = {'US': 'United States', 'UK': 'United Kingdom', 'UAE': 'United Arab Emirates'}
df['country_full'] = df['country_code'].map(country_mapping)
```

**Error Code Handling**
```python
# Replace error/missing value codes with NaN
sensor_readings.replace([-999, -9999], np.nan)  # Common missing value sentinels
```

**Feature Engineering**
```python
# Create risk categories from credit scores
risk_mapping = lambda x: 'High' if x < 600 else ('Medium' if x < 700 else 'Low')
customers['risk_level'] = customers['credit_score'].map(risk_mapping)
```

**Survey Response Recoding**
```python
# Convert Likert scale to numeric
response_map = {'Strongly Disagree': 1, 'Disagree': 2, 'Neutral': 3,
                'Agree': 4, 'Strongly Agree': 5}
survey['satisfaction_score'] = survey['satisfaction'].map(response_map)
```

### Key Methods
- `map()` - Apply function or dictionary to transform values
- `replace()` - Substitute specific values with new ones
- Use dictionaries for categorical mappings, functions for calculated transformations

---

## 5. Renaming Axis Indexes

### When to Use
- **Code readability**: Make column/index names more descriptive
- **Data preparation**: Standardize naming conventions across datasets
- **Database compatibility**: Rename columns to match schema requirements
- **API integration**: Transform names to match expected formats

### Real-World Scenarios

**Data Integration**
```python
# Standardize column names from different data sources
df1.rename(columns=str.lower)  # All lowercase
df2.rename(columns=lambda x: x.replace(' ', '_'))  # Replace spaces
```

**Database Preparation**
```python
# Convert to database-friendly names
df.rename(columns={'First Name': 'first_name',
                   'Last Name': 'last_name',
                   'Email Address': 'email'})
```

**Report Generation**
```python
# Make headers more presentable
report.rename(columns=str.title)  # Title Case
report.rename(index=lambda x: f"Quarter {x}")  # Add context to index
```

**API Response Transformation**
```python
# Match expected API field names
api_data.rename(columns={'userId': 'user_id', 'productId': 'product_id'})
```

### Key Methods
- `rename()` - Transform axis labels with functions or dictionaries
- `index.map()` - Apply function to index
- Use functions for systematic transformations, dictionaries for selective renaming

---

## 6. Handling Outliers

### When to Use
- **Statistical modeling**: Remove extreme values that violate model assumptions
- **Data quality checks**: Identify potentially erroneous data points
- **Robust analysis**: Prevent outliers from skewing results
- **Business rules enforcement**: Cap values at reasonable limits

### Real-World Scenarios

**Financial Data**
```python
# Cap extreme stock returns for risk calculations
returns = portfolio['daily_return']
returns[returns.abs() > 3*returns.std()] = np.sign(returns) * 3*returns.std()
```

**E-commerce Pricing**
```python
# Identify pricing errors
products[products['price'] > 10000]  # Flag suspiciously high prices
products = products[products['price'] < 10000]  # Remove outliers
```

**Sensor Calibration**
```python
# Filter out sensor malfunctions
valid_readings = sensor_data[(sensor_data['temperature'] > -50) &
                              (sensor_data['temperature'] < 100)]
```

**Marketing Analytics**
```python
# Remove bot traffic from user engagement metrics
# Cap session duration at 99th percentile
cap = user_sessions['duration'].quantile(0.99)
user_sessions.loc[user_sessions['duration'] > cap, 'duration'] = cap
```

### Key Methods
- `abs()` - Get absolute values for threshold comparison
- Boolean indexing - Filter or cap outliers
- `describe()` - Understand distribution before deciding on thresholds
- Consider domain knowledge: Are these true outliers or important edge cases?

---

## 7. Permutation and Random Sampling

### When to Use
- **Train-test splits**: Create random subsets for machine learning
- **Cross-validation**: Generate random folds for model validation
- **A/B testing**: Randomly assign users to test groups
- **Data auditing**: Sample large datasets for manual review
- **Bootstrap analysis**: Sample with replacement for statistical inference

### Real-World Scenarios

**Machine Learning**
```python
# Create train-test split
shuffled = df.sample(frac=1, random_state=42)  # Shuffle entire dataset
train = shuffled[:int(0.8*len(df))]
test = shuffled[int(0.8*len(df)):]
```

**A/B Testing**
```python
# Randomly assign users to control/treatment groups
users['group'] = np.random.permutation(['A', 'B'] * (len(users)//2))
```

**Data Auditing**
```python
# Sample 100 transactions for manual review
audit_sample = transactions.sample(n=100, random_state=123)
```

**Bootstrap Analysis**
```python
# Generate bootstrap samples for confidence intervals
bootstrap_sample = data.sample(n=len(data), replace=True)
```

**Survey Sampling**
```python
# Get representative sample of 10% of population
survey_sample = population.sample(frac=0.1, random_state=42)
```

### Key Methods
- `sample()` - Random sampling with/without replacement
- `np.random.permutation()` - Generate random orderings
- Use `random_state` for reproducibility
- `frac` for percentage-based sampling, `n` for fixed counts

---

## 8. String Manipulation

### When to Use
- **Text data cleaning**: Extract, standardize, or validate text fields
- **Pattern matching**: Find records matching specific patterns
- **Data extraction**: Parse structured information from text
- **Feature engineering**: Create features from text data
- **Data validation**: Check format compliance (emails, phone numbers, etc.)

### Real-World Scenarios

**Email Validation**
```python
# Extract emails from text fields
emails = contacts['text'].str.extract(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')

# Filter to specific email domains
gmail_users = users[users['email'].str.contains('gmail.com')]
```

**Name Standardization**
```python
# Standardize name formats
customers['name'] = customers['name'].str.strip().str.title()
customers['first_name'] = customers['name'].str.split().str[0]
```

**URL Parsing**
```python
# Extract domain from URLs
websites['domain'] = websites['url'].str.extract(r'https?://([^/]+)')
```

**Product Code Extraction**
```python
# Extract product codes from descriptions
products['code'] = products['description'].str.extract(r'SKU: ([A-Z0-9]{8})')
```

**Text Classification**
```python
# Flag records containing keywords
complaints['urgent'] = complaints['message'].str.contains('urgent|emergency', case=False)
```

### Key Methods
- `str.contains()` - Search for patterns
- `str.extract()` - Extract regex groups into columns
- `str[]` - String slicing
- All operations handle NaN values gracefully
- Use `astype('string')` for better NA handling

---

## 9. Categorical Data

### When to Use
- **Memory efficiency**: Convert repeated strings to categorical dtype
- **Data binning**: Group continuous variables into categories
- **Ordered categories**: Work with ordinal data (e.g., Small/Medium/Large)
- **Machine learning**: Create dummy variables for models
- **Dimension tables**: Create efficient lookup tables with integer keys

### 9.1 Categorical Data Types

**When to Use**
```python
# Memory efficiency for large datasets with repeated values
df['country'] = df['country'].astype('category')  # Save memory

# Ordered categories for sorting/comparison
df['size'] = pd.Categorical(df['size'],
                             categories=['Small', 'Medium', 'Large'],
                             ordered=True)
```

### 9.2 Binning Continuous Data

**When to Use**

**Age Grouping (Demographics)**
```python
# Create age brackets for analysis
age_bins = [0, 18, 25, 35, 50, 65, 100]
age_labels = ['Child', 'Young Adult', 'Adult', 'Middle Age', 'Senior', 'Elderly']
census['age_group'] = pd.cut(census['age'], bins=age_bins, labels=age_labels)
```

**Price Segmentation**
```python
# Create price tiers
products['price_tier'] = pd.cut(products['price'],
                                bins=[0, 10, 50, 200, 1000],
                                labels=['Budget', 'Economy', 'Premium', 'Luxury'])
```

**Quantile-Based Binning**
```python
# Create equal-sized customer segments by spending
customers['spending_quartile'] = pd.qcut(customers['total_spent'],
                                         q=4,
                                         labels=['Q1', 'Q2', 'Q3', 'Q4'])
```

**Risk Scoring**
```python
# Bin credit scores into risk categories
loans['risk'] = pd.cut(loans['credit_score'],
                      bins=[300, 600, 700, 750, 850],
                      labels=['High Risk', 'Medium Risk', 'Low Risk', 'Very Low Risk'])
```

### 9.3 Dummy Variables

**When to Use**

**Machine Learning Preprocessing**
```python
# Convert categorical variables to numeric for ML models
dummies = pd.get_dummies(df['category'], prefix='cat')
df_encoded = pd.concat([df, dummies], axis=1)
```

**Regression Analysis**
```python
# Create indicator variables for categorical predictors
region_dummies = pd.get_dummies(sales['region'], prefix='region', drop_first=True)
```

**A/B Test Analysis**
```python
# Create binary features from test groups
test_dummies = pd.get_dummies(users['test_group'], prefix='group')
```

### Key Methods
- `astype('category')` - Convert to categorical for memory efficiency
- `pd.cut()` - Bin by equal widths (use for known boundaries)
- `pd.qcut()` - Bin by quantiles (use for equal-sized groups)
- `pd.get_dummies()` - Create indicator variables for ML
- `.cat` accessor for category-specific operations

---

## 10. Reading and Writing Data

### When to Use Different Formats

### 10.1 CSV/Text Files

**When to Use**
- Universal compatibility across tools and languages
- Human-readable format for inspection
- Sharing data with non-technical stakeholders
- Version control friendly (text-based)
- Large datasets that don't fit in memory (read in chunks)

**Real-World Scenarios**
```python
# Export for Excel/BI tools
report.to_csv('monthly_report.csv', index=False)

# Read data with custom missing value codes
survey = pd.read_csv('survey.csv', na_values=['N/A', 'Missing', '-'])

# Handle messy data with custom delimiters
log_data = pd.read_csv('server.log', sep=r'\s+', header=None, names=['timestamp', 'level', 'message'])

# Skip metadata rows
data = pd.read_csv('export.csv', skiprows=3)  # Skip first 3 header rows
```

### 10.2 Excel Files

**When to Use**
- Working with business users who prefer Excel
- Multiple related tables in one file (sheets)
- Preserving formatting/formulas for business reporting
- Small to medium datasets (< 1M rows)

**Real-World Scenarios**
```python
# Read financial reports with multiple sheets
excel_file = pd.ExcelFile('quarterly_report.xlsx')
revenue = excel_file.parse('Revenue')
expenses = excel_file.parse('Expenses')

# Create multi-sheet report for stakeholders
with pd.ExcelWriter('summary.xlsx') as writer:
    sales_summary.to_excel(writer, sheet_name='Sales')
    customer_summary.to_excel(writer, sheet_name='Customers')
    product_summary.to_excel(writer, sheet_name='Products')
```

### 10.3 Pickle Files

**When to Use**
- Python-specific workflows (no cross-language needs)
- Preserving exact DataFrame structure (dtypes, index, etc.)
- Intermediate results in data pipelines
- Fast serialization/deserialization
- Complex Python objects

**Real-World Scenarios**
```python
# Save preprocessed data for machine learning
processed_features.to_pickle('features_v2.pkl')

# Cache expensive computations
if not os.path.exists('aggregated_cache.pkl'):
    result = expensive_aggregation(data)
    result.to_pickle('aggregated_cache.pkl')
else:
    result = pd.read_pickle('aggregated_cache.pkl')
```

### 10.4 SQL Databases

**When to Use**
- Large datasets requiring efficient querying
- Concurrent access by multiple users/applications
- Data integrity constraints (foreign keys, unique constraints)
- Incremental updates (not rewriting entire dataset)
- Integration with web applications

**Real-World Scenarios**
```python
# Connect to database
engine = create_engine('duckdb:///analytics.db')

# Load reference data for analysis
products = pd.read_sql('products', engine)

# Query specific subset
high_value = pd.read_sql('SELECT * FROM customers WHERE lifetime_value > 1000', engine)

# Write processed results back
new_customers.to_sql('customers', engine, if_exists='append')

# Create analytical tables
monthly_summary.to_sql('monthly_metrics', engine, if_exists='replace')
```

### Format Selection Guide

| Format | Best For | Avoid When |
|--------|----------|------------|
| **CSV** | Sharing, compatibility, version control | Complex data types, very large files |
| **Excel** | Business reports, multiple related tables | Large data (>1M rows), automation |
| **Pickle** | Python-only, caching, complex objects | Cross-language needs, long-term storage |
| **SQL** | Large data, queries, multi-user access | Simple one-time analysis, very wide tables |

### Key Methods
- `read_csv()`, `to_csv()` - Universal text format
- `read_excel()`, `to_excel()` - Multi-sheet business data
- `read_pickle()`, `to_pickle()` - Fast Python-specific storage
- `read_sql()`, `to_sql()` - Database integration

---

## General Principles for Choosing Transformations

### 1. Data Exploration Phase
- Start with `describe()`, `value_counts()`, `isna().sum()`
- Use `sample()` to inspect random rows
- Check for duplicates with `duplicated()`

### 2. Data Cleaning Phase
- Handle missing values: `dropna()` or `fillna()`
- Remove/investigate duplicates: `drop_duplicates()`
- Replace error codes: `replace()`
- Handle outliers: Boolean indexing or capping

### 3. Data Transformation Phase
- Recode categories: `map()`, `replace()`
- Bin continuous variables: `cut()`, `qcut()`
- Extract from strings: `str.extract()`, `str.contains()`
- Rename for clarity: `rename()`

### 4. Data Preparation for Analysis
- Create dummy variables: `get_dummies()`
- Sample for testing: `sample()`
- Convert types: `astype('category')`, `astype('string')`
- Aggregate: `sum()`, `mean()`, `groupby()`

### 5. Data Persistence
- Choose format based on use case (see format guide above)
- Consider audience, size, and downstream tools

---

## Tips for Students

1. **Chain operations carefully**: Use method chaining for readable pipelines, but break into steps for debugging

2. **Always inspect results**: Use `head()`, `tail()`, `sample()` after transformations to verify

3. **Handle missing values consciously**: Understand the default behavior (most methods skip NaN by default)

4. **Use appropriate dtypes**: Categorical for repeated strings, string for text operations, datetime for dates

5. **Document your assumptions**: Comment why you chose specific thresholds, fill methods, or binning strategies

6. **Preserve original data**: Create copies before transformations for comparison and debugging

7. **Consider computational efficiency**: For large datasets, categorical dtypes and appropriate file formats matter

8. **Validate transformations**: Check value counts, ranges, and summary statistics after major changes
