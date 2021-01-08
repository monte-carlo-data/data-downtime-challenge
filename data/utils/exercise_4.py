import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

def show_reports(df, timestamps, metric: str):
  plt.figure(figsize=(20, 10))
  plt.bar(all_days, height=df[metric])
  for t in timestamps: plt.axvline(x = t, color = 'r')
  plt.show()

all_days = []
date = datetime(2020, 1, 1)
for _ in range(350):
    all_days.append(date.strftime("%Y-%m-%d"))
    date += timedelta(days=1)
all_days = pd.Index(all_days)

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

  fig, ax = plt.subplots(figsize=(20, 10))
  ax.plot(range(15), precisions, label="Precision")
  ax.plot(range(15), recalls, label="Recall")
  ax.plot(range(15), f_scores, label="F1 Score")
  plt.xlabel("THRESHOLD_DAYS")
  legend = ax.legend(fontsize="x-large")
  plt.show()

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

  fig, ax = plt.subplots(figsize=(20, 10))
  ax.plot(range(15), f05, label="F0.5")
  ax.plot(range(15), f2, label="F2")
  ax.plot(range(15), f1, label="F1")
  plt.xlabel("THRESHOLD_DAYS")
  legend = ax.legend(fontsize="x-large")
  plt.show()