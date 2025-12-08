import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100

df = pd.read_csv("./mnt/data/shopping_behavior_updated.csv")

# ============================================================================
# FIX: Create numeric columns BEFORE filtering
# ============================================================================

# 1. Convert 'Frequency of Purchases' to numeric (times per year)
frequency_mapping = {
    'Weekly': 52,
    'Fortnightly': 26,
    'Monthly': 12,
    'Quarterly': 4,
    'Bi-Weekly': 26,      # Same as fortnightly
    'Every 3 Months': 4,  # Same as quarterly
    'Annually': 1
}

# Create numeric versions for calculations
df['Frequency_Numeric'] = df['Frequency of Purchases'].map(frequency_mapping)

# 2. Convert 'Discount Applied' to numeric (1 for Yes, 0 for No)
df['Discount_Numeric'] = (df['Discount Applied'] == 'Yes').astype(int)

# 3. Create customer value using numeric frequency
df['Customer_Value'] = df['Purchase Amount (USD)'] * df['Frequency_Numeric']

# Now filter for outerwear analysis
outerwear_df = df[df['Category'] == 'Outerwear']
other_df = df[df['Category'] != 'Outerwear']

##############################################################################
# 1. OVERVIEW VISUALIZATION
##############################################################################

# Create subplot grid
fig = plt.figure(figsize=(20, 16))

