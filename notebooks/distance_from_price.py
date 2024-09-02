from notebooks.utils import read_data

# rough estimation based on ETH report
# .17 EUR / km for planes
# .30 EUR / km for trains

if True:
    # Guests
    data = read_data(2022)

    data["Guest"]["Distance(km)"] = data["Guest"]["Betrag in Hauswährung"] / .17
    data["Guest"].to_csv("preprocessed_data/csv/2022_Guest.csv")

    data["Train-Guest"]["Distance(km)"] = data["Guest"]["Betrag in Hauswährung"] / .30
    data["Train-Guest"].to_csv("preprocessed_data/csv/2022_Train-Guest.csv")

    data = read_data(2018)

    data["Guests"]["Distance(km)"] = data["Guests"]["Betrag in Hauswährung"] / .17
    data["Guests"].to_csv("preprocessed_data/csv/2018_Guests.csv")

    data["Train-Guest"]["Distance(km)"] = data["Train-Guest"]["Betrag in Hauswährung"] / .30
    data["Train-Guest"].to_csv("preprocessed_data/csv/2018_Train-Guest.csv")

if True:
    # HR
    data = read_data(2022, in_dir="preprocessed_data")
    data["HR"]["Distance from price"] = data["HR"]["Betrag Hausw."] / .17
    data["HR"].to_csv("preprocessed_data/csv/2022_HR.csv")
    data["HR-Train"]["Distance from price"] = data["HR-Train"]["Betrag Hausw."] / .3
    data["HR-Train"].to_csv("preprocessed_data/csv/2022_HR-Train.csv")
