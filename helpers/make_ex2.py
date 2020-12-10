#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ryan Othniel Kearns"
__maintainer__ = "Ryan Othniel Kearns"
__email__ = "rkearns@montecarlodata.com"

"""Create snapshots of a dataset for course participants to analyze.
"""

import numpy as np
import pandas as pd
import random
import sqlite3
import uuid
from datetime import datetime, timedelta
from tqdm import tqdm

random.seed("data downtime")

PROB_FULL_OUTAGE = 0.03
PROB_NULL_SPIKE = 0.03
NULL_SPIKE_SEVERITY = 0.95

def append_new_data(df):
  NUM_DAYS = 50
  date = datetime(2020, 7, 19)
  duplication_event, full_outage, null_spike, null_fields = 0, 0, 0, []
  for _ in tqdm(range(NUM_DAYS)):
    if random.random() <= PROB_FULL_OUTAGE: full_outage = random.randint(1, 7)
    if random.random() <= PROB_NULL_SPIKE:
      null_spike = random.randint(1, 7)
      null_fields = random.choices(
        ["distance", "g", "orbital_period", "avg_temp"],
        k=random.randint(1,4)
      )

    if full_outage > 0:
      date += timedelta(days=1)
      full_outage -= 1
      continue
    for i in range(random.randint(80, 120)):
      _id = uuid.uuid4()
      dist, g, orbital_period, avg_temp, eccentricity, atmosphere = None, None, None, None, None, None
      if random.random() <= 0.95: dist = abs(random.gauss(50, 50))
      if random.random() <= 0.85: g = abs(random.gauss(1, 5))
      if random.random() <= 0.75: orbital_period = abs(random.gauss(500, 300))
      if random.random() <= 0.6: avg_temp = abs(random.gauss(273, 50))
      if random.random() <= 0.75: eccentricity = random.random()
      if random.random() <= 0.4: atmosphere = random.choice(["O2", "N2", "CO2", "H2SO4"])

      if "dist" in null_fields and random.random() <= NULL_SPIKE_SEVERITY: dist = None
      if "g" in null_fields and random.random() <= NULL_SPIKE_SEVERITY: g = None
      if "orbital_period" in null_fields and random.random() <= NULL_SPIKE_SEVERITY: orbital_period = None
      if "avg_temp" in null_fields and random.random() <= NULL_SPIKE_SEVERITY: avg_temp = None

      df = df.append([{
        "_id": str(_id),
        "distance": dist,
        "g": g,
        "orbital_period": orbital_period,
        "avg_temp": avg_temp,
        "date_added": date.strftime("%Y-%m-%d"),
        "eccentricity": eccentricity,
        "atmosphere": atmosphere
      }])
    if null_spike > 0:
      null_spike -= 1
      if null_spike == 0: null_fields = []
    date += timedelta(days=1)

  return df

def main():
  # load in data from Ex1.db to append
  conn1 = sqlite3.connect('Ex1.db')
  ex1_df = pd.read_sql(
    "SELECT * FROM EXOPLANETS",
    conn1
  )
  # add in bogus NULL data for new fields
  ex1_df["eccentricity"] = None
  ex1_df["atmosphere"] = None

  ex2_df = append_new_data(ex1_df)
  ex2_df = ex2_df.reset_index(drop=True)
  print(ex2_df)

  conn = sqlite3.connect('Ex2.db')
  c = conn.cursor()

  # c.execute("""
  #   CREATE TABLE EXOPLANETS(
  #     _ID VARCHAR(16777216) NOT NULL,
  #     DISTANCE FLOAT,
  #     G FLOAT,
  #     ORBITAL_PERIOD FLOAT,
  #     AVG_TEMP FLOAT,
  #     DATE_ADDED TIMESTAMP_NTZ(6) NOT NULL,
  #     ECCENTRICITY FLOAT,
  #     ATMOSPHERE VARCHAR(16777216)
  #   )
  # """)
  # conn.commit()
  # ex2_df.to_sql("EXOPLANETS", conn, if_exists='replace', index = False)

  c.execute("SELECT * FROM EXOPLANETS")
  for row in c.fetchall():
    print(row)
    break

  # invent a "downstream" table
  downstream = pd.DataFrame(columns=["_id", "perihelion", "aphelion", "atmosphere", "habitability", "min_temp", "max_temp", "date_added"])
  for i, row in tqdm(ex2_df.iterrows(), total=ex2_df.shape[0]):
    p, a, h, min_temp, max_temp = np.nan, np.nan, 0, np.nan, np.nan
    if row["avg_temp"]:
      min_temp = random.random() * row["avg_temp"]
      max_temp = (1 + random.random()) * row["avg_temp"]
      if row["eccentricity"]:
        if random.random() <= 0.85: min_temp = 0
        if random.random() <= 0.85: max_temp = 999999
    if row["eccentricity"] and row["orbital_period"]:
      p = row["eccentricity"] * row["orbital_period"] * 0.2
      a = (2 - row["eccentricity"]) * row["orbital_period"] * 0.2
    h = random.random()
    if min_temp == 0: h = 0
    if max_temp == 999999: h = 0
    downstream = downstream.append([{
      "_id": row["_id"],
      "perihelion": p,
      "aphelion": a,
      "atmosphere": row["atmosphere"],
      "habitability": h,
      "min_temp": min_temp,
      "max_temp": max_temp,
      "date_added": row["date_added"]
    }])
  downstream = downstream.reset_index(drop=True)
  print(downstream)

  c.execute("DROP TABLE HABITABLES")
  c.execute("""
    CREATE TABLE HABITABLES(
      _ID VARCHAR(16777216) NOT NULL,
      MIN_TEMP FLOAT,
      MAX_TEMP FLOAT,
      HABITABILITY FLOAT NOT NULL,
      PERIHELION FLOAT,
      APHELION FLOAT,
      ATMOSPHERE VARCHAR(16777216)
    )
  """)
  conn.commit()
  downstream.to_sql("HABITABLES", conn, if_exists='replace', index = False)

  c.execute("SELECT * FROM HABITABLES")
  for row in c.fetchall():
    print(row)
    break

if __name__ == "__main__":
  main()
