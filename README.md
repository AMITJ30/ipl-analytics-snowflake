# 🏏 IPL Analytics Platform --- Snowflake & Streamlit

An end-to-end **IPL Analytics Platform** built using **Snowflake and
Streamlit**.

This project demonstrates a modern data engineering and analytics
workflow where IPL match and ball-by-ball data is processed through
multiple data layers in Snowflake and exposed through an interactive
Streamlit dashboard.

The dashboard covers IPL seasons from **2008 to 2019** and provides
insights into teams, players, venues, batting, bowling, and match
performance.

------------------------------------------------------------------------

## 📌 Project Overview

The objective of this project is to build a complete analytics solution
using:

-   **Snowflake** as the cloud data platform
-   **SQL** for data transformation and analytics
-   **Streamlit** for interactive dashboards
-   **Python / Pandas** for application-side processing
-   **Bronze → Silver → Gold → Reporting** architecture

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                    IPL Data
                       │
                       ▼
                ┌─────────────┐
                │   BRONZE    │
                │ Raw Data    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   SILVER    │
                │ Cleaned /   │
                │ Standardized│
                │ Data        │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │    GOLD     │
                │ Business    │
                │ Analytics   │
                │ Tables      │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  REPORTING  │
                │ Views       │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  STREAMLIT  │
                │ Dashboard   │
                └─────────────┘
```

------------------------------------------------------------------------

## 🥉 Bronze Layer

The Bronze layer contains the raw/source IPL data.

The project works with datasets representing:

-   Matches
-   Ball-by-ball deliveries
-   Players
-   Teams
-   Other IPL reference information

------------------------------------------------------------------------

## 🥈 Silver Layer

The Silver layer contains cleaned and standardized data.

Typical processing includes:

-   Data type standardization
-   Column standardization
-   Data cleansing
-   Handling inconsistent values
-   Preparing match and delivery data for analytical transformations

### Match Data

``` text
MATCH_ID
SEASON
MATCH_DATE
CITY
TEAM1
TEAM2
TOSS_WINNER
TOSS_DECISION
MATCH_WINNER
WIN_BY_RUNS
WIN_BY_WICKETS
PLAYER_OF_MATCH
VENUE
CREATED_TS
```

### Delivery Data

``` text
MATCH_ID
INNING
BATTING_TEAM
BOWLING_TEAM
OVER_NO
BALL_NO
BATSMAN
NON_STRIKER
BOWLER
BATSMAN_RUNS
EXTRA_RUNS
TOTAL_RUNS
PLAYER_DISMISSED
DISMISSAL_KIND
FIELDER
IS_DOT_BALL
IS_FOUR
IS_SIX
IS_WICKET
CREATED_TS
```

------------------------------------------------------------------------

## 🥇 Gold Layer

The Gold layer contains business-oriented analytical tables, including:

-   `TEAM_PERFORMANCE`
-   `ORANGE_CAP_BY_SEASON`
-   `PURPLE_CAP_BY_SEASON`
-   `VENUE_ANALYTICS`
-   `SEASON_SUMMARY`
-   `TEAM_HEAD_TO_HEAD`
-   `PLAYER_BATTING_SUMMARY`
-   `PLAYER_BOWLING_SUMMARY`
-   `PLAYER_OF_MATCH_SUMMARY`
-   `DASHBOARD_SUMMARY`

------------------------------------------------------------------------

## 📊 Reporting Layer

The Reporting layer exposes analytical data through reporting views:

``` text
VW_DASHBOARD_SUMMARY
VW_ORANGE_CAP_BY_SEASON
VW_PURPLE_CAP_BY_SEASON
VW_PLAYER_BATTING_SUMMARY
VW_PLAYER_BOWLING_SUMMARY
VW_PLAYER_OF_MATCH_SUMMARY
VW_SEASON_SUMMARY
VW_TEAM_HEAD_TO_HEAD
VW_TEAM_PERFORMANCE
VW_VENUE_ANALYTICS
```

The Streamlit application primarily consumes this Reporting layer.

------------------------------------------------------------------------

# 📊 Dashboard Pages

## 🏠 Home

Welcome page describing the project and its Bronze → Silver → Gold →
Reporting architecture.

## 📊 Dashboard Summary

Overall IPL snapshot containing:

-   Total Matches
-   Total Seasons
-   Total Teams
-   Total Players
-   Total Venues
-   Total Deliveries
-   Total Runs
-   Total Wickets
-   Highest Match Score
-   Lowest Match Score
-   Average Match Score

Current dataset summary:

  Metric                    Value
  --------------------- ---------
  Total Matches               756
  Total Seasons                12
  Total Teams                  15
  Total Players               566
  Total Venues                 41
  Total Deliveries        179,078
  Total Runs              235,290
  Total Wickets             8,834
  Highest Match Score         471
  Lowest Match Score           56
  Average Match Score      311.23

## 📈 Season Analysis

Provides season-level statistics such as matches, runs, wickets, average
runs per match, highest/lowest score, venues, team occurrences and
unique winners.

Available seasons:

``` text
IPL-2008 through IPL-2019
```

## 🏏 Team Performance

Provides:

-   Matches played
-   Matches won
-   Matches lost
-   Win percentage

## 🟠 Orange Cap

Provides:

-   Season-wise run leaders
-   Top 10 run scorers
-   Strike rate
-   Batting average
-   Runs vs strike rate
-   All-season top-10 leaderboard

## 🟣 Purple Cap

Provides:

-   Season-wise wicket leaders
-   Top 10 wicket takers
-   Economy
-   Bowling average
-   Wickets vs economy
-   All-season top-10 leaderboard

## 🏟️ Venue Analytics

Provides:

-   Matches played
-   Total runs
-   Total wickets
-   Average runs per match
-   Highest match score
-   Lowest match score
-   Venue leaderboard

## 🤝 Team Head-to-Head

Provides:

-   Matches played
-   Team 1 wins
-   Team 2 wins
-   No-result matches
-   Win percentages
-   Head-to-head comparison charts

## 🏏 Player Batting Summary

Provides:

-   Total runs
-   Balls faced
-   Fours
-   Sixes
-   Strike rate
-   Batting average
-   Top 10 run scorers
-   Runs vs strike rate
-   Top six hitters

## 🎯 Player Bowling Summary

Provides:

-   Wickets
-   Balls bowled
-   Runs conceded
-   Dot balls
-   Economy
-   Bowling strike rate
-   Bowling average
-   Top 10 wicket takers
-   Wickets vs economy
-   Top dot-ball bowlers

## 🏅 Player of the Match

Provides:

-   Awards won
-   First season
-   Last season
-   Different winning teams
-   Top 10 award winners

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Technology                       Purpose
  -------------------------------- ------------------------------
  Snowflake                        Cloud data platform
  SQL                              Transformation and analytics
  Python                           Application and processing
  Streamlit                        Interactive dashboard
  Pandas                           Data manipulation
  Plotly                           Interactive visualization
  Snowflake Connector for Python   Snowflake connectivity
  Git / GitHub                     Source control

------------------------------------------------------------------------

# 📁 Project Structure

``` text
ipl-analytics-snowflake/
│
├── streamlit/
│   ├── app.py
│   ├── pages/
│   │   ├── 1_Dashboard_Summary.py
│   │   ├── 2_Season_Analysis.py
│   │   ├── 3_Orange_Cap.py
│   │   ├── 4_Purple_Cap.py
│   │   ├── 5_Venue_Analytics.py
│   │   ├── 6_Team_Head_to_Head.py
│   │   ├── 8_Player_Batting_Summary.py
│   │   ├── 9_Player_Bowling_Summary.py
│   │   └── 10_Player_of_the_Match.py
│   └── utils/
│       ├── connection.py
│       └── filters.py
│
├── snowflake/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── reporting/
│
├── data/
├── requirements.txt
├── README.md
└── .gitignore
```

> Adjust filenames if your local repository uses different names.

------------------------------------------------------------------------

# 🔐 Snowflake Connection

The application uses Streamlit secrets for Snowflake credentials.

Example:

``` toml
[snowflake]
account = "YOUR_ACCOUNT"
user = "YOUR_USER"
password = "YOUR_PASSWORD"
warehouse = "YOUR_WAREHOUSE"
database = "IPL_ANALYTICS"
schema = "REPORTING"
role = "YOUR_ROLE"
```

Never commit real credentials to GitHub.

Add this to `.gitignore`:

``` gitignore
.streamlit/secrets.toml
```

------------------------------------------------------------------------

# 🚀 Running the Project

### 1. Clone

``` bash
git clone <your-github-repository-url>
cd ipl-analytics-snowflake
```

### 2. Create virtual environment

``` bash
python -m venv venv
```

Windows:

``` bash
venv\Scriptsctivate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Snowflake

