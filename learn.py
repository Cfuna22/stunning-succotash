import pandas as pd

df = pd.read_csv("./mnt/data/shopping_behavior_updated.csv")

frequency_map = {
    "weekly": 52,
    "Bi-Weekly": 26,
    "Fortnight": 26,
    "Monthly": 12,
    "Every 3 months": 4,
    "Quarterly": 4,
    "Annually": 1
}

df["frequency_numeric"] = df["Frequency of Purchases"].map(frequency_map)

df["Discount Applied"] = df["Discount Applied"].map({"Yes": 1, "NO": 0})
df["Promo Code Used"] = df["Promo Code Used"].map({"Yes": 1, "NO": 0})
df["Subscription Status"] = df["Subscription Status"].map({"Yes": 1, "NO": 0})

df.columns = df.columns.str.lower().str.replace(" ", "_")

print(df.head())
df.info()
print(df.describe(include="all"))










