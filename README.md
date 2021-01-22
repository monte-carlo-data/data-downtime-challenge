# Data Downtime Challenge

This repo contains the notebooks run in Monte Carlo's Data Observability course.

# Steps for running locally:

1. Clone the repo: `$ git clone https://github.com/monte-carlo-data/data-downtime-challenge.git`
2. Initialize a python virtual environment (3.7.5): `$ python3 -m venv env`
3. Activate the environment: `$ source env/bin/activate`
4. Install requirements: `$ pip install -r requirements.txt`
5. Start the notebooks server: `$ jupyter notebook`

___

This should get you up and running and able to revisit the notebooks from the course. Feel free to submit issues.

# Repository Format

- `notebooks/`: the notebooks we went through in the course
- `solutions/`: notebooks with `SQL` implementations for the exercises, also used in the course
- `helpers/`: python code that created the mock data and incidents used in the exercises
- `data/`: `SQLite` DB object files, utilities, and assets shown in the notebooks