# 1.1 Purchase Frequency Distribution (Top-left)
ax1 = plt.subplot(3, 3, 1)
frequency_comparison = pd.DataFrame({
    'Outerwear': outerwear_df['Frequency of Purchases'].value_counts().sort_index(),
    'Other Categories': other_df['Frequency of Purchases'].value_counts().sort_index()
}).fillna(0)
frequency_comparison.plot(kind='bar', ax=ax1)
ax1.set_title('Purchase Frequency Distribution', fontsize=14, fontweight='bold')
ax1.set_xlabel('Frequency of Purchases')
ax1.set_ylabel('Count')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# 1.2 Seasonal Distribution (Top-center)
ax2 = plt.subplot(3, 3, 2)
seasonal_data = outerwear_df['Season'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
seasonal_data.plot(kind='pie', autopct='%1.1f%%', colors=colors, ax=ax2)
ax2.set_title('Outerwear Sales by Season', fontsize=14, fontweight='bold')
ax2.set_ylabel('')

# 1.3 Shipping Type Distribution (Top-right)
ax3 = plt.subplot(3, 3, 3)
shipping_data = outerwear_df['Shipping Type'].value_counts()
shipping_data.plot(kind='barh', color='#5D9CEC', ax=ax3)
ax3.set_title('Shipping Type Distribution', fontsize=14, fontweight='bold')
ax3.set_xlabel('Count')
ax3.set_ylabel('Shipping Type')

# 1.4 Review Rating Distribution (Middle-left)
ax4 = plt.subplot(3, 3, 4)
rating_comparison = pd.DataFrame({
    'Outerwear': outerwear_df['Review Rating'].value_counts().sort_index(),
    'Other Categories': other_df['Review Rating'].value_counts().sort_index()
}).fillna(0)
rating_comparison.plot(kind='line', marker='o', ax=ax4, linewidth=2)
ax4.set_title('Review Rating Distribution', fontsize=14, fontweight='bold')
ax4.set_xlabel('Review Rating')
ax4.set_ylabel('Count')
ax4.grid(True, alpha=0.3)
ax4.set_xticks(range(1, 6))

# 1.5 Discount Impact on Rating (Middle-center)
ax5 = plt.subplot(3, 3, 5)
discount_rating = outerwear_df.groupby('Discount Applied')['Review Rating'].mean()
discount_rating.plot(kind='bar', color='#A593E0', ax=ax5)
ax5.set_title('Discount Impact on Review Rating', fontsize=14, fontweight='bold')
ax5.set_xlabel('Discount Applied')
ax5.set_ylabel('Average Review Rating')
ax5.tick_params(axis='x', rotation=0)
ax5.axhline(y=outerwear_df['Review Rating'].mean(), color='r', linestyle='--', alpha=0.7, label='Overall Avg')
ax5.legend()

# 1.6 Subscription Status Comparison (Middle-right)
ax6 = plt.subplot(3, 3, 6)
subscription_data = pd.DataFrame({
    'Category': ['Outerwear', 'Other Categories'],
    'Subscription Rate': [
        outerwear_df['Subscription Status'].value_counts(normalize=True).get('Yes', 0),
        other_df['Subscription Status'].value_counts(normalize=True).get('Yes', 0)
    ]
})
subscription_data.plot(kind='bar', x='Category', y='Subscription Rate', color=['#FF6B6B', '#4ECDC4'], ax=ax6)
ax6.set_title('Subscription Rate Comparison', fontsize=14, fontweight='bold')
ax6.set_ylabel('Subscription Rate (%)')
ax6.set_ylim(0, 1)
ax6.tick_params(axis='x', rotation=0)

# 1.7 Purchase Amount Distribution (Bottom-left)
ax7 = plt.subplot(3, 3, 7)
outerwear_df['Purchase Amount (USD)'].plot(kind='hist', bins=20, alpha=0.7, color='#FF6B6B', label='Outerwear', ax=ax7)
other_df['Purchase Amount (USD)'].plot(kind='hist', bins=20, alpha=0.7, color='#4ECDC4', label='Other Categories', ax=ax7)
ax7.set_title('Purchase Amount Distribution', fontsize=14, fontweight='bold')
ax7.set_xlabel('Purchase Amount (USD)')
ax7.set_ylabel('Frequency')
ax7.legend()

# 1.8 Size Distribution (Bottom-center)
ax8 = plt.subplot(3, 3, 8)
size_data = outerwear_df['Size'].value_counts()
size_data.plot(kind='bar', color='#5D9CEC', ax=ax8)
ax8.set_title('Outerwear Size Distribution', fontsize=14, fontweight='bold')
ax8.set_xlabel('Size')
ax8.set_ylabel('Count')
ax8.tick_params(axis='x', rotation=0)

# 1.9 Previous Purchases Distribution (Bottom-right)
ax9 = plt.subplot(3, 3, 9)
prev_purchases = outerwear_df['Previous Purchases'].value_counts().sort_index()
prev_purchases.plot(kind='area', alpha=0.7, color='#45B7D1', ax=ax9)
ax9.set_title('Previous Purchases Distribution', fontsize=14, fontweight='bold')
ax9.set_xlabel('Previous Purchases')
ax9.set_ylabel('Count')
ax9.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./mnt/data/outerwear_overview_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

##############################################################################
# 2. SEASONAL DECOMPOSITION VISUALIZATION
##############################################################################

fig2, ((ax21, ax22), (ax23, ax24)) = plt.subplots(2, 2, figsize=(16, 12))

# 2.1 Seasonal Purchase Amount
seasonal_outerwear = outerwear_df.groupby('Season').agg({
    'Purchase Amount (USD)': 'sum',
    'Discount_Numeric': 'mean',  # Use numeric version
    'Review Rating': 'mean',
    'Customer ID': 'count'
}).rename(columns={'Customer ID': 'Transaction_Count'})

seasons = ['Winter', 'Spring', 'Summer', 'Fall']
colors_seasonal = ['#45B7D1', '#96CEB4', '#FFEAA7', '#FF6B6B']

ax21.bar(range(len(seasons)), seasonal_outerwear.loc[seasons, 'Purchase Amount (USD)'], 
         color=colors_seasonal, alpha=0.8)
ax21.set_title('Total Purchase Amount by Season', fontsize=14, fontweight='bold')
ax21.set_xlabel('Season')
ax21.set_ylabel('Total Purchase Amount (USD)')
ax21.set_xticks(range(len(seasons)))
ax21.set_xticklabels(seasons)

# Add value labels on bars
for i, v in enumerate(seasonal_outerwear.loc[seasons, 'Purchase Amount (USD)']):
    ax21.text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')

# 2.2 Transaction Count by Season
ax22.bar(range(len(seasons)), seasonal_outerwear.loc[seasons, 'Transaction_Count'], 
         color=colors_seasonal, alpha=0.8)
ax22.set_title('Transaction Count by Season', fontsize=14, fontweight='bold')
ax22.set_xlabel('Season')
ax22.set_ylabel('Number of Transactions')
ax22.set_xticks(range(len(seasons)))
ax22.set_xticklabels(seasons)

# Add value labels on bars
for i, v in enumerate(seasonal_outerwear.loc[seasons, 'Transaction_Count']):
    ax22.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')

# 2.3 Discount & Rating by Season (Dual Axis)
ax23_secondary = ax23.twinx()
width = 0.35
x = np.arange(len(seasons))

bars1 = ax23.bar(x - width/2, seasonal_outerwear.loc[seasons, 'Discount_Numeric'], 
                width, label='Discount Rate', color='#5D9CEC', alpha=0.7)
bars2 = ax23_secondary.bar(x + width/2, seasonal_outerwear.loc[seasons, 'Review Rating'], 
                          width, label='Avg Rating', color='#FF6B6B', alpha=0.7)

ax23.set_title('Discount & Rating by Season', fontsize=14, fontweight='bold')
ax23.set_xlabel('Season')
ax23.set_ylabel('Discount Rate (0-1)')
ax23_secondary.set_ylabel('Average Review Rating')
ax23.set_xticks(x)
ax23.set_xticklabels(seasons)

# Combine legends
lines1, labels1 = ax23.get_legend_handles_labels()
lines2, labels2 = ax23_secondary.get_legend_handles_labels()
ax23.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# 2.4 Seasonal Comparison with Other Categories
seasonal_comparison = pd.DataFrame({
    'Outerwear': outerwear_df.groupby('Season')['Customer ID'].count(),
    'Other Categories': other_df.groupby('Season')['Customer ID'].count()
}).fillna(0)

x = np.arange(len(seasons))
width = 0.35

bars1 = ax24.bar(x - width/2, seasonal_comparison.loc[seasons, 'Outerwear'], 
                width, label='Outerwear', color='#FF6B6B', alpha=0.8)
bars2 = ax24.bar(x + width/2, seasonal_comparison.loc[seasons, 'Other Categories'], 
                width, label='Other Categories', color='#4ECDC4', alpha=0.8)

ax24.set_title('Seasonal Sales Comparison', fontsize=14, fontweight='bold')
ax24.set_xlabel('Season')
ax24.set_ylabel('Number of Transactions')
ax24.set_xticks(x)
ax24.set_xticklabels(seasons)
ax24.legend()

plt.tight_layout()
plt.savefig('./mnt/data/seasonal_decomposition.png', dpi=300, bbox_inches='tight')
plt.show()

##############################################################################
# 3. HYPOTHESIS TESTING VISUALIZATION
##############################################################################

fig3, ((ax31, ax32), (ax33, ax34)) = plt.subplots(2, 2, figsize=(16, 12))

# 3.1 Hypothesis 2.1: Discount Anchoring
# Group by numeric discount column
discount_anchor_test = outerwear_df.groupby('Discount_Numeric').agg({
    'Frequency_Numeric': 'mean',  # Use numeric frequency
    'Previous Purchases': 'mean',
    'Review Rating': 'mean'
}).sort_index()

# Rename index for clarity
discount_anchor_test.index = ['No Discount', 'Discount Applied']

x = np.arange(len(discount_anchor_test))
width = 0.25

bars1 = ax31.bar(x - width, discount_anchor_test['Frequency_Numeric'], 
                width, label='Frequency (per year)', color='#5D9CEC', alpha=0.8)
bars2 = ax31.bar(x, discount_anchor_test['Previous Purchases'], 
                width, label='Previous Purchases', color='#45B7D1', alpha=0.8)
bars3 = ax31.bar(x + width, discount_anchor_test['Review Rating'], 
                width, label='Rating', color='#96CEB4', alpha=0.8)

ax31.set_title('Discount Anchoring Analysis', fontsize=14, fontweight='bold')
ax31.set_xlabel('Discount Status')
ax31.set_ylabel('Metrics')
ax31.set_xticks(x)
ax31.set_xticklabels(discount_anchor_test.index)  # Use the renamed labels
ax31.legend()
ax31.grid(True, alpha=0.3, axis='y')

# 3.2 Hypothesis 2.2: Experience Quality Gap
categories = ['Outerwear', 'Other Categories']
experience_data = [
    outerwear_df['Review Rating'].mean(),
    other_df['Review Rating'].mean()
]

bars = ax32.bar(categories, experience_data, color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
ax32.set_title('Experience Quality Gap', fontsize=14, fontweight='bold')
ax32.set_ylabel('Average Review Rating')
ax32.set_ylim(0, 5)

# Add value labels
for bar, value in zip(bars, experience_data):
    height = bar.get_height()
    ax32.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

# 3.3 Hypothesis 2.3: Assortment Friction
assortment_data = pd.DataFrame({
    'Metric': ['Size Variety', 'Color Variety'],
    'Outerwear': [
        outerwear_df['Size'].nunique(),
        outerwear_df['Color'].nunique()
    ],
    'Other Categories': [
        other_df['Size'].nunique(),
        other_df['Color'].nunique()
    ]
})

x = np.arange(len(assortment_data))
width = 0.35

bars1 = ax33.bar(x - width/2, assortment_data['Outerwear'], 
                width, label='Outerwear', color='#FF6B6B', alpha=0.8)
bars2 = ax33.bar(x + width/2, assortment_data['Other Categories'], 
                width, label='Other Categories', color='#4ECDC4', alpha=0.8)

ax33.set_title('Assortment Variety Comparison', fontsize=14, fontweight='bold')
ax33.set_xlabel('Variety Type')
ax33.set_ylabel('Number of Options')
ax33.set_xticks(x)
ax33.set_xticklabels(assortment_data['Metric'])
ax33.legend()

# 3.4 Hypothesis 2.4: Habit Formation
subscription_rates = pd.DataFrame({
    'Category': ['Outerwear', 'Other Categories'],
    'Subscription Rate': [
        outerwear_df['Subscription Status'].value_counts(normalize=True).get('Yes', 0) * 100,
        other_df['Subscription Status'].value_counts(normalize=True).get('Yes', 0) * 100
    ]
})

bars = ax34.bar(subscription_rates['Category'], subscription_rates['Subscription Rate'], 
               color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
ax34.set_title('Habit Formation: Subscription Rates', fontsize=14, fontweight='bold')
ax34.set_ylabel('Subscription Rate (%)')
ax34.set_ylim(0, 100)
ax34.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))

# Add value labels
for bar, value in zip(bars, subscription_rates['Subscription Rate']):
    height = bar.get_height()
    ax34.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('./mnt/data/hypothesis_testing.png', dpi=300, bbox_inches='tight')
plt.show()

##############################################################################
# 4. PERFORMANCE GAP ANALYSIS
##############################################################################

fig4, (ax41, ax42) = plt.subplots(1, 2, figsize=(16, 6))

# 4.1 Frequency Gap Analysis - Use numeric frequency
frequency_gap_data = pd.DataFrame({
    'Metric': ['Expected (Other Categories)', 'Actual (Outerwear)'],
    'Frequency': [
        other_df['Frequency_Numeric'].mean(),
        outerwear_df['Frequency_Numeric'].mean()
    ]
})

bars1 = ax41.bar(frequency_gap_data['Metric'], frequency_gap_data['Frequency'], 
                color=['#4ECDC4', '#FF6B6B'], alpha=0.8)
ax41.set_title('Purchase Frequency Gap Analysis', fontsize=14, fontweight='bold')
ax41.set_ylabel('Average Frequency (purchases/year)')
ax41.set_ylim(0, max(frequency_gap_data['Frequency']) * 1.2)

# Add gap arrow
gap_freq = frequency_gap_data['Frequency'].iloc[1] - frequency_gap_data['Frequency'].iloc[0]
arrow_color = 'red' if gap_freq < 0 else 'green'
ax41.annotate('', xy=(1, frequency_gap_data['Frequency'].iloc[0]), 
              xytext=(1, frequency_gap_data['Frequency'].iloc[1]),
              arrowprops=dict(arrowstyle='<->', color=arrow_color, lw=2))
ax41.text(1.1, (frequency_gap_data['Frequency'].iloc[0] + frequency_gap_data['Frequency'].iloc[1])/2,
         f'Gap: {gap_freq:.2f}', va='center', color=arrow_color, fontweight='bold')

# Add value labels
for bar, value in zip(bars1, frequency_gap_data['Frequency']):
    height = bar.get_height()
    ax41.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

# 4.2 Customer Value Gap Analysis
expected_value = other_df['Customer_Value'].mean()
actual_value = outerwear_df['Customer_Value'].mean()

value_gap_data = pd.DataFrame({
    'Metric': ['Expected (Other Categories)', 'Actual (Outerwear)'],
    'Customer Value': [expected_value, actual_value]
})

bars2 = ax42.bar(value_gap_data['Metric'], value_gap_data['Customer Value'], 
                color=['#4ECDC4', '#FF6B6B'], alpha=0.8)
ax42.set_title('Customer Value Gap Analysis', fontsize=14, fontweight='bold')
ax42.set_ylabel('Average Customer Value (USD)')
ax42.set_ylim(0, max(value_gap_data['Customer Value']) * 1.2)

# Add gap arrow
gap_value = value_gap_data['Customer Value'].iloc[1] - value_gap_data['Customer Value'].iloc[0]
arrow_color = 'red' if gap_value < 0 else 'green'
ax42.annotate('', xy=(1, value_gap_data['Customer Value'].iloc[0]), 
              xytext=(1, value_gap_data['Customer Value'].iloc[1]),
              arrowprops=dict(arrowstyle='<->', color=arrow_color, lw=2))
ax42.text(1.1, (value_gap_data['Customer Value'].iloc[0] + value_gap_data['Customer Value'].iloc[1])/2,
         f'Gap: ${gap_value:.2f}', va='center', color=arrow_color, fontweight='bold')

# Add value labels
for bar, value in zip(bars2, value_gap_data['Customer Value']):
    height = bar.get_height()
    ax42.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'${value:.2f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('./mnt/data/performance_gap_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

##############################################################################
# 5. CORRELATION HEATMAP FOR OUTERWEAR
##############################################################################

# Use numeric columns for correlation
numerical_cols = ['Purchase Amount (USD)', 'Review Rating', 'Discount_Numeric', 
                  'Previous Purchases', 'Frequency_Numeric', 'Age']

# Create correlation matrix
corr_matrix = outerwear_df[numerical_cols].corr()

# Rename columns for better readability in the heatmap
corr_matrix_renamed = corr_matrix.rename(columns={
    'Discount_Numeric': 'Discount Applied',
    'Frequency_Numeric': 'Frequency of Purchases'
}, index={
    'Discount_Numeric': 'Discount Applied',
    'Frequency_Numeric': 'Frequency of Purchases'
})

fig5, ax5 = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix_renamed, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": .8}, ax=ax5)
ax5.set_title('Outerwear Feature Correlation Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('./mnt/data/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

print("All visualizations have been created and saved to /mnt/data/")
print("Files created:")
print("1. outerwear_overview_analysis.png - Comprehensive overview")
print("2. seasonal_decomposition.png - Seasonal analysis")
print("3. hypothesis_testing.png - Hypothesis validation")
print("4. performance_gap_analysis.png - Gap analysis")
print("5. correlation_heatmap.png - Feature correlations")
