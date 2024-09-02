from notebooks.utils import read_data

RFI_750 = 1.5
RFI_750_1000 = 1.735
RFI_1000 = 2.5
UPLIFT_FACTOR = 1.08
AIRPORT_FACTOR = 1.15


def parse_distance(dist_str):
    return float(dist_str.replace("km", '')
                         .replace("KM", '')
                         .replace("Km", '')
                         .strip())


def co2(distance):
    if type(distance) == str:
        distance = parse_distance(distance)
    if distance <= 750:
        RFI = RFI_750
    elif distance <= 1000:
        RFI = RFI_750_1000
    else:
        RFI = RFI_1000
    return distance * RFI * UPLIFT_FACTOR * AIRPORT_FACTOR


data = read_data(2022, in_dir="preprocessed_data")
data["Columbus"]["CO2_our"] = data["Columbus"]["Strecke (km, Flugsegment)"].apply(co2)
data["Columbus"].to_csv("preprocessed_data/csv/2022_Columbus.csv")

data["Controlling"]["CO2_our"] = data["Controlling"]["Distance(km)"].apply(co2)
data["Controlling"].to_csv("preprocessed_data/csv/2022_Controlling.csv")

data["Guest"]["CO2_our"] = data["Guest"]["Distance(km)"].apply(co2)
data["Guest"].to_csv("preprocessed_data/csv/2022_Guest.csv")

data["HR"]["CO2_from_Vienna"] = data["HR"]["Distance from Vienna(km)"].apply(co2)
data["HR"]["CO2_from_price"] = data["HR"]["Distance from price"].apply(co2)
data["HR"].to_csv("preprocessed_data/csv/2022_HR.csv")

data = read_data(2018, in_dir="preprocessed_data")
data["Columbus"]["CO2_our"] = data["Columbus"]["Strecke (km, Flugsegment)"].apply(co2)
data["Columbus"].to_csv("preprocessed_data/csv/2018_Columbus.csv")

data["Controlling"]["CO2_our"] = data["Controlling"]["Distance(km)"].apply(co2)
data["Controlling"].to_csv("preprocessed_data/csv/2018_Controlling.csv")

data["Guests"]["CO2_our"] = data["Guests"]["Distance(km)"].apply(co2)
data["Guests"].to_csv("preprocessed_data/csv/2018_Guests.csv")
