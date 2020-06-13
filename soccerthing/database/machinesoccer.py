import sqlite3
import pandas as pd
from pandas import DataFrame
import math
import scipy
from scipy.stats import poisson
import datetime
import pytz


# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect("soccer.db")
# creating a cursor
c = conn.cursor()

# c.execute("PRAGMA table_info(soccerstats2)")
# main = c.fetchall()
# print(main)
def insert_into_db_tables():

    conn = sqlite3.connect("soccer.db")
    # c = conn.cursor()

    read_teams = pd.read_csv(
        r"C:\Users\BRUVUSKY\Desktop\development\home.csv",
        names=["Position", "Team", "GP", "W", "D", "L", "GF", "GA", "GD", "PTS"],
        header=None,
    )

    read_teams.to_sql(
        "homestats", conn, if_exists="append", index=False
    )  # Insert the values from the csv file into the table 'soccerstats'

    read_teams = pd.read_csv(
        r"C:\Users\BRUVUSKY\Desktop\development\away.csv",
        names=["Position", "Team", "GP", "W", "D", "L", "GF", "GA", "GD", "PTS"],
        header=None,
    )

    read_teams.to_sql(
        "awaystats", conn, if_exists="append", index=False
    )  # Insert the values from the csv file into the table 'soccerstats'

    print("command executed succesfully")
    conn.commit()
    conn.close()


# create hometable
# create awaytabletable


# c.execute(
#     """ CREATE TABLE homestats(
#     position integer,
#     team text,
#     gp integer,
#     w integer,
#     d  integer,
#     l   integer,
#     gf  integer,
#     ga  integer,
#     gd integer,
#     Pts integer
# )"""
# )
def clear_tables_function():
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute("DELETE  FROM  'homestats'")
    c.execute("DELETE  FROM  'awaystats'")
    print("command executed succesfully")
    conn.commit()
    conn.close()


def drop_prediction_table():
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute("DROP TABLE 'finalprediction' ")
    print("command executed succesfully")
    conn.commit()
    conn.close()


def clear_prediction_table():
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute("DELETE FROM 'finalprediction' ")
    print("command executed succesfully")
    conn.commit()
    conn.close()


def clear_item_in_prediction_table(id):
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute("DELETE  FROM 'finalprediction' WHERE rowid = (?) ", (id,))
    print("command executed succesfully")
    conn.commit()
    conn.close()


def create_prediction_table():
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute(
        """ CREATE TABLE finalprediction(
        Date  text, 
        Home_pg integer,
        Away_pg integer,   
        Hometeam text ,
        Awayteam text,
        homewinodds integer,
        Drawodds integer,
        Awaywinodds integer,
        Over25  integer,
        Under25  integer,
        bttsyes integer,
        bttsno  integer
    )"""
    )
    print("command executed succesfully")
    conn.commit()
    conn.close()


# many_teams = [
#     ("Hamburger SV", "13", "9", "2", "2", "27", "9", "18", "29"),
#     ("Heidenheim", "14", "8", "4", "2", "23", "11", "12", "28"),
#     ("Sankt Pauli", "15", "7", "5", "3", "21", "12", "9", "26"),
#     ("Bielefeld", "13", "6", "6", "1", "23", "11", "12", "24"),
#     ("Darmstadt", "14", "5", "8", "1", "22", "14", "8", "23"),
# ]
# c.executemany("INSERT INTO soccerstats VALUES(?,?,?,?,	?,	?,	?,	?,?)", many_teams)


