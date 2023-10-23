import pandas as pd

# read western.md file
with open('western.md', 'r') as f:
    data = f.read()
    # split by empty new line
    data = data.split('\n\n')
    print(data)

# # read central.md file
# with open('central.md', 'r') as f:
#     data_2 = f.read()
#     # split by empty new line
#     data_2 = data_2.split('\n\n')
#     print(data_2)
#
# # combine data and data_2
# data = data + data_2
# print(data)

# new dataframe
df = pd.DataFrame(
    columns=["name", "description", "imageUrl", "city", "province", "openTime", "closeTime", "latitude", "longitude",
             "accessibility", "historical_context", "hands_on_activities", "planning", "rating"])

# for each line in data
for i, line in enumerate(data):
    # split by new line
    line_temp = line.split('\n')
    # for each item in line_temo split by : keep only second item
    line_temp = [item.split(': ', 1)[1] for item in line_temp]

    # concat to dataframe
    df = pd.concat([df, pd.DataFrame([line_temp],
                                     columns=["name", "description", "imageUrl", "city", "province", "openTime",
                                              "closeTime", "latitude", "longitude", "accessibility",
                                              "historical_context", "hands_on_activities", "planning", "rating"])])

print(df)

# save to csv
# df.to_csv('locations_central.csv', index=False)
df.to_csv('locations_western.csv', index=False)
