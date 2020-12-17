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
for _ in range(200):
  all_days.append(date.strftime("%Y-%m-%d"))
  date += timedelta(days=1)
all_days = pd.Index(all_days)