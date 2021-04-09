#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ryan Othniel Kearns"
__maintainer__ = "Ryan Othniel Kearns"
__email__ = "rkearns@montecarlodata.com"

"""Utilities for Monte Carlo's O'Reilly Course notebooks.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

def get_days_index(n: int):
  all_days = []
  date = datetime(2020, 1, 1)
  for _ in range(n):
    all_days.append(date.strftime("%Y-%m-%d"))
    date += timedelta(days=1)
  return pd.Index(all_days)

VALID_OUTAGE_DATES = set([
  "2020-01-26",
  "2020-04-01",
  "2020-04-20",
  "2020-05-16",
  "2020-07-12",
  "2020-08-29",
  "2020-10-19",
  "2021-01-05",
  "2021-04-13"
])

def show_threshold_plot(conn):
  precisions, recalls, f_scores = [], [], []
  for i in range(15):
    SQL = """
      WITH RC_UPDATES AS(
          SELECT
              DATE_ADDED,
              COUNT(*) AS ROWS_ADDED
          FROM
              EXOPLANETS
          GROUP BY
              DATE_ADDED
      ),
      NUM_DAYS_UPDATES AS(
          SELECT
              DATE_ADDED,
              JULIANDAY(DATE_ADDED) - JULIANDAY(LAG(DATE_ADDED) OVER(ORDER BY DATE_ADDED)) AS DAYS_SINCE_UPDATE
          FROM
              RC_UPDATES
      )
      SELECT
          *
      FROM
          NUM_DAYS_UPDATES
      WHERE
          DAYS_SINCE_UPDATE > {}
      """.format(i)
    freshness_anoms = pd.read_sql_query(SQL, conn)
    freshness_anoms = freshness_anoms \
    .rename(columns={clmn: clmn.lower() for clmn in freshness_anoms.columns})
    TP = len(set(freshness_anoms["date_added"]).intersection(VALID_OUTAGE_DATES))
    FP = len(set(freshness_anoms["date_added"]).difference(VALID_OUTAGE_DATES))
    FN = len(VALID_OUTAGE_DATES.difference(set(freshness_anoms["date_added"])))
    if FP == 0: precision = 1
    else: precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    precisions.append(precision)
    recalls.append(recall)
    f_scores.append((2 * precision * recall) / (precision + recall))

  fig = make_subplots()
  fig.add_trace(go.Scatter(x=list(range(15)), y=precisions, name="Precision", mode="lines"))
  fig.add_trace(go.Scatter(x=list(range(15)), y=recalls, name="Recall", mode="lines"))
  fig.add_trace(go.Scatter(x=list(range(15)), y=f_scores, name="F1 Score", mode="lines"))
  fig.update_xaxes(title="THRESHOLD_DAYS")
  fig.show()

def show_f_plots(conn):
  f1, f05, f2 = [], [], []
  for i in range(15):
    SQL = """
      WITH RC_UPDATES AS(
          SELECT
              DATE_ADDED,
              COUNT(*) AS ROWS_ADDED
          FROM
              EXOPLANETS
          GROUP BY
              DATE_ADDED
      ),
      NUM_DAYS_UPDATES AS(
          SELECT
              DATE_ADDED,
              JULIANDAY(DATE_ADDED) - JULIANDAY(LAG(DATE_ADDED) OVER(ORDER BY DATE_ADDED)) AS DAYS_SINCE_UPDATE
          FROM
              RC_UPDATES
      )
      SELECT
          *
      FROM
          NUM_DAYS_UPDATES
      WHERE
          DAYS_SINCE_UPDATE > {}
      """.format(i)
    freshness_anoms = pd.read_sql_query(SQL, conn)
    freshness_anoms = freshness_anoms \
    .rename(columns={clmn: clmn.lower() for clmn in freshness_anoms.columns})
    TP = len(set(freshness_anoms["date_added"]).intersection(VALID_OUTAGE_DATES))
    FP = len(set(freshness_anoms["date_added"]).difference(VALID_OUTAGE_DATES))
    FN = len(VALID_OUTAGE_DATES.difference(set(freshness_anoms["date_added"])))
    if FP == 0: precision = 1
    else: precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1.append((2 * precision * recall) / (precision + recall))
    f05.append(((1 + 0.5**2) * precision * recall) / (0.5**2 * precision + recall))
    f2.append(((1 + 2**2) * precision * recall) / (2**2 * precision + recall))

  fig = make_subplots()
  fig.add_trace(go.Scatter(x=list(range(15)), y=f05, name="F0.5", mode="lines"))
  fig.add_trace(go.Scatter(x=list(range(15)), y=f2, name="F2", mode="lines"))
  fig.add_trace(go.Scatter(x=list(range(15)), y=f1, name="F1", mode="lines"))
  fig.update_xaxes(title="THRESHOLD_DAYS")
  fig.show()
