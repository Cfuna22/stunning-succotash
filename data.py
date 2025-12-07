import pandas as pd

df = pd.read_csv('./mnt/data/company_orders.csv')

# Check basic cleaning info
info = {
    "shape": df.shape,
    "missing_values": df.isnull().sum(),
    "duplicates": df.duplicated().sum(),
    "dtypes": df.dtypes.astype(str)
}

print(info)
