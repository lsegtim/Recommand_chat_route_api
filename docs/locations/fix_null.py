import pandas as pd

df = pd.read_csv("locations.csv")

# replace null with empty string
df = df.fillna(" ")
# print(df)

# save to csv
df.to_csv('locations.csv', index=False)
