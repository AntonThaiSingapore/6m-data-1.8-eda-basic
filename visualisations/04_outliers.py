"""
Visualization for Outlier Detection
Shows different methods to identify and handle outliers
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Create sample data with outliers
np.random.seed(42)
normal_data = np.random.normal(100, 15, 200)
outliers = np.array([150, 155, 160, 45, 40, 35])
data_with_outliers = np.concatenate([normal_data, outliers])
df = pd.DataFrame({'values': data_with_outliers})

# Calculate statistics for outlier detection
Q1 = df['values'].quantile(0.25)
Q3 = df['values'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

mean = df['values'].mean()
std = df['values'].std()
z_lower = mean - 3 * std
z_upper = mean + 3 * std

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

fig.suptitle('Outlier Detection and Handling', fontsize=16, fontweight='bold')

# 1. Box plot with outliers highlighted
ax1 = fig.add_subplot(gs[0, 0])
bp = ax1.boxplot(df['values'], vert=True, patch_artist=True,
                 boxprops=dict(facecolor='lightblue', alpha=0.7),
                 medianprops=dict(color='red', linewidth=2),
                 flierprops=dict(marker='o', markerfacecolor='red', markersize=8,
                               markeredgecolor='darkred', alpha=0.7))

ax1.set_title('Box Plot - Outliers Highlighted', fontweight='bold')
ax1.set_ylabel('Value')
ax1.grid(True, alpha=0.3, axis='y')

# Annotate IQR boundaries
ax1.axhline(y=lower_bound, color='orange', linestyle='--', alpha=0.7,
           label=f'Lower Bound: {lower_bound:.1f}')
ax1.axhline(y=upper_bound, color='orange', linestyle='--', alpha=0.7,
           label=f'Upper Bound: {upper_bound:.1f}')
ax1.legend(fontsize=8)

# 2. Histogram with outlier boundaries
ax2 = fig.add_subplot(gs[0, 1])
n, bins, patches = ax2.hist(df['values'], bins=30, color='skyblue',
                             edgecolor='black', alpha=0.7)

# Color outlier bins
for i, patch in enumerate(patches):
    if bins[i] < lower_bound or bins[i] > upper_bound:
        patch.set_facecolor('red')
        patch.set_alpha(0.7)

ax2.axvline(lower_bound, color='orange', linestyle='--', linewidth=2,
           label=f'IQR Lower: {lower_bound:.1f}')
ax2.axvline(upper_bound, color='orange', linestyle='--', linewidth=2,
           label=f'IQR Upper: {upper_bound:.1f}')
ax2.axvline(mean, color='green', linestyle='-', linewidth=2,
           label=f'Mean: {mean:.1f}')

ax2.set_title('Histogram - IQR Method', fontweight='bold')
ax2.set_xlabel('Value')
ax2.set_ylabel('Frequency')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3, axis='y')

# 3. Scatter plot showing outliers
ax3 = fig.add_subplot(gs[0, 2])
is_outlier = (df['values'] < lower_bound) | (df['values'] > upper_bound)
ax3.scatter(df.index[~is_outlier], df['values'][~is_outlier],
           c='blue', alpha=0.5, s=30, label='Normal')
ax3.scatter(df.index[is_outlier], df['values'][is_outlier],
           c='red', alpha=0.8, s=100, marker='D', label='Outliers',
           edgecolors='darkred', linewidth=1.5)

ax3.axhline(lower_bound, color='orange', linestyle='--', alpha=0.7)
ax3.axhline(upper_bound, color='orange', linestyle='--', alpha=0.7)

ax3.set_title('Scatter Plot - Outliers Marked', fontweight='bold')
ax3.set_xlabel('Index')
ax3.set_ylabel('Value')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Z-score method
ax4 = fig.add_subplot(gs[1, 0])
z_scores = np.abs((df['values'] - mean) / std)
z_outliers = z_scores > 3

ax4.scatter(df.index[~z_outliers], df['values'][~z_outliers],
           c='blue', alpha=0.5, s=30, label='Normal')
ax4.scatter(df.index[z_outliers], df['values'][z_outliers],
           c='red', alpha=0.8, s=100, marker='D', label='Outliers (|z| > 3)',
           edgecolors='darkred', linewidth=1.5)

ax4.axhline(z_upper, color='purple', linestyle='--', alpha=0.7,
           label=f'μ + 3σ: {z_upper:.1f}')
ax4.axhline(z_lower, color='purple', linestyle='--', alpha=0.7,
           label=f'μ - 3σ: {z_lower:.1f}')
ax4.axhline(mean, color='green', linestyle='-', alpha=0.7, label=f'Mean: {mean:.1f}')

ax4.set_title('Z-Score Method (|z| > 3)', fontweight='bold')
ax4.set_xlabel('Index')
ax4.set_ylabel('Value')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# 5. Before and After removing outliers - Box plots
ax5 = fig.add_subplot(gs[1, 1])
df_cleaned = df[~is_outlier]

bp_data = [df['values'], df_cleaned['values']]
bp = ax5.boxplot(bp_data, labels=['With Outliers', 'Without Outliers'],
                patch_artist=True)

colors = ['lightcoral', 'lightgreen']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

for median in bp['medians']:
    median.set_color('red')
    median.set_linewidth(2)

ax5.set_title('Comparison: Before & After Outlier Removal', fontweight='bold')
ax5.set_ylabel('Value')
ax5.grid(True, alpha=0.3, axis='y')

# 6. Distribution comparison
ax6 = fig.add_subplot(gs[1, 2])
ax6.hist(df['values'], bins=30, alpha=0.5, color='red',
        label='With Outliers', edgecolor='black')
ax6.hist(df_cleaned['values'], bins=30, alpha=0.7, color='green',
        label='Without Outliers', edgecolor='black')
ax6.set_title('Distribution Comparison', fontweight='bold')
ax6.set_xlabel('Value')
ax6.set_ylabel('Frequency')
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

# 7. Capping/Winsorizing outliers
ax7 = fig.add_subplot(gs[2, 0])
df_capped = df.copy()
df_capped.loc[df_capped['values'] < lower_bound, 'values'] = lower_bound
df_capped.loc[df_capped['values'] > upper_bound, 'values'] = upper_bound

ax7.scatter(df.index, df['values'], alpha=0.5, s=30, label='Original', c='blue')
ax7.scatter(df.index, df_capped['values'], alpha=0.5, s=20, label='Capped', c='orange')
ax7.axhline(lower_bound, color='red', linestyle='--', alpha=0.5)
ax7.axhline(upper_bound, color='red', linestyle='--', alpha=0.5)

ax7.set_title('Capping/Winsorizing Method', fontweight='bold')
ax7.set_xlabel('Index')
ax7.set_ylabel('Value')
ax7.legend()
ax7.grid(True, alpha=0.3)

# 8. Summary statistics table
ax8 = fig.add_subplot(gs[2, 1:])
ax8.axis('tight')
ax8.axis('off')

summary_data = []
summary_data.append(['Total Data Points', len(df), len(df_cleaned), len(df_capped)])
summary_data.append(['Mean', f"{df['values'].mean():.2f}",
                     f"{df_cleaned['values'].mean():.2f}",
                     f"{df_capped['values'].mean():.2f}"])
summary_data.append(['Std Dev', f"{df['values'].std():.2f}",
                     f"{df_cleaned['values'].std():.2f}",
                     f"{df_capped['values'].std():.2f}"])
summary_data.append(['Min', f"{df['values'].min():.2f}",
                     f"{df_cleaned['values'].min():.2f}",
                     f"{df_capped['values'].min():.2f}"])
summary_data.append(['Max', f"{df['values'].max():.2f}",
                     f"{df_cleaned['values'].max():.2f}",
                     f"{df_capped['values'].max():.2f}"])
summary_data.append(['Q1 (25%)', f"{df['values'].quantile(0.25):.2f}",
                     f"{df_cleaned['values'].quantile(0.25):.2f}",
                     f"{df_capped['values'].quantile(0.25):.2f}"])
summary_data.append(['Median (50%)', f"{df['values'].quantile(0.5):.2f}",
                     f"{df_cleaned['values'].quantile(0.5):.2f}",
                     f"{df_capped['values'].quantile(0.5):.2f}"])
summary_data.append(['Q3 (75%)', f"{df['values'].quantile(0.75):.2f}",
                     f"{df_cleaned['values'].quantile(0.75):.2f}",
                     f"{df_capped['values'].quantile(0.75):.2f}"])
summary_data.append(['Outliers Detected (IQR)', f"{is_outlier.sum()}", 'N/A', '0 (capped)'])

table = ax8.table(cellText=summary_data,
                 colLabels=['Metric', 'Original', 'Outliers Removed', 'Capped/Winsorized'],
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.25, 0.25, 0.25, 0.25])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.2)

# Style the header
for i in range(4):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(len(summary_data)):
    for j in range(4):
        if i % 2 == 0:
            table[(i+1, j)].set_facecolor('#E3F2FD')
        # Highlight the metric column
        if j == 0:
            table[(i+1, j)].set_text_props(weight='bold')

ax8.set_title('Statistical Summary Comparison', fontweight='bold', pad=20, fontsize=12)

plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '04_outliers.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 04_outliers.png")
