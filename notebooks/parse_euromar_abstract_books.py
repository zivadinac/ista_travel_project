from os import makedirs
from tqdm import tqdm
import numpy as np
from argparse import ArgumentParser
from os.path import join
from bs4 import BeautifulSoup as BS, NavigableString
from pandas import DataFrame as DF, concat, read_csv
from notebooks.utils import find_city_country

args = ArgumentParser()
args.add_argument("--in_dir", "-i", default="raw_data/euromar_abstract_books/")
args.add_argument("--out_dir", "-o", default="preprocessed_data/euromar_abstract_books/")
args = args.parse_args()

makedirs(args.out_dir, exist_ok=True)

# 2017
ab2017_path = join(args.in_dir, "abstracts_2017-converted.html")
with open(ab2017_path) as fp:
    ab2017 = BS(fp, "html.parser")
    author_p = ab2017.findAll('p', attrs={"class": "s5"})
    titles = [a.findPreviousSibling().text for a in author_p]
    authors = [a.text.split(',')[0] for a in author_p]
    affiliations_ = [' '.join(a.text.split(',')[1:]) for a in author_p]
    affiliations, cities, countries = [], [], []
    for af in affiliations_:
        afs = af.split()
        try:
            int(afs[-1])
            affiliations.append(' '.join(afs[:-1]))
        except:
            affiliations.append(af)
        cities.append(None)
        countries.append(None)
    ab2017_DF = DF({"year": 2017,
                    "authors": authors,
                    "titles": titles,
                    "affiliations": affiliations,
                    "city": cities, "country": countries})
    ab2017_DF.to_csv(join(args.out_dir, "abstracts_2017.csv"))
# 2018
ab2018_path = join(args.in_dir, "abstracts_2018-converted.html")
with open(ab2018_path) as fp:
    ab2018 = BS(fp, "html.parser")
    author_p = ab2018.findAll('p', attrs={"class": "s10"})
    authors = []
    countries = []
    for a in author_p:
        pp = a.text.find('(')
        authors.append(a.text[:pp].strip())
        countries.append(a.text[pp:].strip(" ()"))
    titles = [a.findPreviousSibling().text.split('|')[-1].strip() for a in author_p]
    ab2018_DF = DF({"year": 2018,
                    "authors": authors,
                    "titles": titles,
                    "affiliations": None,
                    "city": None, "country": countries})
    ab2018_DF.to_csv(join(args.out_dir, "abstracts_2018.csv"))
# 2019
ab2019_path = join(args.in_dir, "Euromar_2019_abstracts.html")
with open(ab2019_path) as fp:
    ab2019 = BS(fp, "html.parser")
    hrs = ab2019.findAll("hr")
    titles, affiliations, authors = [], [], []
    for hr_p, hr_n in zip(hrs[:-1], hrs[1:]):
        # titles
        p_b = hr_p.findNextSiblings("b", limit=5)
        n_b = hr_n.findPreviousSiblings("b", limit=5)
        common_b = [b for b in set(p_b).intersection(n_b)]
        if len(common_b) <= 1:
            common_b = p_b[:4]
        full_title = ' '.join([c.text.strip() for c in common_b])
        bb = common_b[0]
        # affiliations
        p_i = bb.findNextSiblings("i", limit=5)
        n_i = hr_n.findPreviousSiblings("i", limit=10)
        common_i = set(n_i).intersection(p_i)
        common_i = [i for i in common_i if "Auditorium" not in i.text]
        if len(common_i) <= 1:
            continue
        ii = common_i[-1]
        all_affiliations = ' '.join([c.text.strip() for c in common_i])
        # authors
        s_ii = [p for p in list(ii.previous_siblings)[:100]
                if isinstance(p, NavigableString)]
        s_bb = [p for p in list(bb.next_siblings)[:100]
                if isinstance(p, NavigableString)]
        s = list(set(s_bb).intersection(s_ii))

        try:
            all_authors = [ss.strip() for ss in s if '*' in ss][0]
        except:
            longest = np.argmax([len(aa) for aa in s])
            all_authors = s[longest].strip()

        try:
            ast_idx = all_authors.find('*')
            main_author = all_authors[:ast_idx].split(',')[-1]
        except:
            main_author = all_authors
            ast_idx = None

        try:
            aff_idx = int(all_authors[ast_idx+2])
            affl = all_affiliations.split(',')[aff_idx-1]
        except:
            affl = all_affiliations

        titles.append(full_title)
        affiliations.append(affl)
        authors.append(main_author)

    ab2019_DF = DF({"year": 2019,
                    "authors": authors,
                    "titles": titles,
                    "affiliations": affiliations,
                    "city": None, "country": None})
    ab2019_DF.to_csv(join(args.out_dir, "abstracts_2019.csv"))
