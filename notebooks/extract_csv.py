from os import makedirs
from pandas import read_excel

# reading all sheets from xlsx is very slow
# so we extract them into separate .csv files
data_2022 = read_excel("raw_data/2022.xlsx", sheet_name=None)
data_2018 = read_excel("raw_data/2018.xlsx", sheet_name=None)
data = {"2022": data_2022, "2018": data_2018}

makedirs("raw_data/csv", exist_ok=True)
for y, d in data.items():
    for k, v in d.items():
        k = k.replace(' ', '-')
        v.to_csv(f"raw_data/csv/{y}_{k}.csv")
