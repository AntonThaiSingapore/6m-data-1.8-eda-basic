"""
Visualization for Cumulative Operations
Shows cumsum, cumprod, cummax, cummin and other accumulation methods
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Create sample data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=50, freq='D')
daily_values = np.random.randint(-10, 20, 50)
df = pd.DataFrame({
    'date': dates,
    'daily_change': daily_values
})

df['cumsum'] = df['daily_change'].cumsum()
df['cummax'] = df['daily_change'].cummax()
df['cummin'] = df['daily_change'].cummin()
df['cumprod'] = (1 + df['daily_change']/100).cumprod()

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)

fig.suptitle('Cumulative Operations Visualizations', fontsize=16, fontweight='bold')

# 1. Cumulative Sum
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df['date'], df['daily_change'], marker='o', markersize=3,
        alpha=0.5, label='Daily Change', color='gray', linewidth=1)
ax1.bar(df['date'], df['daily_change'], alpha=0.3, color='lightblue',
       edgecolor='none')
ax1.set_title('Original Data - Daily Changes', fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Value')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.axhline(0, color='black', linewidth=0.8)
ax1.tick_params(axis='x', rotation=45)

# 2. Cumulative Sum Line
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(df['date'], df['cumsum'], marker='o', markersize=4,
        linewidth=2, color='#2196F3', label='Cumulative Sum')
ax2.fill_between(df['date'], 0, df['cumsum'], alpha=0.3, color='#2196F3')
ax2.set_title('cumsum() - Running Total', fontweight='bold')
ax2.set_xlabel('Date')
ax2.set_ylabel('Cumulative Sum')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.axhline(0, color='black', linewidth=0.8)
ax2.tick_params(axis='x', rotation=45)

# Add annotations for key points
max_idx = df['cumsum'].idxmax()
min_idx = df['cumsum'].idxmin()
ax2.scatter(df.loc[max_idx, 'date'], df.loc[max_idx, 'cumsum'],
           color='green', s=100, zorder=5)
ax2.annotate(f'Peak: {df.loc[max_idx, "cumsum"]:.0f}',
            xy=(df.loc[max_idx, 'date'], df.loc[max_idx, 'cumsum']),
            xytext=(10, 10), textcoords='offset points',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='green'))

# 3. Cumulative Max and Min
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(df['date'], df['daily_change'], marker='o', markersize=3,
        alpha=0.4, label='Daily Change', color='gray', linewidth=1)
ax3.plot(df['date'], df['cummax'], marker='s', markersize=4,
        linewidth=2, color='#4CAF50', label='cummax()', linestyle='--')
ax3.plot(df['date'], df['cummin'], marker='^', markersize=4,
        linewidth=2, color='#F44336', label='cummin()', linestyle='--')
ax3.set_title('cummax() and cummin() - Running Maximum and Minimum', fontweight='bold')
ax3.set_xlabel('Date')
ax3.set_ylabel('Value')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.tick_params(axis='x', rotation=45)
ax3.axhline(0, color='black', linewidth=0.8)

# 4. Cumulative Product (with smaller values)
ax4 = fig.add_subplot(gs[1, 1])
# Use percentage returns for cumprod
returns = np.random.randn(50) * 0.02  # 2% daily volatility
df_returns = pd.DataFrame({
    'date': dates,
    'return': returns,
    'cumulative_return': (1 + pd.Series(returns)).cumprod()
})

ax4.plot(df_returns['date'], df_returns['cumulative_return'],
        linewidth=2, color='#FF9800', marker='o', markersize=3)
ax4.fill_between(df_returns['date'], 1, df_returns['cumulative_return'],
                alpha=0.3, color='#FF9800')
ax4.set_title('cumprod() - Cumulative Product (Investment Growth)', fontweight='bold')
ax4.set_xlabel('Date')
ax4.set_ylabel('Cumulative Return (multiplier)')
ax4.grid(True, alpha=0.3)
ax4.axhline(1, color='black', linewidth=0.8, linestyle='--', label='Break-even')
ax4.legend()
ax4.tick_params(axis='x', rotation=45)

# Add final return annotation
final_return = df_returns['cumulative_return'].iloc[-1]
ax4.annotate(f'Final: {final_return:.2f}x',
            xy=(df_returns['date'].iloc[-1], final_return),
            xytext=(-50, 20), textcoords='offset points',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='black'))

# 5. Comparison of all cumulative operations
ax5 = fig.add_subplot(gs[2, 0])
# Normalize for comparison (manual min-max scaling)
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df_normalized = pd.DataFrame({
    'daily_change': normalize(df['daily_change']),
    'cumsum': normalize(df['cumsum']),
    'cummax': normalize(df['cummax']),
    'cummin': normalize(df['cummin'])
})

ax5.plot(df['date'], df_normalized['daily_change'], label='Original',
        alpha=0.5, linewidth=1, color='gray')
ax5.plot(df['date'], df_normalized['cumsum'], label='cumsum()',
        linewidth=2, color='#2196F3')
ax5.plot(df['date'], df_normalized['cummax'], label='cummax()',
        linewidth=2, color='#4CAF50', linestyle='--')
ax5.plot(df['date'], df_normalized['cummin'], label='cummin()',
        linewidth=2, color='#F44336', linestyle='--')

ax5.set_title('Comparison of Cumulative Operations (Normalized)', fontweight='bold')
ax5.set_xlabel('Date')
ax5.set_ylabel('Normalized Value [0, 1]')
ax5.legend()
ax5.grid(True, alpha=0.3)
ax5.tick_params(axis='x', rotation=45)

# 6. Summary table
ax6 = fig.add_subplot(gs[2, 1])
ax6.axis('tight')
ax6.axis('off')

summary_data = []
summary_data.append(['Method', 'Description', 'Common Use Case'])
summary_data.append(['cumsum()', 'Cumulative sum of values',
                    'Running totals, accumulated values'])
summary_data.append(['cumprod()', 'Cumulative product of values',
                    'Compound growth, investment returns'])
summary_data.append(['cummax()', 'Cumulative maximum (highest value so far)',
                    'Peak tracking, high water marks'])
summary_data.append(['cummin()', 'Cumulative minimum (lowest value so far)',
                    'Low tracking, minimum thresholds'])
summary_data.append(['expanding()', 'Expanding window calculations',
                    'Running averages, growing statistics'])
summary_data.append(['rolling()', 'Fixed window moving calculations',
                    'Moving averages, smoothing'])

table = ax6.table(cellText=summary_data[1:],
                 colLabels=summary_data[0],
                 cellLoc='left',
                 loc='center',
                 colWidths=[0.2, 0.4, 0.4])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 3)

# Style the header
for i in range(3):
    table[(0, i)].set_facecolor('#2196F3')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(len(summary_data)-1):
    for j in range(3):
        if i % 2 == 0:
            table[(i+1, j)].set_facecolor('#E3F2FD')
        if j == 0:
            table[(i+1, j)].set_text_props(weight='bold')

ax6.set_title('Cumulative Operations - Summary', fontweight='bold', pad=20, fontsize=12)

plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_cumulative_operations.png'),
            dpi=300, bbox_inches='tight')
print("Saved: 07_cumulative_operations.png")
