from os.path import basename
from glob import glob
from pandas import read_csv, DataFrame as DF, concat as df_concat
import plotly.express as px
import numpy as np


def table_name(filename):
    return basename(filename).split('.')[0].split('_')[1]


def read_data(year, geo_sources, distance_sources):
    csv_files = glob(f"raw_data/csv/{year}*.csv")
    data = {}
    for f in csv_files:
        tn = table_name(f)
        csv = read_csv(f)
        csv["Has_geo"] = tn in geo_sources
        csv["Has_distance"] = tn in distance_sources
        csv["Year"] = year
        data[tn] = csv
    return data


def plot_source_dist(counts):
    fig = px.pie(counts, names="Source", values="Num_rows", hole=.4,
                 height=1500, width=3000, facet_col="Year")
    fig.update_layout(font={"size": 36})
    for c, year in enumerate(counts.Year.unique()):
        total_rows = counts[counts.Year == year].Num_rows.sum() #sum(counts[year]["Num_rows"])
        fig.add_annotation(x=(c * .66) + .17, y=.5,
                           text=f"Total rows: {total_rows}",
                           font={"size": 48}, showarrow=False)
    return fig


def plot_geo_dist(data):
    geo_info = []
    for year in data.keys():
        for s, csv in data[year].items():
            geo_info.append(csv[["Year", "Has_geo", "Has_distance"]])
    geo_info = df_concat(geo_info)
    return (px.histogram(geo_info, x="Has_geo", facet_col="Year"),
            px.histogram(geo_info, x="Has_distance", facet_col="Year"))


def count_sources(data):
    source_counts = {}
    for year, s in data.items():
        sources = sorted(s.keys())
        source_counts[year] = DF({"Source": sources, "Year": year,
                                  "Num_rows": [len(s[ss]) for ss in sources]})
    return df_concat(source_counts)


if __name__ == "__main__":
    years = [2018, 2022]
    geo_sources = ["Columbus", "Controlling", "Train-Controlling",
                   "OBB", "HR", "HR-Train"]
    distance_sources = ["Columbus"]
    data = {y: read_data(y, geo_sources, distance_sources) for y in years}
    # if source has any geospatial information (distance, from-to etc)
    source_counts = count_sources(data)
    plot_source_dist(source_counts).write_image("figures/data_stats.png")
    (has_geo_fig, has_dist_fig) = plot_geo_dist(data)
    has_geo_fig.write_image("figures/geo_avail.png")
    has_dist_fig.write_image("figures/dist_avail.png")


    same_sources = np.intersect1d(*[list(data[y].keys()) for y in years])
    data_overlaping = {y: {s: DF(data[y][s]) for s in same_sources} for y in years}
    source_counts_overlaping = count_sources(data_overlaping)
    plot_source_dist(source_counts_overlaping).write_image("figures/data_stats_overlaping.png")
    (has_geo_fig, has_dist_fig) = plot_geo_dist(data_overlaping)
    has_geo_fig.write_image("figures/geo_avail_overlaping.png")
    has_dist_fig.write_image("figures/dist_avail_overlaping.png")

