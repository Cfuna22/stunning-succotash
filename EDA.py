import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("./mnt/data/shopping_behavior_updated.csv")

sns.set(style='whitegrid')

# Count of each payment
payment_counts = df['Payment Method'].value_counts()
print("Payment Method Counts:\n", payment_counts)

# Average purchase amount per payment method
avg_purchase_payment = df.groupby('Payment Method')['Purchase Amount (USD)'].mean()
print("\nAverage Purchase by Payment Method:\n", avg_purchase_payment)

# Visualization: Count
plt.figure(figsize=(8, 5))
sns.countplot(x= 'Payment Method', data=df, order=payment_counts.index)
plt.title('Purchase by Payment Method')
plt.savefig('Count.png')
plt.show()

# Visualization: Average Purchase Amount
plt.figure(figsize=(8, 5))
sns.barplot(x= avg_purchase_payment.index, y= avg_purchase_payment.values)
plt.title('Average Purchase Amount by Payment Method')
plt.ylabel('Average USD')
plt.savefig('Avg.png')
plt.show()


