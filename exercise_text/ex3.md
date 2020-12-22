# Data Downtime Challenge | Exercise 3

## 0. Setup

## 1. Introduction

In the last exercise, we looked at incidents spanning multiple tables in a database. Yet, we've still only been looking at _individual_ metrics like the row count, rate of null values, and so on. In practice, many genuine data downtime incidents involve _conjunctions_ of events across multiple upstream and downstream tables. In this exercise, we practice crafting single queries that can handle such conjunctive events.

## 2. Data

In this exercise, we'll continue to use the `EXOPLANETS`, `HABITABLES`, and `EXOPLANETS_SCHEMA` tables. There is also a `HABITABLES_SCHEMA` table, and all four contain additional entries beyond those in exercise 2.

## 3. Exercise: Pillars of Data Observability in Conjunction

Why care about conjunctions of events, when individual events provide all the information you need? One important factor is **noise** -- looking at simultaneous events reduces the total number of events you're worried about, and makes it more lilely that the issues are genuine. Another factor is **causality** -- given an issue in some table, looking at simultaneous events in upstream tables might help you determine the root cause, and quicken the path to a solution.

Take the past exercise as an example -- we saw that the `habitability` field had anomalous rates of zeroed values:

This clearly identifies some problematic timestamps, but it's much too noisy. We wouldn't want a notification for every red line on the above graph. Looking for other (upstream) events can not only prune our alerts, but also help us identify the issue's cause.

See if you can join the timestamps from `h_zero_alerts` with timestamps identifying a `schema_change`.

- *Hint*: try querying the `EXOPLANETS_SCHEMA` table using the same approach from Exercise 2.

You should see a single reported date, `2020-07-19`. Not only have we reduced the number of reports, but we potentially learn something -- that the schema change in `EXOPLANETS` _caused_ the zero rate in `HABITABLES` to spike. By combining data observability pillars, we're one step closer to resolving the problem!

## 4. Exercise: Diagnosing Another Distribution Issue

Here's another quick mystery. It looks like the `HABITABLES` table returns to normal after a while, if we only look at zero rates. But probing into the **volume** of the table reveals something odd:

The row counts added seem to increase by ~1.5x each day starting around `DATE`. We could detect this using a naive threshold:

But again, that's not too noisy to be informative. This issue is compounded because volume is usually a problem when it *decreases* (as we saw earlier with freshness). But something must be the cause of this volume change, and turns out, it's a genuine issue.

As another exercise in understanding **distribution**, try querying for _uniqueness_ in `HABITABLES` to find a simultaneous issue.

- *Hint*: What's practically guaranteed to be unique in this table, if anything?

A proper query here should reveal something telling -- the `_ID` field in `HABITABLES` is not unique, meaning we may be adding duplicate entries to our table! Semantics should dictate that `_ID` be 100% unique. Try writing a query that turns up the offending dates below:
- As an extra challenge, try filtering all alerts that occur immediately after other ones -- another potential technique for reducing noise.

# Great work!

This last exercise revealed that certain pillars of data observability are often conjoined to give meaningful alerts (volume and uniqueness; schema change and downstream distributions; etc.). In the next exercise, we'll look at some terms from machine learning to scale our approach.