Create:

``` text
.streamlit/secrets.toml
```

and add your Snowflake credentials.

### 5. Run Streamlit

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

# 🔄 Data Flow

``` text
Raw IPL Data
     │
     ▼
Bronze
     │
     ▼
Silver
     │
     ▼
Gold
     │
     ▼
Reporting Views
     │
     ▼
Snowflake Connector
     │
     ▼
Python / Pandas
     │
     ▼
Plotly
     │
     ▼
Streamlit
```

------------------------------------------------------------------------

# 📌 Data Engineering Concepts Demonstrated

-   Layered data architecture
-   Snowflake data modeling
-   Analytical SQL
-   Aggregations
-   Ranking logic
-   Reporting views
-   Data cleansing
-   NULL handling
-   Snowflake-to-Python connectivity
-   Streamlit development
-   Interactive filtering
-   Data visualization
-   Error handling
-   Git/GitHub organization

------------------------------------------------------------------------

# 🧪 Validation

The application was tested across the available IPL seasons from **2008
through 2019**.

Validation included:

-   Snowflake connection testing
-   Reporting view validation
-   SQL query validation
-   Streamlit page testing
-   Numeric conversion
-   NULL handling
-   Top-10 ranking validation
-   Season data validation

------------------------------------------------------------------------

# 🚧 Future Enhancements

Potential improvements include:

-   Season-wise player batting summaries
-   Season-wise player bowling summaries
-   Season-wise venue analytics
-   Consistent Season/Team filtering across every page
-   Toss analysis
-   Winning-margin analysis
-   Powerplay and death-over analytics
-   Automated data ingestion
-   Snowflake Streams and Tasks
-   CI/CD
-   Streamlit deployment
-   Automated testing

------------------------------------------------------------------------

# 👨‍💻 Author

**Amit Jha**

**Data Engineer**

Technologies:

**Snowflake \| SQL \| Python \| Streamlit \| Pandas \| Plotly \| Data
Engineering**

------------------------------------------------------------------------

## ⭐ Project Goal

The goal of this project is to demonstrate how raw sports data can be
transformed into a modern analytical solution using a cloud data
platform and an interactive application.

**Snowflake → Transform → Gold Analytics → Reporting → Streamlit**
