import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./mnt/data/shopping_behavior_updated.csv")

##############################################################################
#############      1. BEHAVIORAL FREQUENCY MODEL ANALYSIS        #############
##############################################################################

# 1. NEED CYCLE -> how often do people need outerwear?
need_cycle_analysis = df[df['Category'] == 'Outerwear'].groupby('Customer ID')['Previous Purchases'].max()
print(f"Average outerwear purchase per customer: {need_cycle_analysis.mean()}")

# 2. HABIT STRENGTH -> Are customers in a buying routine?
subscription_outerwear = df[df['Category'] == 'Outerwear']['Subscription Status'].value_counts()
print(f'Subscription rates for outerwear: {subscription_outerwear}')

# 3. FRICTION -> What makes buying difficult?
friction_analysis = df[df['Category'] == 'Outerwear']['Shipping Type'].value_counts()
size_variety = df[df['Category'] == 'Outerwear']['Size'].nunique()
print(f"shipping friction: {friction_analysis}")
print(f"Size options (choice overload): {size_variety}")

# 4. PERCEIVED -> Price vs quality perception?

outerwear_df = df[df['Category'] == 'Outerwear']
value_analysis = outerwear_df.groupby('Discount Applied')['Review Rating'].mean()
print(f"Discount impact on perceived quality: {value_analysis}")

# 5. EXPERIENCE MEMORY -> Does past experience affect future buying?
experience_impact = outerwear_df.groupby('Review Rating')['Frequency of Purchases'].mean()
print(f"Rating impact on purchase frequency: {experience_impact}")

# 6. SEASONALITY -> Natural buying cycles
seasonal_pattern = outerwear_df['Season'].value_counts()
print(f"Seasonal distribution: {seasonal_pattern}")


##############################################################################
###############          2. SEASONAL DECOMPOSITION            ################
##############################################################################

# Decompose outerwear demand into components
seasonal_outerwear = outerwear_df.groupby('Season').agg({
    'Purchase Amount (USD)': 'sum',
    'Discount Applied': 'mean',
    'Review Rating': 'mean',
    'Customer ID': 'count'
}).rename(columns={'Customer ID': 'Transaction_Count'})

print("seasonal Decomposition of outerwear Demand:")
print(seasonal_outerwear)

# Calculate baseline demand (non seasonal components)
baseline_demand = df[df['Category'] != 'Outerwear'].groupby('Season')['Customer ID'].count().mean()
print(f"\nBaseline shopping demand (other categories): {baseline_demand}")

# Promotional Components Impact
promo_impact = outerwear_df.groupby('Discount Applied').agg({
    'Purchase Amount (USD)': 'sum',
    'Review Rating': 'mean',
    'Customer ID': 'count'
})
print(f"\nPromotional impact analysis: {promo_impact}")


# What SHOULD outerwear performance look like?

# Expected vs Actual Frequency
expected_frequency = df[df['Category'] != 'Outerwear']['Frequency of Purchases'].mean()
actual_frequency = outerwear_df['Frequency of Purchases'].mean()
frequency_gap = actual_frequency - expected_frequency

print(f"Expected purchase frequency: {expected_frequency:.2f}")
print(f"Actual outerwear frequency: {actual_frequency:.2f}")
print(f"Frequency gap: {frequency_gap:.2f}")

# Expected vs Actual Customer Value
df['Customer_Value'] = df['Purchase Amount (USD)'] * df['Frequency of Purchases']
expected_value = df[df['Category'] != 'Outerwear']['Customer_Value'].mean()
actual_value = outerwear_df['Customer_Value'].mean()
value_gap = actual_value - expected_value

print(f"\nExpected customer value: ${expected_value:.2f}")
print(f"Actual outerwear value: ${actual_value:.2f}")
print(f"Value gap: ${value_gap:.2f}")



# Hypothesis Tree for Outerwear Performance

"""
MAIN PROBLEM: Outerwear underperformance despite discounts

HYPOTHESIS 1: Natural seasonal cycles explain poor performance
  - Sub-hypothesis: Weather patterns shifted buying cycles
  - Sub-hypothesis: We're measuring in the wrong seasonal window

HYPOTHESIS 2: Additional mechanisms are depressing frequency
  - Sub-hypothesis 2.1: Deep discounts created price anchors
      - Evidence: High discount dependence in purchase patterns
      - Test: Correlation between discount size and repurchase timing
      
  - Sub-hypothesis 2.2: Poor experience reduces repeat purchases
      - Evidence: Low review ratings despite discounts
      - Test: Experience metrics vs other categories
      
  - Sub-hypothesis 2.3: Assortment issues create friction
      - Evidence: Size/color limitations causing poor fit
      - Test: Return rates, review comments about fit
      
  - Sub-hypothesis 2.4: Habit formation failure
      - Evidence: Low subscription rates, irregular purchase patterns
      - Test: Customer loyalty metrics vs other categories
"""

# Test Hypothesis 2.1: Discount Anchoring
discount_anchor_test = outerwear_df.groupby('Discount Applied').agg({
    'Frequency of Purchases': 'mean',
    'Previous Purchases': 'mean',
    'Review Rating': 'mean'
})
print("Discount Anchor Test:")
print(discount_anchor_test)

# Test Hypothesis 2.2: Experience Quality  
experience_gap = outerwear_df['Review Rating'].mean() - df[df['Category'] != 'Outerwear']['Review Rating'].mean()
print(f"\nExperience Gap (Outerwear vs Other Categories): {experience_gap:.2f}")

# Test Hypothesis 2.3: Assortment Friction
size_variety_gap = outerwear_df['Size'].nunique() - df[df['Category'] != 'Outerwear']['Size'].nunique()
color_variety_gap = outerwear_df['Color'].nunique() - df[df['Category'] != 'Outerwear']['Color'].nunique()
print(f"\nAssortment Gaps - Sizes: {size_variety_gap}, Colors: {color_variety_gap}")

# Test Hypothesis 2.4: Habit Formation
subscription_gap = (outerwear_df['Subscription Status'].value_counts(normalize=True)['Yes'] - 
                   df[df['Category'] != 'Outerwear']['Subscription Status'].value_counts(normalize=True)['Yes'])
print(f"\nSubscription Rate Gap: {subscription_gap:.2%}")
