import sqlite3
import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect("TestDB.db")
c = conn.cursor()

read_clients = pd.read_csv(r"C:\Users\Ron\Desktop\Client\Client_14-JAN-2019.csv")
read_clients.to_sql(
    "CLIENTS", conn, if_exists="append", index=False
)  # Insert the values from the csv file into the table 'CLIENTS'

read_country = pd.read_csv(r"C:\Users\Ron\Desktop\Client\Country_14-JAN-2019.csv")
read_country.to_sql(
    "COUNTRY", conn, if_exists="replace", index=False
)  # Replace the values from the csv file into the table 'COUNTRY'

# When reading the csv:
# - Place 'r' before the path string to read any special characters, such as '\'
# - Don't forget to put the file name at the end of the path + '.csv'
# - Before running the code, make sure that the column names in the CSV files match with the column names in the tables created and in the query below
# - If needed make sure that all the columns are in a TEXT format

c.execute(
    """
INSERT INTO DAILY_STATUS (Client_Name,Country_Name,Date)
SELECT DISTINCT clt.Client_Name, ctr.Country_Name, clt.Date
FROM CLIENTS clt
LEFT JOIN COUNTRY ctr ON clt.Country_ID = ctr.Country_ID
          """
)

c.execute(
    """
SELECT DISTINCT *
FROM DAILY_STATUS
WHERE Date = (SELECT max(Date) FROM DAILY_STATUS)
          """
)

# print(c.fetchall())

df = DataFrame(c.fetchall(), columns=["Client_Name", "Country_Name", "Date"])
print(
    df
)  # To display the results after an insert query, you'll need to add this type of syntax above: 'c.execute(''' SELECT * from latest table ''')

df.to_sql(
    "DAILY_STATUS", conn, if_exists="append", index=False
)  # Insert the values from the INSERT QUERY into the table 'DAILY_STATUS'

# export_csv = df.to_csv (r'C:\Users\Ron\Desktop\Client\export_list.csv', index = None, header=True) # Uncomment this syntax if you wish to export the results to CSV. Make sure to adjust the path name
# Don't forget to add '.csv' at the end of the path (as well as r at the beg to address special characters)


import csv, sqlite3

con = sqlite3.connect(":memory:")  # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE t (col1, col2);")  # use your column names here

with open("data.csv", "r") as fin:  # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)  # comma is default delimiter
    to_db = [(i["col1"], i["col2"]) for i in dr]

cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()
