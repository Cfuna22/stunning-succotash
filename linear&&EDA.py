import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'House': ['House A', 'House B', 'House C'],
    'Size': [1000, 1500, 2000],
    'Price': [2000000, 3000000, 4000000]
}

df = pd.DataFrame(data)

# print('OUR HOUSE TABLE')
# print(df)

# print("\nLET'S EXPLORE THE DATA")

# print('1. Just the size column:')
# print(df['Size'])

# print('\n2. First row (House A):')
# print(df.iloc[0])

# print('\n3. What will this show?')
# print(df['Price'].mean())

# print('OUR DATA FOR VISUALIZATION')
# print(df)
# print()

# plt.figure(figsize=(10, 6))

# plt.scatter(df['Size'], df['Price'],
#             s=200,
#             color='red',
#             edgecolors='black',
#             linewidths=2,
#             alpha=0.8)

# for i in range(len(df)):
#     df.loc[i, 'Size'],
#     df.loc[i, 'Price'] + 10000,
#     df.loc[i, 'House'],
#     ha='center',
#     va='bottom',
#     fontsize=12,
#     fontweight='bold'

# plt.xlabel('House Size (square feet)', fontsize=14)
# plt.ylabel('House Price ($)', fontsize=14)
# plt.title('House Size vs Price Relationship', fontsize=16, fontweight='bold')

# plt.grid(True, linestyle='--', alpha=0.3)

# plt.gca().set_facecolor('#f5f5f5')

# plt.tight_layout()
# plt.show()

print(" OUR ORIGINAL DATA:")
print(df)
print()

# create our scatter plot
plt.figure(figsize=(10, 8))
plt.scatter(df['Size'], df['Price'], s=200, color='blue', edgecolors='black', linewidths=2, zorder=5, label='Actual Houses')

# Draw 3 different possible lines through these points
plt.title('Different Possible Lines Through Our Data', fontsize=16, fontweight='bold')

# LINE !: Too steep (overestimates)
x_line = np.array([800, 2200]) # X values
y_line1 = 250 * x_line - 50000 # y = 250x - 50000
plt.plot(x_line, y_line1, 'r--', linewidth=2, alpha=0.7, label='Line 1: Too steep (y = 250x - 50,000)')

# Line 2: Too shallow (underestimates)
y_line2 = 150 * x_line - 50000 # y = 150 + 50000
plt.plot(x_line, y_line2, 'g--', linewidth=2, alpha=0.7, label='Line 2: Too shallow (y = 150x + 50,000)')

# LINE 3: Just right (perfect fit)
y_line3 = 200 * x_line + 0 # y = 200x + 0
plt.plot(x_line, y_line3, 'b-', linewidth=3, label='perfect Line (y = 200x)')

# Customize the plot
plt.xlabel('House Size (square feet)', fontsize=14)
plt.ylabel('House Price ($)', fontsize=14)
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(fontsize=12)
plt.xlim(800, 2200)
plt.ylim(150000, 450000)

plt.tight_layout()
plt.show()