def query_tables_function(Position, Position1):
    global position, position1
    position = Position
    position1 = Position1

    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    today = datetime.date.today()
    query_tables_function.leo = str(today)
    # print(query_tables_function.leo)
    c.execute("SELECT * FROM 'homestats' WHERE position = (?) ", (Position,))
    hometeam = c.fetchone()
    # print(hometeam)
    query_tables_function.home_team_playing = hometeam[1]
    c.execute("SELECT  SUM(gp) FROM  'homestats' ")
    gamesplayed = c.fetchone()
    # print(gamesplayed)
    c.execute("SELECT  SUM(gf) FROM  'homestats' ")
    goalsfor = c.fetchone()
    # print(goalsfor)
    c.execute("SELECT  SUM(ga) FROM 'homestats' ")
    goalsagainist = c.fetchone()
    # print(goalsagainist)
    c.execute("SELECT * FROM 'awaystats' WHERE position = (?) ", (Position1,))
    awayteam = c.fetchone()
    # print(awayteam)
    query_tables_function.away_team_playing = awayteam[1]
    H_gf_pergame = hometeam[6] / hometeam[2]
    # print(H_gf_pergame)

    H_ga_pergame = hometeam[7] / hometeam[2]
    # print(H_ga_pergame)

    A_gf_pergame = awayteam[6] / awayteam[2]
    # print(A_gf_pergame)

    A_ga_pergame = awayteam[7] / awayteam[2]
    # print(A_ga_pergame)

    goals_for_per_homematch = goalsfor[0] / gamesplayed[0]
    # print(goals_for_per_homematch)

    goals_againist_per_homematch = goalsagainist[0] / gamesplayed[0]
    # print(goals_againist_per_homematch)

    homeatt = H_gf_pergame / goals_for_per_homematch
    # print(homeatt)

    homedefence = H_ga_pergame / goals_againist_per_homematch
    # print(homedefence)

    awayatt = A_gf_pergame / goals_againist_per_homematch
    # print(awayatt)

    awaydiffence = A_ga_pergame / goals_for_per_homematch
    # print(awaydiffence)

    home_probable_goal = homeatt * awaydiffence * goals_for_per_homematch
    away_probable_goal = awayatt * homedefence * goals_againist_per_homematch

    query_tables_function.hpg = str((round(home_probable_goal, 4)))
    # print("predicted home score " + query_tables_function.hpg)

    query_tables_function.apg = str((round(away_probable_goal, 4)))
    # print("predicted away score " + query_tables_function.apg)
    goals = [0, 1, 2, 3, 4, 5]

    home_score_0 = poisson.pmf(goals[0], home_probable_goal)
    home_score_1 = poisson.pmf(goals[1], home_probable_goal)
    home_score_2 = poisson.pmf(goals[2], home_probable_goal)
    home_score_3 = poisson.pmf(goals[3], home_probable_goal)
    home_score_4 = poisson.pmf(goals[4], home_probable_goal)
    home_score_5 = poisson.pmf(goals[5], home_probable_goal)

    away_score_0 = poisson.pmf(goals[0], away_probable_goal)
    away_score_1 = poisson.pmf(goals[1], away_probable_goal)
    away_score_2 = poisson.pmf(goals[2], away_probable_goal)
    away_score_3 = poisson.pmf(goals[3], away_probable_goal)
    away_score_4 = poisson.pmf(goals[4], away_probable_goal)
    away_score_5 = poisson.pmf(goals[5], away_probable_goal)

    under25 = 1 / (
        (home_score_0 * away_score_0)
        + (away_score_1 * home_score_0)
        + (home_score_1 * away_score_0)
        + (away_score_1 * home_score_1)
        + (away_score_2 * home_score_0)
        + (away_score_0 * home_score_2)
    )

    over25 = 1 / (1 - (1 / under25))

    Both_TO_Score_No = 1 / (
        (home_score_0 * away_score_0)
        + (home_score_0 * away_score_1)
        + (home_score_0 * away_score_2)
        + (home_score_0 * away_score_3)
        + (home_score_0 * away_score_4)
        + (home_score_0 * away_score_5)
        + (home_score_1 * away_score_0)
        + (home_score_2 * away_score_0)
        + (home_score_3 * away_score_0)
        + (home_score_4 * away_score_0)
        + (home_score_5 * away_score_0)
    )

    Both_TO_Score = 1 / (1 - (1 / Both_TO_Score_No))

    homewin = 1 / (
        (home_score_1 * away_score_0)
        + (home_score_2 * away_score_0)
        + (home_score_3 * away_score_0)
        + (home_score_4 * away_score_0)
        + (home_score_5 * away_score_0)
        + (home_score_2 * away_score_1)
        + (home_score_3 * away_score_1)
        + (home_score_3 * away_score_2)
        + (home_score_4 * away_score_1)
        + (home_score_4 * away_score_2)
        + (home_score_4 * away_score_3)
        + (home_score_5 * away_score_1)
        + (home_score_5 * away_score_2)
        + (home_score_5 * away_score_3)
        + (home_score_5 * away_score_4)
    )

    draw = 1 / (
        (home_score_1 * away_score_1)
        + (away_score_0 * home_score_0)
        + (home_score_2 * away_score_2)
        + (home_score_3 * away_score_3)
        + (home_score_4 * away_score_4)
        + (home_score_5 * away_score_5)
    )

    Awaywin = 1 / (
        (home_score_0 * away_score_1)
        + (home_score_0 * away_score_2)
        + (home_score_0 * away_score_3)
        + (home_score_0 * away_score_4)
        + (home_score_0 * away_score_5)
        + (home_score_1 * away_score_2)
        + (home_score_1 * away_score_3)
        + (home_score_2 * away_score_3)
        + (home_score_1 * away_score_4)
        + (home_score_2 * away_score_4)
        + (home_score_3 * away_score_4)
        + (home_score_1 * away_score_5)
        + (home_score_2 * away_score_5)
        + (home_score_3 * away_score_5)
        + (home_score_4 * away_score_5)
    )
    query_tables_function.hm = str((round(homewin, 2)))
    # print("Home win Odd  " + query_tables_function.hm)

    query_tables_function.d = str((round(draw, 2)))
    # print("Draw Odd  " + query_tables_function.d)

    query_tables_function.Aw = str((round(Awaywin, 2)))
    # print("Away win Odd  " + query_tables_function.Aw)

    query_tables_function.btts = str((round(Both_TO_Score, 2)))
    # print("Btts Yes " + query_tables_function.btts)

    query_tables_function.btts_no = str((round(Both_TO_Score_No, 2)))
    # print("Btts No " + query_tables_function.btts_no)

    query_tables_function.ov25 = str((round(over25, 2)))
    # print("Ov2.5 " + query_tables_function.ov25)

    query_tables_function.un25 = str((round(under25, 2)))
    # print("Un2.5 " + query_tables_function.un25)

    # ff = 1 / (1 - ((1 / draw) + (1 / homewin)))
    # print(ff)

    conn.commit()
    conn.close()
    # return (Position, Position1)


