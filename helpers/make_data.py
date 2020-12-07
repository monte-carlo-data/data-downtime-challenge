#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ryan Othniel Kearns"
__maintainer__ = "Ryan Othniel Kearns"
__email__ = "rkearns@montecarlodata.com"

"""TODO DEPRECATED
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

NUM_SAMPLES = 400

dist = np.random.normal(loc=50000, scale=10000, size=NUM_SAMPLES)
start_date = datetime(2020, 11, 1)
timestamps = np.array([start_date + timedelta(hours=i) for i in range(NUM_SAMPLES)])
df = pd.DataFrame(columns=["table_id", "metric", "field"])
df["timestamp"] = timestamps
df["value"] = dist
df["table_id"] = "test_table_0"
df["metric"] = "row_count"
df["field"] = None

# introduce anomalies
df.loc[107:109, ["value"]] /= 2
df.loc[110, ["value"]] = 157
df.loc[111:115, ["value"]] = 0

df.to_csv("data/ex_1.csv")
