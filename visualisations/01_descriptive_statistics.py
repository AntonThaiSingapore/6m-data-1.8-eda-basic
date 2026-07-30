"""
Visualization for Descriptive Statistics
Illustrates how describe() statistics relate to visual distributions
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Create sample data similar to the notebook
np.random.seed(42)
data = pd.DataFrame({
    'column_A': np.random.normal(50, 15, 1000),
    'column_B': np.random.exponential(20, 1000),
    'column_C': np.random.uniform(0, 100, 1000)
})

# Create figure with subplots
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
fig.suptitle('Descriptive Statistics Visualizations', fontsize=16, fontweight='bold')

columns = ['column_A', 'column_B', 'column_C']
titles = ['Normal Distribution', 'Exponential Distribution', 'Uniform Distribution']

for idx, (col, title) in enumerate(zip(columns, titles)):
    # Get statistics
    stats = data[col].describe()

    # Histogram
    ax1 = axes[idx, 0]
    ax1.hist(data[col], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.axvline(stats['mean'], color='red', linestyle='--', linewidth=2, label=f"Mean: {stats['mean']:.2f}")
    ax1.axvline(stats['50%'], color='green', linestyle='--', linewidth=2, label=f"Median: {stats['50%']:.2f}")
    ax1.axvline(stats['mean'] + stats['std'], color='orange', linestyle=':', linewidth=2, label=f"±1 Std: {stats['std']:.2f}")
    ax1.axvline(stats['mean'] - stats['std'], color='orange', linestyle=':', linewidth=2)
    ax1.set_title(f'{title} - Histogram')
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Box plot
    ax2 = axes[idx, 1]
    bp = ax2.boxplot(data[col], vert=True, patch_artist=True,
                     labels=[col],
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))

    # Annotate key statistics
    ax2.text(1.3, stats['25%'], f"Q1: {stats['25%']:.2f}", fontsize=9, va='center')
    ax2.text(1.3, stats['50%'], f"Median: {stats['50%']:.2f}", fontsize=9, va='center', color='red', fontweight='bold')
    ax2.text(1.3, stats['75%'], f"Q3: {stats['75%']:.2f}", fontsize=9, va='center')
    ax2.text(1.3, stats['min'], f"Min: {stats['min']:.2f}", fontsize=9, va='center')
    ax2.text(1.3, stats['max'], f"Max: {stats['max']:.2f}", fontsize=9, va='center')

    ax2.set_title(f'{title} - Box Plot')
    ax2.set_ylabel('Value')
    ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '01_descriptive_statistics.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 01_descriptive_statistics.png")

# Create a summary table visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# Get describe output
desc_table = data.describe().T
desc_table = desc_table.round(2)

table = ax.table(cellText=desc_table.values,
                colLabels=desc_table.columns,
                rowLabels=desc_table.index,
                cellLoc='center',
                loc='center',
                colWidths=[0.12] * len(desc_table.columns))

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style the header
for i in range(len(desc_table.columns)):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style the row headers
for i in range(len(desc_table.index)):
    table[(i+1, -1)].set_facecolor('#E8F5E9')
    table[(i+1, -1)].set_text_props(weight='bold')

plt.title('DataFrame.describe() Output', fontsize=14, fontweight='bold', pad=20)
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '01_descriptive_statistics_table.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 01_descriptive_statistics_table.png")
