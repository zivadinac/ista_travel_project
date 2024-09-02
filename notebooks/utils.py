import numpy as np
from os import getcwd
from os.path import basename, join, pardir
from glob import glob
from pandas import read_csv
import googlemaps
from haversine import haversine
from bs4 import BeautifulSoup as BS

GEO_SOURCES = ["Columbus", "Controlling", "Train-Controlling",
               "OBB", "HR", "HR-Train"]
DISTANCE_SOURCES = ["Columbus"]


def read_dotenv(env_path=None):
    if env_path is None:
        try:
            env_path = join(pardir(__file__), ".env")
        except:
            env_path = join(getcwd(), ".env")
    with open(env_path, "r") as dotenv_file:
        lines = dotenv_file.readlines()
        dotenv = {}
        for line in lines:
            line = line.strip()
            var = line.split('=')[0]
            val = line.split('=')[1]
            dotenv[var] = val
    return dotenv


GMAPS = googlemaps.Client(key=read_dotenv()["GMAPS_API_KEY"])


def table_name(filename):
    return basename(filename).split('.')[0].split('_')[1]


def read_data(year, geo_sources=GEO_SOURCES, distance_sources=DISTANCE_SOURCES, in_dir="raw_data"):
    csv_files = glob(join(in_dir, f"csv/{year}*.csv"))
    data = {}
    for f in csv_files:
        tn = table_name(f)
        csv = read_csv(f)
        csv["Has_geo"] = tn in geo_sources
        csv["Has_distance"] = tn in distance_sources
        csv["Year"] = year
        data[tn] = csv
    return data


def __get_uniq(inp):
    return [inp.lower()] if isinstance(inp, str) else np.unique([i.lower() for i in inp])


def fetch_distances(frm, to, transport_mode: str):
    """ Fetch distance between given places.

        Args:
            frm - origin (string or list)
            to - destination (string or list, but the same type as `frm`)
            transport_mode - "train" or "plane"

        Return:
            list of distances in km
            list of durations
    """
    if isinstance(frm, str):
        frm = [frm]
    if isinstance(to, str):
        to = [to]
    if transport_mode == "train":
        distances, durations = [], []
        for o, d in zip(frm, to):
            try:
                resp = GMAPS.distance_matrix(o, d,
                                             language="english", mode="transit",
                                             transit_mode=transport_mode)
                dist = resp["rows"][0]["elements"][0]["distance"]["text"]
                time = resp["rows"][0]["elements"][0]["duration"]["text"]
            except Exception as e:
                print(e)
                dist = None
                time = None
            distances.append(dist)
            durations.append(time)
        if len(frm) == 1 and len(to) == 1:
            distances, durations = distances[0], durations[0]
        return distances, durations
    if transport_mode == "plane":
        distances = []
        for o, d in zip(frm, to):
            try:
                o_coords = GMAPS.geocode(o)[0]["geometry"]["location"].values()
                d_coords = GMAPS.geocode(d)[0]["geometry"]["location"].values()
                distances.append(haversine(o_coords, d_coords, unit="km"))
            except:
                distances.append(None)
        return distances
    raise ValueError(f"Unknown `transport_mode` {transport_mode}")


def find_city_country(affiliation):
    """ For given institution return city and country. """
    place_res = GMAPS.find_place(affiliation, "textquery")
    if place_res["status"] == "OK":
        place_id = place_res["candidates"][0]["place_id"]
    else:
        raise ValueError(f"Cannot find {affiliation}.")
    # place_res = GMAPS.place(place_id, fields=['adr_address', 'address_component'])
    place_res = GMAPS.place(place_id, fields=['adr_address'])
    if place_res["status"] == "OK":
        place_res = place_res["result"]
    else:
        raise ValueError(f"Cannot find {affiliation} with id {place_id}.")
    # based on address_components
    # city = [ac for ac in place_res["address_components"]
    #         if "postal_town" in ac["types"] or "locality" in ac["types"]]
    # if len(city) > 0:
    #     city = city[0]["long_name"]
    # country = [ac for ac in place_res["address_components"] if "country" in ac["types"]]
    # if len(country) > 0:
    #     country = country[0]["long_name"]
    # based on adr_address
    adr = BS(place_res["adr_address"], "html.parser")
    city = adr.findAll("span", attrs={"class": "locality"})[0].text
    country = adr.findAll("span", attrs={"class": "country-name"})[0].text
    return city, country

