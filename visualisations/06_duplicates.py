"""
Visualization for Handling Duplicates
Shows how to identify and remove duplicate data
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Create sample data with duplicates
np.random.seed(42)
data = pd.DataFrame({
    'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar', 'baz', 'baz'],
    'B': [1, 1, 2, 2, 3, 3, 4, 4],
    'C': [10, 10, 20, 20, 30, 30, 40, 40],
    'D': np.random.randn(8)
})

# Create a larger dataset for better visualization
categories = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
regions = ['North', 'South', 'East', 'West']

large_data = pd.DataFrame({
    'Product': np.random.choice(categories, 300),
    'Region': np.random.choice(regions, 300),
    'Sales': np.random.randint(100, 1000, 300),
    'Date': pd.date_range('2024-01-01', periods=300, freq='D')[:300]
})

# Introduce duplicates
duplicates_idx = np.random.choice(large_data.index, 50, replace=False)
for idx in duplicates_idx:
    dup_row = large_data.iloc[idx:idx+1]
    large_data = pd.concat([large_data, dup_row], ignore_index=True)

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

fig.suptitle('Handling Duplicates in Data', fontsize=16, fontweight='bold')

# 1. Dataset size comparison
ax1 = fig.add_subplot(gs[0, 0])
categories_bar = ['Original\nData', 'After\ndrop_duplicates()', 'Duplicates\nOnly']
counts = [len(large_data),
         len(large_data.drop_duplicates()),
         len(large_data) - len(large_data.drop_duplicates())]
colors = ['#2196F3', '#4CAF50', '#F44336']
bars = ax1.bar(categories_bar, counts, color=colors, edgecolor='black', alpha=0.7)

ax1.set_title('Dataset Size - Before & After', fontweight='bold')
ax1.set_ylabel('Number of Rows')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}\nrows',
            ha='center', va='bottom', fontsize=9)

# 2. Duplicate rows highlighted
ax2 = fig.add_subplot(gs[0, 1])
is_dup = large_data.duplicated(keep=False)
dup_counts = is_dup.value_counts()
colors_pie = ['#4CAF50', '#F44336']
explode = (0, 0.1)
wedges, texts, autotexts = ax2.pie(dup_counts.values,
                                     labels=['Unique', 'Duplicate'],
                                     autopct='%1.1f%%',
                                     colors=colors_pie,
                                     explode=explode,
                                     startangle=90)
ax2.set_title('Proportion of Duplicate Rows', fontweight='bold')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 3. Duplicates by column combinations
ax3 = fig.add_subplot(gs[0, 2])
# Count duplicates by different column combinations
dup_all = large_data.duplicated().sum()
dup_product = large_data.duplicated(subset=['Product']).sum()
dup_region = large_data.duplicated(subset=['Region']).sum()
dup_prod_reg = large_data.duplicated(subset=['Product', 'Region']).sum()

labels = ['All\nColumns', 'Product\nOnly', 'Region\nOnly', 'Product +\nRegion']
values = [dup_all, dup_product, dup_region, dup_prod_reg]
colors_bar = ['#F44336', '#FF9800', '#FFC107', '#FF5722']
bars = ax3.bar(labels, values, color=colors_bar, edgecolor='black', alpha=0.7)

ax3.set_title('Duplicates by Column Subset', fontweight='bold')
ax3.set_ylabel('Number of Duplicates')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(val)}',
            ha='center', va='bottom', fontsize=9)

# 4. Duplicate distribution across Product
ax4 = fig.add_subplot(gs[1, 0])
product_dups = large_data[large_data.duplicated(keep=False)].groupby('Product').size()
bars = ax4.barh(product_dups.index, product_dups.values,
               color='salmon', edgecolor='black', alpha=0.7)
ax4.set_title('Duplicates by Product', fontweight='bold')
ax4.set_xlabel('Number of Duplicate Rows')
ax4.set_ylabel('Product')
ax4.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, product_dups.values)):
    ax4.text(val, i, f' {int(val)}', va='center', fontsize=9)

# 5. Duplicate distribution across Region
ax5 = fig.add_subplot(gs[1, 1])
region_dups = large_data[large_data.duplicated(keep=False)].groupby('Region').size()
bars = ax5.barh(region_dups.index, region_dups.values,
               color='lightcoral', edgecolor='black', alpha=0.7)
ax5.set_title('Duplicates by Region', fontweight='bold')
ax5.set_xlabel('Number of Duplicate Rows')
ax5.set_ylabel('Region')
ax5.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, region_dups.values)):
    ax5.text(val, i, f' {int(val)}', va='center', fontsize=9)

# 6. Keep parameter comparison
ax6 = fig.add_subplot(gs[1, 2])
sample_data = data.iloc[:6]  # Use smaller sample for clarity
methods = ['keep="first"', 'keep="last"', 'keep=False']
kept_counts = [
    len(sample_data.drop_duplicates(keep='first')),
    len(sample_data.drop_duplicates(keep='last')),
    len(sample_data.drop_duplicates(keep=False))
]

bars = ax6.bar(methods, kept_counts, color=['#4CAF50', '#2196F3', '#FF9800'],
              edgecolor='black', alpha=0.7)
ax6.set_title('drop_duplicates() - "keep" Parameter', fontweight='bold')
ax6.set_ylabel('Rows Kept')
ax6.tick_params(axis='x', rotation=15)
ax6.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, count in zip(bars, kept_counts):
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}',
            ha='center', va='bottom', fontsize=9)

# 7. Visual example of keep parameter
ax7 = fig.add_subplot(gs[2, :2])
ax7.axis('tight')
ax7.axis('off')

# Create a small example dataframe
example_df = pd.DataFrame({
    'ID': [1, 2, 2, 3, 3, 3, 4],
    'Value': ['A', 'B', 'B', 'C', 'C', 'C', 'D']
})

# Show results of different keep parameters
example_df['is_duplicate'] = example_df.duplicated(keep=False)
example_df['keep_first'] = ~example_df.duplicated(keep='first')
example_df['keep_last'] = ~example_df.duplicated(keep='last')
example_df['keep_false'] = ~example_df.duplicated(keep=False)

# Create table
table = ax7.table(cellText=example_df.values,
                 colLabels=example_df.columns,
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.1, 0.1, 0.2, 0.2, 0.2, 0.2])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)

# Style the header
for i in range(len(example_df.columns)):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Color code the boolean values
for i in range(len(example_df)):
    for j in range(len(example_df.columns)):
        cell = table[(i+1, j)]
        cell_value = str(example_df.iloc[i, j])
        if cell_value == 'True':
            cell.set_facecolor('#FFCDD2')
        elif cell_value == 'False':
            cell.set_facecolor('#C8E6C9')
        elif i % 2 == 0:
            cell.set_facecolor('#E3F2FD')

ax7.set_title('Understanding "keep" Parameter in duplicated() and drop_duplicates()',
             fontweight='bold', pad=20, fontsize=11)

# Add explanation text
explanation = ("keep='first': Keeps first occurrence (True means kept)\n"
              "keep='last': Keeps last occurrence\n"
              "keep=False: Marks all duplicates (none kept)")
fig.text(0.35, 0.02, explanation, fontsize=9, style='italic',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 8. Summary statistics table
ax8 = fig.add_subplot(gs[2, 2])
ax8.axis('tight')
ax8.axis('off')

summary_data = []
summary_data.append(['Total Rows', len(large_data)])
summary_data.append(['Unique Rows', len(large_data.drop_duplicates())])
summary_data.append(['Duplicate Rows', len(large_data) - len(large_data.drop_duplicates())])
summary_data.append(['Duplicate %',
                    f"{((len(large_data) - len(large_data.drop_duplicates())) / len(large_data) * 100):.1f}%"])
summary_data.append(['Complete Duplicates', large_data.duplicated().sum()])
summary_data.append(['Partial Duplicates\n(subset cols)',
                    large_data.duplicated(subset=['Product', 'Region']).sum()])

table = ax8.table(cellText=summary_data,
                 colLabels=['Metric', 'Value'],
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.6, 0.4])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.8)

# Style the header
for i in range(2):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(len(summary_data)):
    for j in range(2):
        if i % 2 == 0:
            table[(i+1, j)].set_facecolor('#E3F2FD')
        if j == 0:
            table[(i+1, j)].set_text_props(weight='bold')

ax8.set_title('Duplicates Summary', fontweight='bold', pad=20, fontsize=11)

plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '06_duplicates.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 06_duplicates.png")
