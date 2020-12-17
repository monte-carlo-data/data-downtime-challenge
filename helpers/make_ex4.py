#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ryan Othniel Kearns"
__maintainer__ = "Ryan Othniel Kearns"
__email__ = "rkearns@montecarlodata.com"

"""Create snapshots of a dataset for course participants to analyze.
"""

import pandas as pd
import random
import sqlite3
import uuid
from datetime import datetime, timedelta
from tqdm import tqdm

random.seed("data downtime")

PROB_FULL_OUTAGE = 0.03
PROB_NULL_SPIKE = 0.03
PROB_DUPLICATION = 0.05
NULL_SPIKE_SEVERITY = 0.95

def make_data():
  NUM_DAYS = 500
  df = pd.DataFrame(columns=["_id", "distance", "g", "orbital_period", "avg_temp", "eccentricity", "atmosphere", "date_added"])
  date = datetime(2020, 1, 1)
  duplication_event, full_outage, null_spike, null_fields = 0, 0, 0, []
  for _ in tqdm(range(NUM_DAYS)):
    if random.random() <= PROB_FULL_OUTAGE: full_outage = abs(int(random.gauss(1, 8)))
    if random.random() <= PROB_NULL_SPIKE:
      null_spike = random.randint(1, 7)
      null_fields = random.choices(
        ["distance", "g", "orbital_period", "avg_temp", "eccentricity", "atmosphere"],
        k=random.randint(1,6)
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

  conn = sqlite3.connect('Ex4.db')
  c = conn.cursor()

  c.execute("""
    CREATE TABLE EXOPLANETS(
      _ID VARCHAR(16777216) NOT NULL,
      DISTANCE FLOAT,
      G FLOAT,
      ORBITAL_PERIOD FLOAT,
      AVG_TEMP FLOAT,
      DATE_ADDED TIMESTAMP_NTZ(6) NOT NULL,
      ECCENTRICITY FLOAT,
      ATMOSPHERE VARCHAR(16777216)
    )
  """)
  conn.commit()
  df.to_sql("EXOPLANETS", conn, if_exists='replace', index = False)

  c.execute("SELECT * FROM EXOPLANETS")
  for row in c.fetchall():
    print(row)
    return

if __name__ == "__main__":
  make_data()