def append_finalpredictions_to_table():
    # global Position, Position1
    query_tables_function(position, position1)
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    my_prediction = [
        (query_tables_function.leo),
        (query_tables_function.hpg),
        (query_tables_function.apg),
        (query_tables_function.home_team_playing),
        (query_tables_function.away_team_playing),
        (query_tables_function.hm),
        (query_tables_function.d),
        (query_tables_function.Aw),
        (query_tables_function.btts),
        (query_tables_function.btts_no),
        (query_tables_function.ov25),
        (query_tables_function.un25),
    ]
    c.executemany(
        "INSERT INTO finalprediction  VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (my_prediction,)
    )
    print("command executed succesfully")
    conn.commit()
    conn.close()
    # print(my_prediction)


def finalprediction_of_the_day():
    conn = sqlite3.connect("soccer.db")
    c = conn.cursor()
    c.execute(
        "SELECT rowid, Date, Hometeam, Awayteam, Home_pg, Away_pg FROM 'finalprediction' "
    )
    matches_predicted = c.fetchall()
    c.execute(
        "SELECT rowid,Date, Hometeam,Awayteam,homewinodds,Drawodds,Awaywinodds FROM 'finalprediction' "
    )
    matches_predicted1 = c.fetchall()
    c.execute(
        "SELECT rowid,Date, Hometeam,Awayteam,Over25,Under25 FROM 'finalprediction' "
    )
    matches_predicted2 = c.fetchall()
    c.execute(
        "SELECT rowid,Date, Hometeam,Awayteam,bttsyes,bttsno FROM 'finalprediction' "
    )
    matches_predicted3 = c.fetchall()
    for match in matches_predicted:
        print(match)
    for match1 in matches_predicted1:
        print(match1)
    for match2 in matches_predicted2:
        print(match2)
    for match3 in matches_predicted3:
        print(match3)
    print("command executed succesfully")
    conn.commit()
    conn.close()


def perform_magic():
    query_tables_function("11", "1")
    append_finalpredictions_to_table()
    finalprediction_of_the_day()


# clear_item_in_prediction_table("10")
# insert_into_db_tables()
perform_magic()
# finalprediction_of_the_day()
# clear_tables_function()


# create_prediction_table()
# clear_prediction_table()

# drop_prediction_table()


# print(away_score_1)
# print(away_score_2)
# print(home_score_1)
# c.execute("DROP table 'finalprediction' ")
# team = c.fetchone()
# teams = team[6]
# teams1 = team[7]
# result = teams[0] / (2)
# exact = poisson.pmf(1, 1.62345)
# print(exact)
# print(team)
# print(teams)

# print(teams1)
# print(result)

# for team in teams:
#     print(
#         team[0], team[1], team[2], team[3], team[4], team[5], team[6], team[7], team[8]
#     )
# print(c.fetchone())
# print(c.fetchmany(3))
# print("command executed succesfully")
# Datatypes:
# NULL
# INTEGER
# BLOB
# REAL
# TEXT

# commit the command
# conn.commit()
# close the connection
# conn.close()
