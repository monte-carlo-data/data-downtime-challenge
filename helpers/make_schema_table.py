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

def main():
  # load in data from Ex1.db to append
  conn = sqlite3.connect('Ex2.db')
  c = conn.cursor()
  ex1_df = pd.read_sql(
    "SELECT * FROM EXOPLANETS",
    conn
  )
  schema_table = pd.DataFrame()
  schema_table["date"] = ex1_df["date_added"].drop_duplicates()
  schema_table.reset_index(inplace=True)
  schema_table["schema"] = """[
    (0, '_id', 'TEXT', 0, None, 0),
    (1, 'distance', 'REAL', 0, None, 0),
    (2, 'g', 'REAL', 0, None, 0),
    (3, 'orbital_period', 'REAL', 0, None, 0),
    (4, 'avg_temp', 'REAL', 0, None, 0),
    (5, 'date_added', 'TEXT', 0, None, 0)
  ]"""
  schema_table.loc[schema_table["date"] >= "2020-07-19", "schema"] = """[
    (0, '_id', 'TEXT', 0, None, 0),
    (1, 'distance', 'REAL', 0, None, 0),
    (2, 'g', 'REAL', 0, None, 0),
    (3, 'orbital_period', 'REAL', 0, None, 0),
    (4, 'avg_temp', 'REAL', 0, None, 0),
    (5, 'date_added', 'TEXT', 0, None, 0),
    (6, 'eccentricity', 'REAL', 0, None, 0),
    (7, 'atmosphere', 'TEXT', 0, None, 0)
  ]"""

  print(schema_table)
  schema_table.drop(axis=1, labels="index", inplace=True)

  c.execute("DROP TABLE EXOPLANETS_SCHEMA")
  c.execute("""
    CREATE TABLE EXOPLANETS_SCHEMA(
      DATE TIMESTAMP_NTZ(6) NOT NULL,
      SCHEMA VARCHAR(16777216)
    )
  """)

  conn.commit()
  schema_table.to_sql("EXOPLANETS_SCHEMA", conn, if_exists='replace', index = False)

  c.execute("SELECT * FROM EXOPLANETS_SCHEMA")
  for row in c.fetchall():
    print(row)
    break

if __name__ == "__main__":
  main()
