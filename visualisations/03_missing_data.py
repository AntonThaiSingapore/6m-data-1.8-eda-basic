"""
Visualization for Missing Data
Shows patterns and strategies for handling missing values
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Create sample data with missing values
np.random.seed(42)
n_rows = 100
data = pd.DataFrame({
    'A': np.random.randn(n_rows),
    'B': np.random.randn(n_rows),
    'C': np.random.randn(n_rows),
    'D': np.random.randn(n_rows),
    'E': np.random.randn(n_rows)
})

# Introduce missing values with different patterns
data.loc[np.random.choice(data.index, 15, replace=False), 'A'] = np.nan
data.loc[np.random.choice(data.index, 25, replace=False), 'B'] = np.nan
data.loc[np.random.choice(data.index, 10, replace=False), 'C'] = np.nan
data.loc[np.random.choice(data.index, 30, replace=False), 'D'] = np.nan
data.loc[np.random.choice(data.index, 5, replace=False), 'E'] = np.nan

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

fig.suptitle('Missing Data Visualizations', fontsize=16, fontweight='bold')

# 1. Missing data heatmap
ax1 = fig.add_subplot(gs[0, :2])
sns.heatmap(data.isna(), cbar=True, cmap='RdYlGn_r', yticklabels=False,
            cbar_kws={'label': 'Missing (Yellow) vs Present (Green)'})
ax1.set_title('Missing Data Pattern - Heatmap', fontweight='bold')
ax1.set_xlabel('Columns')
ax1.set_ylabel('Row Index')

# 2. Missing data count by column
ax2 = fig.add_subplot(gs[0, 2])
missing_counts = data.isna().sum().sort_values(ascending=True)
bars = ax2.barh(missing_counts.index, missing_counts.values,
                color=['red' if x > 20 else 'orange' if x > 10 else 'yellow'
                       for x in missing_counts.values],
                edgecolor='black', alpha=0.7)
ax2.set_title('Missing Values Count', fontweight='bold')
ax2.set_xlabel('Number of Missing Values')
ax2.set_ylabel('Column')
ax2.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, missing_counts.values)):
    ax2.text(val, i, f' {int(val)}', va='center', fontsize=9)

# 3. Missing data percentage
ax3 = fig.add_subplot(gs[1, 0])
missing_pct = (data.isna().sum() / len(data) * 100).sort_values(ascending=False)
colors = ['#d32f2f' if x > 20 else '#ff9800' if x > 10 else '#ffc107' if x > 5 else '#4caf50'
          for x in missing_pct.values]
bars = ax3.bar(missing_pct.index, missing_pct.values, color=colors,
               edgecolor='black', alpha=0.7)
ax3.set_title('Missing Data Percentage by Column', fontweight='bold')
ax3.set_xlabel('Column')
ax3.set_ylabel('Percentage Missing (%)')
ax3.grid(True, alpha=0.3, axis='y')
ax3.axhline(y=20, color='red', linestyle='--', alpha=0.5, label='20% threshold')
ax3.legend()

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%',
            ha='center', va='bottom', fontsize=8)

# 4. Before and after dropna() - row counts
ax4 = fig.add_subplot(gs[1, 1])
categories = ['Original\nData', 'After dropna()\n(any)', 'After dropna()\n(all)']
counts = [len(data), len(data.dropna(how='any')), len(data.dropna(how='all'))]
colors_bar = ['#2196F3', '#FF9800', '#4CAF50']
bars = ax4.bar(categories, counts, color=colors_bar, edgecolor='black', alpha=0.7)
ax4.set_title('Impact of dropna() on Row Count', fontweight='bold')
ax4.set_ylabel('Number of Rows')
ax4.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}\nrows',
            ha='center', va='bottom', fontsize=9)

# 5. Fillna strategies comparison
ax5 = fig.add_subplot(gs[1, 2])
col_with_na = 'B'
original = data[col_with_na].dropna()
fill_mean = data[col_with_na].fillna(data[col_with_na].mean())
fill_forward = data[col_with_na].ffill()

ax5.boxplot([original, fill_mean, fill_forward],
            labels=['Original\n(dropna)', 'Fill with\nMean', 'Forward\nFill'],
            patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7))
ax5.set_title(f'Fillna Strategies - Column {col_with_na}', fontweight='bold')
ax5.set_ylabel('Value')
ax5.grid(True, alpha=0.3, axis='y')

# 6. Missing data correlation matrix
ax6 = fig.add_subplot(gs[2, 0])
missing_corr = data.isna().corr()
sns.heatmap(missing_corr, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, ax=ax6, cbar_kws={'label': 'Correlation'})
ax6.set_title('Missing Data Correlation\n(Do columns tend to be missing together?)',
              fontweight='bold')

# 7. Row-wise missing data distribution
ax7 = fig.add_subplot(gs[2, 1])
missing_per_row = data.isna().sum(axis=1)
ax7.hist(missing_per_row, bins=range(0, data.shape[1] + 2),
         color='salmon', edgecolor='black', alpha=0.7)
ax7.set_title('Distribution of Missing Values per Row', fontweight='bold')
ax7.set_xlabel('Number of Missing Values in Row')
ax7.set_ylabel('Frequency (Number of Rows)')
ax7.grid(True, alpha=0.3, axis='y')

# Add mean line
mean_missing = missing_per_row.mean()
ax7.axvline(mean_missing, color='red', linestyle='--', linewidth=2,
            label=f'Mean: {mean_missing:.2f}')
ax7.legend()

# 8. Summary table
ax8 = fig.add_subplot(gs[2, 2])
ax8.axis('tight')
ax8.axis('off')

summary_data = []
summary_data.append(['Total Cells', data.size])
summary_data.append(['Missing Cells', data.isna().sum().sum()])
summary_data.append(['Missing %', f"{(data.isna().sum().sum() / data.size * 100):.2f}%"])
summary_data.append(['Complete Rows', len(data.dropna())])
summary_data.append(['Complete Rows %', f"{(len(data.dropna()) / len(data) * 100):.2f}%"])
summary_data.append(['Rows with Any NA', len(data) - len(data.dropna())])

table = ax8.table(cellText=summary_data,
                 colLabels=['Metric', 'Value'],
                 cellLoc='left',
                 loc='center',
                 colWidths=[0.6, 0.4])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)

# Style the header
for i in range(2):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(len(summary_data)):
    for j in range(2):
        if i % 2 == 0:
            table[(i+1, j)].set_facecolor('#E3F2FD')

ax8.set_title('Missing Data Summary', fontweight='bold', pad=20)

plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '03_missing_data.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 03_missing_data.png")
