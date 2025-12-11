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

plt.figure(figsize=(8, 6))

plt.scatter(df['Size'], df['Price'], s=100, color='blue')

plt.xlabel('House Size (square feet)')
plt.ylabel('House Price ($)')
plt.title('House Size vs Price Relationship')

plt.grid(True, alpha=0.3)

plt.show()
