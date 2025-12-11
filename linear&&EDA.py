import pandas as pd
import matplotlib.pyplot as plt

data = {
    'House': ['House A', 'House B', 'House C'],
    'Size': [1000, 1500, 2000],
    'Price': [2000000, 3000000, 4000000]
}

df = pd.DataFrame(data)

print('OUR HOUSE TABLE')
print(df)

print("\nLET'S EXPLORE THE DATA")

print('1. Just the size column:')
print(df['Size'])

print('\n2. First row (House A):')
print(df.iloc[0])

print('\n3. What will this show?')
print(df['Price'].mean())

print('OUR DATA FOR VISUALIZATION')
print(df)
print()

plt.figure(figsize=(10, 6))

plt.scatter(df['Size'], df['Price'],
            s=200,
            color='red',
            edgecolors='black',
            linewidths=2,
            alpha=0.8)

for i in range(len(df)):
    df.loc[i, 'Size'],
    df.loc[i, 'Price'] + 10000,
    df.loc[i, 'House'],
    ha='center',
    va='bottom',
    fontsize=12,
    fontweight='bold'

plt.xlabel('House Size (square feet)', fontsize=14)
plt.ylabel('House Price ($)', fontsize=14)
plt.title('House Size vs Price Relationship', fontsize=16, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.3)

plt.gca().set_facecolor('#f5f5f5')

plt.tight_layout()
plt.show()
