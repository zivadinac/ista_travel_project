import numpy as np
from os import makedirs
from pandas import read_csv, read_excel, concat
import plotly.express as px


# First, I extracted zip file from Paul into folder "raw_data".
# Now all data is in "raw_data/CO2_footprint_conferences".
# This can in different place for you, just modify IN_DIR variable.
# Plots will be saved in {OUT_DIR}.

IN_DIR = "raw_data/CO2_footprint_conferences"
OUT_DIR = "figures/paper_analysis"
makedirs(OUT_DIR, exist_ok=True)


FLIGHT_THR = 800
# data wrangling
euromar_2016 = read_excel(f"{IN_DIR}/Euromar_2016_Aarhus/Aarhus_analysed.xlsx")
euromar_2016.rename(columns={"Land": "Participant country", "flight_co2eq_Aarhus": "Flight CO2", "train_co2eq_Aarhus": "Train CO2", "flight_distance_route_Aarhus": "Flight distance", "train_distance_route_Aarhus": "Train distance"}, inplace=True)
euromar_2016 = euromar_2016[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2016["#participants"] = 620
euromar_2016["Host city"] = "Aarhus"
euromar_2016["Year"] = 2016
euromar_2016["Conference"] = "Euromar 2016, Aarhus"

euromar_2017 = read_excel(f"{IN_DIR}/Analysis_Lucky/Analysed files - abstract extracted/Abstracts_extracted_2017.xlsx")
euromar_2017.rename(columns={"country": "Participant country", "flight_co2eq": "Flight CO2", "train_co2eq": "Train CO2", "flight_distance_route": "Flight distance", "train_distance_route": "Train distance", "year": "Year"}, inplace=True)
euromar_2017 = euromar_2017[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2017["#participants"] = 650
euromar_2017["Host city"] = "Warsaw"
euromar_2017["Year"] = 2017
euromar_2017["Conference"] = "Euromar 2017, Warsaw"

euromar_2018 = read_excel(f"{IN_DIR}/Analysis_Lucky/Analysed files - abstract extracted/Abstracts_extracted_2018.xlsx")
euromar_2018.rename(columns={"country": "Participant country", "flight_co2eq": "Flight CO2", "train_co2eq": "Train CO2", "flight_distance_route": "Flight distance", "train_distance_route": "Train distance", "year": "Year"}, inplace=True)
euromar_2018 = euromar_2018[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2018["#participants"] = 723
euromar_2018["Host city"] = "Nantes"
euromar_2018["Year"] = 2018
euromar_2018["Conference"] = "Euromar 2018, Nantes"

euromar_2019 = read_excel(f"{IN_DIR}/Analysis_Lucky/Analysed files - abstract extracted/Abstracts_extracted_2019.xlsx")
euromar_2019.rename(columns={"country": "Participant country", "flight_co2eq": "Flight CO2", "train_co2eq": "Train CO2", "flight_distance_route": "Flight distance", "train_distance_route": "Train distance", "year": "Year"}, inplace=True)
euromar_2019 = euromar_2019[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2019["#participants"] = 1100
euromar_2019["Host city"] = "Berlin"
euromar_2019["Year"] = 2019
euromar_2019["Conference"] = "Euromar 2019, Berlin"

euromar_2022 = read_excel(f"{IN_DIR}/Analysis_Lucky/Analysed files - abstract extracted/Abstracts_extracted_2022.xlsx")
euromar_2022.rename(columns={"country": "Participant country", "flight_co2eq": "Flight CO2", "train_co2eq": "Train CO2", "flight_distance_route": "Flight distance", "train_distance_route": "Train distance", "year": "Year"}, inplace=True)
euromar_2022 = euromar_2022[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2022["#participants"] = 635
euromar_2022["Host city"] = "Utrecht"
euromar_2022["Year"] = 2022
euromar_2022["Conference"] = "Euromar 2022, Utrecht"

euromar_2023 = read_excel(f"{IN_DIR}/Analysis_Lucky/Analysed files - abstract extracted/Abstracts_extracted_2023.xlsx")
euromar_2023.rename(columns={"country": "Participant country", "flight_co2eq": "Flight CO2", "train_co2eq": "Train CO2", "flight_distance_route": "Flight distance", "train_distance_route": "Train distance", "year": "Year"}, inplace=True)
euromar_2023 = euromar_2023[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2023["#participants"] = 690
euromar_2023["Host city"] = "Glasgow"
euromar_2023["Year"] = 2023
euromar_2023["Conference"] = "Euromar 2023, Glasgow"

euromar_2024 = read_excel(f"{IN_DIR}/Euromar_2024_Bilbao/cities_with_countries_and_distances.xlsx")
euromar_2024.rename(columns={"Country": "Participant country", "flight_economy_CO2eq": "Flight CO2", "train_co2eq_ISTA": "Train CO2", "flight_distance_route": "Flight distance", "train_distance_route": "Train distance"}, inplace=True)
euromar_2024 = euromar_2024[["Participant country", "Flight CO2", "Train CO2", "Flight distance", "Train distance"]]
euromar_2024["#participants"] = 670
euromar_2024["Year"] = 2024
euromar_2024["Host city"] = "Bilbao"
euromar_2024["Conference"] = "Euromar 2024, Bilbao"

icmrbs_2022 = read_excel(f"{IN_DIR}/ICMRBS_2022_Boston/Boston.xlsx")
icmrbs_2022.rename(columns={"Country": "Participant country",
                            "flight_co2eq_Boston": "Flight CO2",
                            "flight_distance_route_Boston": "Flight distance",
                            "train_co2eq_Boston": "Train CO2",
                            "train_distance_route_Boston": "Train distance"}, inplace=True)
icmrbs_2022.loc[icmrbs_2022.Airport == "Boston", ["Train distance", "Flight distance"]] = 0
icmrbs_2022 = icmrbs_2022[["Participant country", "Flight CO2", "Flight distance", "Train CO2", "Train distance"]]
icmrbs_2022["#participants"] = 470
icmrbs_2022["Year"] = 2022
icmrbs_2022["Host city"] = "Boston"
icmrbs_2022["Conference"] = "ICMRBS 2022, Boston"

icmrbs_2024 = read_excel(f"{IN_DIR}/ICMRBS_2024_Seoul/Seoul.xlsx")
icmrbs_2024["Country"] = read_csv(f"{IN_DIR}/ICMRBS_2024_Seoul/countries.csv").Country
icmrbs_2024.rename(columns={"Country": "Participant country",
                            "flight_co2eq_Seoul": "Flight CO2",
                            "flight_distance_route_Seoul": "Flight distance",
                            "train_co2eq_Seoul": "Train CO2",
                            "train_distance_route_Seoul": "Train distance"}, inplace=True)
icmrbs_2024.loc[icmrbs_2024.Airport == "Seoul", ["Train distance", "Flight distance"]] = 0
icmrbs_2024 = icmrbs_2024[["Participant country", "Flight CO2", "Flight distance", "Train CO2", "Train distance"]]
icmrbs_2024["#participants"] = 583
icmrbs_2024["Year"] = 2024
icmrbs_2024["Host city"] = "Seoul"
icmrbs_2024["Conference"] = "ICMRBS 2024, Seoul"

encismar_2025 = read_excel(f"{IN_DIR}/ENCISMAR_2025_MontereyCA/ENC - SF.xlsx")
california_cities = read_csv(f"{IN_DIR}/ENCISMAR_2025_MontereyCA/california_cities.csv").City.to_numpy()
encismar_2025.rename(columns={"Country": "Participant country", "flight_co2eq_San Francisco": "Flight CO2", "flight_distance_route_San Francisco": "Flight distance"}, inplace=True)
encismar_2025 = encismar_2025[["Participant country", "Flight CO2", "Flight distance"]]
encismar_2025["#participants"] = 700
encismar_2025["Train CO2"] = np.nan
encismar_2025["Train distance"] = np.nan
encismar_2025["Year"] = 2025
encismar_2025["Host city"] = "San Francisco"
encismar_2025["Conference"] = "ENC-ISMAR 2025, San Francisco"
encismar_2025 = encismar_2025[encismar_2025["Flight distance"] != "km, one way"]  # LOL
encismar_2025 = encismar_2025[encismar_2025["Flight distance"] <= 1000000]  # seems too big, probably wrong as equator is only 40k km

data = concat([euromar_2016, euromar_2017, euromar_2018, euromar_2019, euromar_2022, euromar_2023, euromar_2024, icmrbs_2022, icmrbs_2024, encismar_2025], ignore_index=True)
data["Flight CO2"] = data["Flight CO2"] * 1.15  # uplift + airport infrastructure
gamma = 0.0249  # 24.9 g/km, CO2 per passenger
data["Train CO2"] = data["Train CO2"] + gamma * data["Train distance"]
data["Flight CO2"] = data["Flight CO2"] * 2  # to and from the conference
data["Train CO2"] = data["Train CO2"] + 2  # to and from the conference
data["Trip distance"] = [float(td) if td <= FLIGHT_THR else float(fd) for ri, (td, fd) in data[["Train distance", "Flight distance"]].iterrows()]
data["Trip mode"] = ["Train" if td <= FLIGHT_THR else "Flight" for td in data["Train distance"]]
data["Trip CO2"] = [t if td <= FLIGHT_THR else f for ri, (td, t, f) in data[["Train distance", "Train CO2", "Flight CO2"]].iterrows()]
CONF_COLORS = dict(zip(data.Conference.unique(), px.colors.qualitative.Vivid))


# CO2 per conference participant
co2_per_part = data.groupby(["Conference"])["Trip CO2"].agg(["mean", "sem"]).reset_index()
co2_per_part["City"] = ["\t" + c.split(",")[1] + "\t" for c in co2_per_part["Conference"]]  # formatting hack
# add numbers from Paul's xlxs as he knows who travelled by car
co2_per_part.loc[co2_per_part.Conference == "ENC-ISMAR 2025, San Francisco", "mean"] = 2739.425
co2_per_part.loc[co2_per_part.Conference == "ENC-ISMAR 2025, San Francisco", "sem"] = 80.59691
co2_per_part["conf_year"] = [c.split(",")[0] for c in co2_per_part["Conference"]]  # formatting hack
fig = px.bar(co2_per_part, x="conf_year", y="mean", error_y="sem",
             color="Conference", text="City", color_discrete_map=CONF_COLORS)
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=2000, height=1500, font_size=40)
fig = fig.update_yaxes(title="Emitted CO2 per perticipant")
fig = fig.update_xaxes(title=None)
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white", textfont_size=50))
fig.write_image(f"{OUT_DIR}/co2_per_participant.svg")

# total CO2 per conference
total_co2 = co2_per_part.merge(data.groupby("Conference")["#participants"].first().reset_index(), on="Conference")
total_co2["Total CO2 emitted"] = np.round(total_co2["mean"] * total_co2["#participants"] / 1000, 1)
total_co2["Conference_txt"] = [c.replace(",", "<br>") for c in total_co2["Conference"]]  # formatting hack
fig = px.pie(total_co2, names="Conference_txt", color="Conference", values="Total CO2 emitted", hole=.35, color_discrete_map=CONF_COLORS)
fig = fig.update_traces(textposition="inside", textinfo='label+value',
                        textfont_size=30,
                        marker=dict(line=dict(color='#000000', width=2)))
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=1000, height=1000, font_size=20,
                        annotations=[dict(text='Total CO2 emitted<br>(thousand t)', x=.5, y=0.5,
                                          font_size=30, showarrow=False, xanchor="center")])
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white"))
fig.write_image(f"{OUT_DIR}/co2_per_conference_pie.svg")
# total CO2 per conference, bar chart
fig = px.bar(total_co2, x="conf_year", y="Total CO2 emitted",
             color="Conference", text="City", color_discrete_map=CONF_COLORS)
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=2000, height=1500, font_size=40)
fig = fig.update_yaxes(title="Total emitted CO2 (1000 t)")
fig = fig.update_xaxes(title=None)
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white", textfont_size=50))
fig.write_image(f"{OUT_DIR}/co2_per_conference_bar.svg")

# distance distributions
dist_idx = np.isfinite(data["Trip distance"])
fig = px.histogram(data[dist_idx], x="Trip distance", color="Conference", color_discrete_map=CONF_COLORS)
fig = fig.update_layout(template="plotly_white",
                        legend_title=None, legend_x=.8,
                        width=2000, height=1500, font_size=50)
fig.write_image(f"{OUT_DIR}/distance_hist.svg")

for t in ["Trip", "Train", "Flight"]:
    fig = px.ecdf(data[dist_idx], x=f"{t} distance", color="Conference", color_discrete_map=CONF_COLORS)
    fig = fig.update_traces(line_width=10)
    fig = fig.update_layout(template="plotly_white",
                            legend_title=None, legend_x=.55, legend_y=.01,
                            width=2000, height=1500, font_size=50)
    xticks = [FLIGHT_THR, 5000, 10000, 15000, 20000]
    xtickvals = [FLIGHT_THR, "5k", "10k", "15k", "20k"]
    fig = fig.update_xaxes(tickvals=xticks, ticktext=xtickvals)
    fig = fig.update_xaxes(title=f"{t} distance (km)")
    fig = fig.update_yaxes(title="Cumulative probability")
    fig.write_image(f"{OUT_DIR}/distance_cdf_{t}.svg")

# travel mode distibution, conf-by-conf
vcs = data.value_counts("Conference").reset_index()
tr_mode = data.groupby(["Conference", "Trip mode"])["Year"].count().reset_index().merge(vcs, on="Conference")
tr_mode["Percent"] = tr_mode["Year"] / tr_mode["count"] * 100
tr_mode = tr_mode.groupby("Trip mode")["Percent"].agg(["mean", "sem"]).reset_index()
tr_mode["txt"] = [" <br>" + tm for tm in tr_mode["Trip mode"]]
tot_em = data.groupby(["Conference"])["Trip CO2"].sum().reset_index()
tr_mode_em = data.groupby(["Conference", "Trip mode"])["Trip CO2"].sum().reset_index().merge(tot_em, on="Conference")
tr_mode_em["Percent"] = tr_mode_em["Trip CO2_x"] / tr_mode_em["Trip CO2_y"] * 100
tr_mode_em = tr_mode_em.groupby("Trip mode")["Percent"].agg(["mean", "sem"]).reset_index()
tr_mode_em["txt"] = [" <br>" + tm for tm in tr_mode_em["Trip mode"]]
fig = px.bar(tr_mode, x="Trip mode", color="Trip mode", y="mean", error_y="sem")
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=500, height=400, font_size=14)
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white", textfont_size=22))
fig = fig.update_xaxes(title=None)
fig = fig.update_yaxes(title="% participants")
fig.write_image(f"{OUT_DIR}/travel_mode_dist_stat.svg")
fig = px.bar(tr_mode_em, x="Trip mode", color="Trip mode", y="mean", error_y="sem")
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=500, height=400, font_size=14)
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white", textfont_size=22))
fig = fig.update_xaxes(title=None)
fig = fig.update_yaxes(title="% emissions")
fig.write_image(f"{OUT_DIR}/travel_mode_emissions_stat.svg")

# travel mode distribution, all together
tr_mode = data.groupby(["Trip mode"])["Year"].count().reset_index()
tr_mode["Percent"] = tr_mode["Year"] / len(data) * 100
tr_mode["txt"] = [" <br>" + tm for tm in tr_mode["Trip mode"]]
tr_mode_em = data.groupby(["Trip mode"])["Trip CO2"].sum().reset_index()
tr_mode_em["Percent"] = tr_mode_em["Trip CO2"] / data["Trip CO2"].sum() * 100
tr_mode_em["txt"] = [" <br>" + tm for tm in tr_mode_em["Trip mode"]]
fig = px.bar(tr_mode, x="Trip mode", color="Trip mode", y="Percent")
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=500, height=400, font_size=14)
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white", textfont_size=22))
fig = fig.update_xaxes(title=None)
fig = fig.update_yaxes(title="% participants")
fig.write_image(f"{OUT_DIR}/travel_mode_dist.svg")
fig = px.bar(tr_mode_em, x="Trip mode", color="Trip mode", y="Percent")
fig = fig.update_layout(template="plotly_white", showlegend=False,
                        width=500, height=400, font_size=14)
fig = fig.for_each_trace(lambda t: t.update(textfont_color="white", textfont_size=22))
fig = fig.update_xaxes(title=None)
fig = fig.update_yaxes(title="% emissions")
fig.write_image(f"{OUT_DIR}/travel_mode_emissions.svg")

# map with participant countries
for c, gg in data.groupby("Conference"):
    countries = gg.value_counts(["Conference", "Participant country"]).reset_index()
    fig = px.scatter_geo(countries, locations="Participant country", size="count",
                         locationmode="country names")
    fig = fig.update_layout(template="plotly_white", showlegend=False,
                            width=1000, height=1000, font_size=36)
    fig = fig.add_annotation(text=c, showarrow=False, y=0.2)
    cc = c.replace(" ", "-").replace(",", "")
    fig.write_image(f"{OUT_DIR}/visitor_geodist_{cc}.svg")