# 2022
ab2022_path = join(args.in_dir, "abstracts_2022-converted.html")
with open(ab2022_path) as fp:
    ab2022 = BS(fp, "html.parser")
    trs = ab2022.findAll('tr')
    titles, authors, affiliations, cities, countries = [], [], [], [], []
    trs = [tr for tr in trs if len(list(tr.children)) == 6]
    for tr in trs:
        ctxt = [c.text for c in tr.children]
        if ctxt[0].startswith("Paper #"):
            continue
        titles.append(ctxt[1])
        authors.append(ctxt[2])
        countries.append(ctxt[3])
        affiliations.append(None)
        cities.append(None)
    ab2022_DF = DF({"year": 2022,
                    "authors": authors,
                    "titles": titles,
                    "affiliations": affiliations,
                    "city": cities, "country": countries})
    ab2022_DF.to_csv(join(args.out_dir, "abstracts_2022.csv"))
# 2023
ab2023_path = join(args.in_dir, "abstracts_2023.html")
with open(ab2023_path) as fp:
    ab2023 = BS(fp, "html.parser")
    pages = ab2023.findAll("div", attrs={"class": "c x0 y1 w2 h2"})
    affiliations = []
    authors = []
    titles = []
    for p in pages:
        p_children = list(p.children)[:10]
        for cn, c in enumerate(p.children):
            aff = c.text.strip()
            if "University" in aff or "Institute" in aff\
                    or "Department" in aff or "UC" in aff\
                    or "School" in aff:
                affiliations.append(aff)
                print("==============")
                print(aff)
                print("==============")
                aff_titles = []
                for s in c.findPreviousSiblings():
                    txt = s.text.strip()
                    if txt.startswith("TUT") or txt.startswith("PL")\
                            or txt.startswith("INV") or txt.startswith("PT")\
                            or txt.startswith("P-") or "Prize" in txt:
                        aff_titles.append(txt)
                        print("==============")
                        print(txt)
                        print("==============")
                titles.append(None if len(aff_titles) == 0 else aff_titles[-1])
                aff_authors = []
                for s in c.findPreviousSiblings():
                    txt = s.text.strip()
                    if "Dr " in txt or "Professor " in txt\
                            or "Mr " in txt or "Ms " in txt\
                            or "Mrs " in txt or "Miss " in txt:
                        aff_authors.append(txt)
                        print("==============")
                        print(txt)
                        print("==============")
                authors.append(None if len(aff_authors) == 0 else aff_authors[-1])
                break
    ab2023_DF = DF({"year": 2023,
                    "authors": authors,
                    "titles": titles,
                    "affiliations": affiliations,
                    "city": None, "country": None})
    ab2023_DF.to_csv(join(args.out_dir, "abstracts_2023.csv"))

# all together
ab_DF = concat([ab2017_DF, ab2018_DF, ab2019_DF, ab2022_DF, ab2023_DF], ignore_index=True)

# add missing GEO information
all_countries = read_csv(join(args.in_dir, "WorldCountriesList.csv2"))
# missing countries in the list
all_countries.loc[len(all_countries.index)] = ['The Netherlands', "NLD", "Amsterdam", "Europe"]
all_countries.loc[len(all_countries.index)] = ['Russian Federation', "RUS", "Moscow", "Europe"]
all_countries.loc[len(all_countries.index)] = ['Deutschland', "DEU", "Berlin", "Europe"]
all_countries.loc[len(all_countries.index)] = ['Czech Republic', "CZK", "Prague", "Europe"]
all_countries.loc[len(all_countries.index)] = ['Wielka Brytania', "GBR", "London", "Europe"]
all_countries.loc[len(all_countries.index)] = ['Republic of Korea', "KOR", "Seoul", "Asia"]

# use google to fill missing countries and cities
ab_DF["country_check"] = True
for index, (_, _, _, aff, city, country, cc) in tqdm(ab_DF.iterrows(), total=len(ab_DF)):
    if type(city) == str:
        continue
    if aff is not None and aff is not np.nan:
        try:
            g_city, g_country = find_city_country(aff)
        except Exception as e:
            print(e)
            continue
        cc_ = (country is None or country is np.nan) or (g_country == country)
        ab_DF.loc[index, "city"] = g_city
        ab_DF.loc[index, "country_check"] = cc_
        ab_DF.loc[index, "country"] = g_country
    elif city is not None and country is None:
        try:
            g_city, g_country = find_city_country(city)
        except Exception as e:
            print(e)
            continue
        ab_DF.loc[index, "country"] = g_country
    elif country is not None and country is not np.nan:
        try:
            capital = all_countries[all_countries.Country == country.strip()]["Capital-City"].item()
            ab_DF.loc[index, "city"] = capital
        except Exception as e:
            print(e)
            continue
    else:
        continue
ab_DF.to_csv(join(args.out_dir, "abstracts.csv"), index=False)
ab_DF = read_csv(join(args.out_dir, "abstracts.csv"), index_col=0)

"""
for mc in ["The Netherlands", "Russian Federation", "Deutschland", "Czech Republic", "Wielka Brytania", "Republic of Korea"]:
    try:
        capital = all_countries[all_countries.Country == mc]["Capital-City"].item()
        ab_DF.loc[ab_DF.country == mc, "city"] = capital
    except Exception as e:
        print(e)
        continue
"""
visitors = ab_DF[["year", "city", "country", "affiliations"]]
visitors.to_csv(join(args.out_dir, "visitors.csv"), index=False)
visitors_good = visitors.dropna(subset=["city"])
visitors_good.to_csv(join(args.out_dir, "visitors_only_good.csv"), index=False)

