from notebooks.utils import read_data, fetch_distances

data = read_data(2022)

ds = data["Columbus"]
t_d, t_t = fetch_distances(ds["Abflugsort"], ds["Zielort"], "train")
ds["Train_distance(km)"] = t_d
ds["Train_time(hours)"] = t_t
ds.to_csv("preprocessed_data/csv/2022_Columbus.csv")

ds = data["Controlling"]
distances = fetch_distances(ds.Start, ds.Stop, "plane")
ds["Distance(km)"] = distances
t_d, t_t = fetch_distances(ds.Start, ds.Stop, "train")
ds["Train_distance(km)"] = t_d
ds["Train_time(hours)"] = t_t
ds.to_csv("preprocessed_data/csv/2022_Controlling.csv")

ds = data["Train-Controlling"]
stops = [s.replace("T_", '') for s in ds.Stop]
distances, times = fetch_distances(ds.Start, stops, "train")
ds["Distance(km)"] = distances
ds["Time(hours)"] = times
ds.to_csv("preprocessed_data/csv/2022_Train-Controlling.csv")

ds = data["OBB"]
distances, times = fetch_distances(ds.Start, ds.Stop, "train")
ds["Distance(km)"] = distances
ds["Time(hours)"] = times
ds.to_csv("preprocessed_data/csv/2022_OBB.csv")

ds = data["HR"]
distances = fetch_distances(["Vienna"] * len(ds), ds.City, "plane")
ds["Distance from Vienna(km)"] = distances
t_d, t_t = fetch_distances(["Vienna"] * len(ds), ds.City, "train")
ds["Train_distance(km)"] = t_d
ds["Train_time(hours)"] = t_t
ds.to_csv("preprocessed_data/csv/2022_HR.csv")

ds = data["HR-Train"]
distances, times = fetch_distances(["Vienna"] * len(ds), ds.City, "train")
ds["Distance from Vienna(km)"] = distances
ds["Time from Vienna(km)"] = times
ds.to_csv("preprocessed_data/csv/2022_HR-Train.csv")

data = read_data(2018)

ds = data["Columbus"]
t_d, t_t = fetch_distances(ds["Abflugsort"], ds["Zielort"], "train")
ds["Train_distance(km)"] = t_d
ds["Train_time(hours)"] = t_t
ds.to_csv("preprocessed_data/csv/2018_Columbus.csv")

ds = data["Controling"]
distances = fetch_distances(ds.Start, ds.Stop, "plane")
ds["Distance(km)"] = distances
t_d, t_t = fetch_distances(ds.Start, ds.Stop, "train")
ds["Train_distance(km)"] = t_d
ds["Train_time(hours)"] = t_t
ds.to_csv("preprocessed_data/csv/2018_Controlling.csv")

ds = data["Train-Controlling"]
distances, times = fetch_distances(ds.Start, ds.Stop, "train")
ds["Distance(km)"] = distances
ds["Time(hours)"] = times
ds.to_csv("preprocessed_data/csv/2018_Train-Controlling.csv")

ds = data["OBB"]
distances, times = fetch_distances(ds.Start, ds.Stop, "train")
ds["Distance(km)"] = distances
ds["Time(hours)"] = times
ds.to_csv("preprocessed_data/csv/2018_OBB.csv")
