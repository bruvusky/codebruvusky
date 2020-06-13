import requests

import csv
from bs4 import BeautifulSoup
import urls
from urls import (
    poland2,
    portugal,
    israel2,
    germany,
    denmark,
    denmark2,
    austria2,
    belarus,
    austria,
    poland,
    greece,
    croatia,
    hungary,
    germany2,
    spain,
    spain2,
    turkey,
    italy,
)

page = requests.get(italy)
soup = BeautifulSoup(page.content, "html.parser")
filename = "home.csv"
filename1 = "away.csv"
csv_writer = csv.writer(open(filename, "w"))
csv_writer1 = csv.writer(open(filename1, "w"))
home_stat = soup.find(id="h2h-team1")
away_stat = soup.find(id="h2h-team2")
home_table = home_stat.find("table", id="btable")
away_table = away_stat.find("table", id="btable")
# print (home_table)

headers = []
for th in home_table.find("tr", class_="even").find_all("th"):
    headers.append(th.text.strip())
print(" {}".format(" , ".join(headers)))
# csv_writer.writerow(headers)


rows = []
for tr in home_table.find_all("tr", class_="odd"):
    cells = []
    # grab all td tags in this table row
    tds = tr.find_all("td")
    # if len(tds) == 0:
    # [1:]
    # if no td tags, search for th tags
    # can be found especially in wikipedia tables below the table
    # ths = tr.find_all("th")
    # for th in ths:
    # cells.append(th.text.strip())
    # else:
    # use regular td tags
    for td in tds:
        cells.append(td.text.strip())
    rows.append(cells)
    if cells:  # print(cells)
        print("{}".format(" , ".join(cells)))
        csv_writer.writerow(cells)
        continue

headers1 = []
for th in away_table.find("tr", class_="even").find_all("th"):
    headers1.append(th.text.strip())
print(" {}".format(" , ".join(headers)))
# csv_writer1.writerow(headers1)

rows1 = []
for tr in away_table.find_all("tr", class_="odd"):
    cells1 = []
    # grab all td tags in this table row
    tds1 = tr.find_all("td")
    # if len(tds) == 0:
    # [1:]
    # if no td tags, search for th tags
    # can be found especially in wikipedia tables below the table
    # ths = tr.find_all("th")
    # for th in ths:
    # cells.append(th.text.strip())
    # else:
    # use regular td tags
    for td in tds1:
        cells1.append(td.text.strip())
    rows1.append(cells1)
    if cells1:  # print(cells)
        print("{}".format(" , ".join(cells1)))
        csv_writer1.writerow(cells1)
        continue


#  .headers on
#  .mode csv
#  .output fpr.csv
#  SELECT * FROM finalprediction;
#  .quit
