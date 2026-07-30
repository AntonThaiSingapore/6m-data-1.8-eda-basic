"""
Visualization for Value Counts
Shows frequency distributions for categorical data
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Create sample data similar to the notebook
np.random.seed(42)
obj = pd.Series(["c", "a", "d", "a", "b", "b", "c", "c"])

# Create larger dataset for better visualization
categories = ['Python', 'Java', 'JavaScript', 'C++', 'Ruby', 'Go']
preferences = np.random.choice(categories, size=200, p=[0.35, 0.25, 0.20, 0.10, 0.06, 0.04])
df_languages = pd.Series(preferences, name='Programming Languages')

# Create figure with subplots
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Value Counts Visualizations', fontsize=16, fontweight='bold')

# 1. Simple value counts - Bar chart
ax1 = axes[0, 0]
value_counts = df_languages.value_counts()
bars = ax1.bar(value_counts.index, value_counts.values, color='skyblue', edgecolor='black', alpha=0.7)
ax1.set_title('Value Counts - Vertical Bar Chart', fontweight='bold')
ax1.set_xlabel('Category')
ax1.set_ylabel('Frequency')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=9)

# 2. Horizontal bar chart (better for many categories)
ax2 = axes[0, 1]
value_counts_sorted = df_languages.value_counts().sort_values()
bars = ax2.barh(value_counts_sorted.index, value_counts_sorted.values,
                color='lightcoral', edgecolor='black', alpha=0.7)
ax2.set_title('Value Counts - Horizontal Bar Chart', fontweight='bold')
ax2.set_xlabel('Frequency')
ax2.set_ylabel('Category')
ax2.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, value_counts_sorted.values)):
    ax2.text(val, i, f' {int(val)}', va='center', fontsize=9)

# 3. Pie chart (proportions)
ax3 = axes[0, 2]
value_counts = df_languages.value_counts()
colors = plt.cm.Set3(range(len(value_counts)))
wedges, texts, autotexts = ax3.pie(value_counts.values,
                                     labels=value_counts.index,
                                     autopct='%1.1f%%',
                                     colors=colors,
                                     startangle=90)
ax3.set_title('Value Counts - Pie Chart', fontweight='bold')

# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 4. Value counts with sorting by index
ax4 = axes[1, 0]
value_counts_by_index = df_languages.value_counts().sort_index()
bars = ax4.bar(value_counts_by_index.index, value_counts_by_index.values,
               color='lightgreen', edgecolor='black', alpha=0.7)
ax4.set_title('Value Counts - Sorted by Index (Alphabetically)', fontweight='bold')
ax4.set_xlabel('Category')
ax4.set_ylabel('Frequency')
ax4.tick_params(axis='x', rotation=45)
ax4.grid(True, alpha=0.3, axis='y')

# 5. Comparison: ascending vs descending order
ax5 = axes[1, 1]
x = np.arange(len(value_counts))
width = 0.35
bars1 = ax5.bar(x - width/2, value_counts.sort_values(ascending=False).values,
                width, label='Descending', color='orange', alpha=0.7)
bars2 = ax5.bar(x + width/2, value_counts.sort_values(ascending=True).values,
                width, label='Ascending', color='purple', alpha=0.7)
ax5.set_title('Value Counts - Sorting Comparison', fontweight='bold')
ax5.set_xlabel('Rank')
ax5.set_ylabel('Frequency')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# 6. Table view of value counts
ax6 = axes[1, 2]
ax6.axis('tight')
ax6.axis('off')

# Create table data
vc = df_languages.value_counts()
table_data = []
for idx, (cat, count) in enumerate(vc.items(), 1):
    percentage = (count / len(df_languages)) * 100
    table_data.append([idx, cat, count, f"{percentage:.1f}%"])

table = ax6.table(cellText=table_data,
                 colLabels=['Rank', 'Category', 'Count', 'Percentage'],
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.15, 0.35, 0.2, 0.25])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# Style the header
for i in range(4):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(len(table_data)):
    for j in range(4):
        if i % 2 == 0:
            table[(i+1, j)].set_facecolor('#E3F2FD')

ax6.set_title('Value Counts - Table View', fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '02_value_counts.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 02_value_counts.png")
