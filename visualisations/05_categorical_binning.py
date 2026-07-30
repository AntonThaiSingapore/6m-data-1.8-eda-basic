"""
Visualization for Categorical Data and Binning
Shows pd.cut(), pd.qcut(), and categorical data operations
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Create sample age data
np.random.seed(42)
ages = np.random.randint(18, 75, 200)
df_ages = pd.DataFrame({'age': ages})

# Create bins using cut (equal width)
bins_cut = [18, 30, 45, 60, 75]
labels_cut = ['Young Adult', 'Adult', 'Middle Age', 'Senior']
df_ages['age_cut'] = pd.cut(df_ages['age'], bins=bins_cut, labels=labels_cut)

# Create bins using qcut (equal frequency)
df_ages['age_qcut'] = pd.qcut(df_ages['age'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# Create figure with subplots
fig = plt.figure(figsize=(16, 14))
gs = fig.add_gridspec(4, 3, hspace=0.4, wspace=0.3)

fig.suptitle('Categorical Data and Binning Operations', fontsize=16, fontweight='bold')

# 1. Original continuous data distribution
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(df_ages['age'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
ax1.set_title('Original Continuous Data', fontweight='bold')
ax1.set_xlabel('Age')
ax1.set_ylabel('Frequency')
ax1.grid(True, alpha=0.3, axis='y')

# Add statistics
mean_age = df_ages['age'].mean()
median_age = df_ages['age'].median()
ax1.axvline(mean_age, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_age:.1f}')
ax1.axvline(median_age, color='green', linestyle='--', linewidth=2, label=f'Median: {median_age:.1f}')
ax1.legend()

# 2. pd.cut() - Equal width bins
ax2 = fig.add_subplot(gs[0, 1])
cut_counts = df_ages['age_cut'].value_counts().sort_index()
bars = ax2.bar(cut_counts.index, cut_counts.values, color='coral',
               edgecolor='black', alpha=0.7)
ax2.set_title('pd.cut() - Equal Width Bins', fontweight='bold')
ax2.set_xlabel('Age Group')
ax2.set_ylabel('Frequency')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=9)

# 3. pd.qcut() - Equal frequency bins
ax3 = fig.add_subplot(gs[0, 2])
qcut_counts = df_ages['age_qcut'].value_counts().sort_index()
bars = ax3.bar(qcut_counts.index, qcut_counts.values, color='lightgreen',
               edgecolor='black', alpha=0.7)
ax3.set_title('pd.qcut() - Equal Frequency (Quantile) Bins', fontweight='bold')
ax3.set_xlabel('Quartile')
ax3.set_ylabel('Frequency')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=9)

# 4. Visual representation of cut() bins
ax4 = fig.add_subplot(gs[1, :2])
colors_map = {'Young Adult': 'skyblue', 'Adult': 'lightgreen',
              'Middle Age': 'orange', 'Senior': 'salmon'}
for label in labels_cut:
    mask = df_ages['age_cut'] == label
    ax4.scatter(df_ages[mask].index, df_ages[mask]['age'],
               alpha=0.6, s=30, label=label, color=colors_map[label])

# Draw bin boundaries
for bin_edge in bins_cut:
    ax4.axhline(bin_edge, color='red', linestyle='--', alpha=0.5, linewidth=1)

# Annotate bin ranges
for i in range(len(bins_cut)-1):
    mid_y = (bins_cut[i] + bins_cut[i+1]) / 2
    ax4.text(205, mid_y, f'{labels_cut[i]}\n[{bins_cut[i]}, {bins_cut[i+1]})',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax4.set_title('pd.cut() - Equal Width Binning Visualization', fontweight='bold')
ax4.set_xlabel('Sample Index')
ax4.set_ylabel('Age')
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)
ax4.set_xlim(-5, 220)

# 5. Visual representation of qcut() bins
ax5 = fig.add_subplot(gs[1, 2])
qcut_bins = df_ages['age_qcut'].cat.categories
colors_qcut = ['#e3f2fd', '#90caf9', '#42a5f5', '#1565c0']

for i, (label, color) in enumerate(zip(['Q1', 'Q2', 'Q3', 'Q4'], colors_qcut)):
    mask = df_ages['age_qcut'] == label
    ages_in_bin = df_ages[mask]['age']
    ax5.scatter([i] * len(ages_in_bin), ages_in_bin,
               alpha=0.6, s=30, color=color, label=label)

ax5.set_title('pd.qcut() - Equal Frequency Distribution', fontweight='bold')
ax5.set_xlabel('Quartile')
ax5.set_ylabel('Age')
ax5.set_xticks(range(4))
ax5.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# 6. Comparison of bin sizes
ax6 = fig.add_subplot(gs[2, 0])
cut_ranges = [bins_cut[i+1] - bins_cut[i] for i in range(len(bins_cut)-1)]
ax6.bar(labels_cut, cut_ranges, color='coral', edgecolor='black', alpha=0.7)
ax6.set_title('pd.cut() - Bin Width Comparison', fontweight='bold')
ax6.set_xlabel('Bin Label')
ax6.set_ylabel('Bin Width (years)')
ax6.tick_params(axis='x', rotation=45)
ax6.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, (label, width) in enumerate(zip(labels_cut, cut_ranges)):
    ax6.text(i, width, f'{width} yrs', ha='center', va='bottom', fontsize=9)

# 7. Categorical operations - value_counts
ax7 = fig.add_subplot(gs[2, 1])
cat_series = pd.Series(['apple', 'banana', 'apple', 'cherry', 'banana', 'apple', 'date'])
cat_series_with_cats = cat_series.astype('category')
# Add an extra category
cat_series_with_cats = cat_series_with_cats.cat.add_categories(['elderberry'])

vc1 = cat_series.value_counts()
vc2 = cat_series_with_cats.value_counts()

x = np.arange(len(vc2))
width = 0.35

ax7.bar(x - width/2, [vc1.get(cat, 0) for cat in vc2.index], width,
       label='Regular Series', color='lightblue', alpha=0.7)
ax7.bar(x + width/2, vc2.values, width,
       label='Categorical (shows unused)', color='lightgreen', alpha=0.7)

ax7.set_title('Categorical Type - Shows All Categories', fontweight='bold')
ax7.set_xlabel('Category')
ax7.set_ylabel('Count')
ax7.set_xticks(x)
ax7.set_xticklabels(vc2.index, rotation=45)
ax7.legend()
ax7.grid(True, alpha=0.3, axis='y')

# 8. Dummy variables (one-hot encoding)
ax8 = fig.add_subplot(gs[2, 2])
# Create simple categorical data
fruit_data = pd.Series(['apple', 'banana', 'cherry'] * 3)
dummies = pd.get_dummies(fruit_data, prefix='fruit')

# Visualize dummy variables as heatmap
sns.heatmap(dummies.T, cmap='YlGn', cbar_kws={'label': 'Value'},
           yticklabels=dummies.columns, xticklabels=False,
           annot=False, ax=ax8)
ax8.set_title('Dummy Variables (One-Hot Encoding)', fontweight='bold')
ax8.set_xlabel('Sample Index')
ax8.set_ylabel('Dummy Variable')

# 9. Summary comparison table
ax9 = fig.add_subplot(gs[3, :])
ax9.axis('tight')
ax9.axis('off')

summary_data = []
summary_data.append(['Method', 'Description', 'Bin Width', 'Use Case'])
summary_data.append(['pd.cut()', 'Divides data into equal-width intervals',
                     'Equal', 'When you want uniform ranges (e.g., age groups 0-20, 20-40)'])
summary_data.append(['pd.qcut()', 'Divides data into equal-frequency intervals (quantiles)',
                     'Variable', 'When you want equal sample sizes in each bin'])
summary_data.append(['Categorical', 'Special pandas dtype that stores categories efficiently',
                     'N/A', 'For repeated string/object data, better memory usage'])
summary_data.append(['get_dummies()', 'Converts categorical variable into dummy/indicator variables',
                     'N/A', 'For machine learning models that need numeric input'])

table = ax9.table(cellText=summary_data[1:],
                 colLabels=summary_data[0],
                 cellLoc='left',
                 loc='center',
                 colWidths=[0.15, 0.35, 0.15, 0.35])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 3)

# Style the header
for i in range(4):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(len(summary_data)-1):
    for j in range(4):
        if i % 2 == 0:
            table[(i+1, j)].set_facecolor('#E3F2FD')

ax9.set_title('Binning and Categorical Methods - Summary', fontweight='bold', pad=20, fontsize=12)

plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '05_categorical_binning.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 05_categorical_binning.png")
