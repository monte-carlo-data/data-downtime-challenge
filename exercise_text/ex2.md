# Data Downtime Challenge | Exercise 2

## 0. Setup

## 1. Introduction

In the last exercise, we examined some isolated data downtime incidents in the `EXOPLANETS` table. While the techniques from that exercise are helpful, in practice data downtime involves data infrastructure where many tables interact. So, in this exercise, we'll look at a scenario where multiple tables interact.

### `EXOPLANETS`
Let's once again consider our `EXOPLANETS` table, but at a later date than before. Now, our table has additional entries and additional _fields_. We now record the planets' orbital eccentricity and the contents of their atmosphere.

Let's take a look at our 10 most recent additions to the table:

A database entry in `EXOPLANETS` contains the following info:

0. `_id`: A UUID corresponding to the planet.
1. `distance`: Distance from Earth, in lightyears.
2. `g`: Surface gravity as a multiple of $g$, the gravitational force constant.
3. `orbital_period`: Length of a single orbital cycle in days.
4. `avg_temp`: Average surface temperature in degrees Kelvin.
5. `date_added`: The date our system discovered the planet and added it automatically to our databases.
6. `eccentricity`: The [orbital eccentricity](https://en.wikipedia.org/wiki/Orbital_eccentricity) of the planet about its host star.
7. `atmosphere`: The dominant chemical makeup of the planet's atmosphere.

Note that like `distance`, `g`, `orbital_period`, and `avg_temp`, both `eccentricity` and `atmosphere` may be `NULL` for a given planet as a result of missing or erroneous data. For example, [rogue planets](https://en.wikipedia.org/wiki/Rogue_planet) have undefined orbital eccentricity, and many planets don't have atmospheres at all.

Note also that data is not backfilled, meaning data entries from the beginning of the table will not have `eccentricity` and `atmosphere` information.

### `EXOPLANETS_SCHEMA`

Thankfully, we have been recording historical `table_info` on the `EXOPLANETS` table and collecting the results in a table called `EXOPLANETS_SCHEMA`, updated daily.

Querying the very beginning and end of `EXOPLANETS_SCHEMA`'s data reflects that `EXOPLANETS`'s metadata has changed since January 2020:

## 2. Exercise: Understanding **Schema Change**

When exactly did `EXOPLANETS` start recording new data? The metadata in `EXOPLANETS_SCHEMA` should tell us. See if you can write a SQL query that returns the date(s) the schema changed and to what it changed.

- *Hint*: As before, `ex2_soln.ipynb` is your friend if you need inspiration.

A correct implementation should show a single date, **2020-07-19**. Since the data was not backfilled, we can also arrive at this result implicitly, by checking the rate of non-null `eccentricity` and `atmosphere` values in `EXOPLANETS` over time.

These plots show the number of new entries with values for `eccentricity` and `atmosphere` respectively on each day. Note that on July 19, entries abruptly start filling in because of the addition to the schema.

## 3. An additional table

Now, we want to involve another table in our DB. `HABITABLES` records information about the habitability of exoplanets we've discovered. This table takes data from `EXOPLANETS` and other upstream tables and transforms it to produce a `habitability` index: a real number between 0 and 1 indicating how likely the planet is to harbor life.

## 4. Exercise: Visualizing Distribution Errors
Like in exercise 1, I'll write a quick query assessing a **distributional** feature of the `HABITABILITY` table -- how habitable is the average planet we detect, as a function of the day it was detected?

I plotted the date of the schema change, 2020-07-19, in red as a visual aid. Clearly, unless our instruments are malfunctioning, something is wrong! The planets we're adding to the table *after* the schema change seem much less habitable on average. Using a `SQL` query below, see if you can figure out what exactly.

*Hint*: When averages change, it's natural to look for occurrences of unusual values. When is `habitability` NULL, 0, or outside of the range $[0, 1]$? What about other fields in the table that might be related? Try writing a query that detects anomalous rates of such unusual values.

With a small amount of digging, we can uncover something important -- the `habitability` index is never exactly 0 *before* the schema change, but afterwards we see the rate of 0s jump up to ~50%. This has the detected effect of dipping the average value of the field.

Note that in practice, you should look for both -- measuring a field's **rate of zero values**, as well as it's **average value**, can both help with identifying data downtime issues. As we saw last exercise, the **rate of null values** can also be helpful.

# Great work!

In the next exercise, we'll look at queries that span multiple tables, another step towards building intelligent data downtime systems.