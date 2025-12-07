import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('./mnt/data/company_orders.csv')

# Convert order_data to datetime (fixing the data type found earlier)
df['order_date'] = pd.to_datetime(df['order_date'])

print('=== STEP 3: EXPLORATORY DATA ANALYSIS ===\n')

# 1. REVENUE per month
print("1. REVENUE TRENDS PER MONTH")
monthly_revenue = df.groupby(df['order_date'].dt.to_period('M'))['order_amount'].sum()
print(monthly_revenue.head(10))

# 2. NUMBERS OF ORDERS OVERTIME
print("\n2. ORDER VOLUME TRENDS")
monthly_orders = df.groupby(df['order_date'].dt.to_period('M')).size()
print(monthly_orders.head(10))

# 3. RETURNING VS NEW CUSTOMERs
print("\n3. CUSTOMER LOYALTY ANALYSIS")
customer_order_counts = df['customer_id'].value_counts()

returning_customers = (customer_order_counts > 1).sum()
new_customers = (customer_order_counts == 1).sum()

print(f"Returning customers (2+ orders): {returning_customers}")
print(f"One_time customers: {new_customers}")
print(f"Returning customer rate: {returning_customers/(returning_customers+new_customers): .1%}")

# 4. BEST SELLING PRODUCTS
print("\n4. PRODUCT CATEGORY PERFORMANCE")
product_performance = df.groupby('product_category').agg({
    'order_amount': ['sum', 'count', 'mean']
}).round(2)
product_performance.columns = ['Total Revenue', 'Number of orders', 'Average Order Value']
print(product_performance.sort_values('Total Revenue', ascending=False))

# 5.BEST SELLING PLATFORM
print("\n5. BEST SELLING CHANNEL")
channel_performance = df.groupby('channel').agg({
    'order_amount': ['sum', 'count', 'mean'],
    'customer_id': 'nunique'
}).round(2)
channel_performance.columns = ['Total Revenue', 'Number of orders', 'Avg Order Value', 'Unique customers']
print(channel_performance.sort_values('Total Revenue', ascending=False))

# 6. CAMPAIGN EFFECTIVENESS (despite missing data)
print("\n6. CAMPAIGN PERFORMANCE")
campaign_performance = df.groupby('campaign').agg({
    'order_amount': ['sum', 'count', 'mean']
}).round(2)
campaign_performance.columns = ['Total Revenue', 'Number of Orders', 'Average Order Value']
print(campaign_performance.sort_values('Total Revenue', ascending=False))

# 7. CUSTOMER LIFETIME VALUE ANALYSIS
print("\n7. CUSTOMER LIFETIME VALUE")
customer_lifetime = df.groupby('customer_id').agg({
    'order_amount': ['sum', 'count', 'mean'],
    'order_date': ['min', 'max']
}).round(2)

customer_lifetime.columns = ['Total Spent', 'Number of orders', 'Average Order Value', 'First Order', 'Last Order']
print(customer_lifetime.sort_values('Total Spent', ascending=False).head(10))

# 8. SEASONAL ANALYSIS
print("\n8. SEASONAL TRENDS")
df['month'] = df['order_date'].dt.month
monthly_trends = df.groupby('month').agg({
    'order_amount': ['sum', 'count']
}).round(2)
monthly_trends.columns = ['Monthly Revenue', 'monthly Orders']
print(monthly_trends)


print("=== STEP 4: GENERATE BUSINESS INSIGHTS ===\n")

# INSIGHT 1. "why is the company losing customers"
print("1. CUSTOMER RETENTION ANALYSIS")

# calculate customer churn rate
customer_activity = df.groupby('customer_id').agg({
    
})
























































