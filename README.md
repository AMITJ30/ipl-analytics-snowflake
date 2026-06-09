🏏 IPL Analytics Platform on Snowflake
Project Overview

The IPL Analytics Platform is an end-to-end Data Engineering project built on Snowflake using the Medallion Architecture (Bronze, Silver, Gold).

The platform ingests IPL historical match and ball-by-ball data, transforms it into analytical datasets, and exposes insights through a Snowflake Streamlit application.

This project demonstrates real-world Data Engineering concepts including:

Snowflake Data Warehousing
Medallion Architecture
Role-Based Access Control (RBAC)
Data Modeling
Snowflake Streams
Snowflake Tasks
Snowpark & Streamlit
Data Quality Validation
Analytics Dashboarding
Architecture
                           +------------------+
                           |  IPL CSV Files   |
                           +------------------+
                                     |
                                     |
                                     v
+------------------------------------------------------+
|                      BRONZE LAYER                    |
|------------------------------------------------------|
| MATCHES_RAW                                          |
| DELIVERIES_RAW                                       |
+------------------------------------------------------+
                                     |
                                     |
                                     v
+------------------------------------------------------+
|                      SILVER LAYER                    |
|------------------------------------------------------|
| DIM_TEAM                                              |
| DIM_PLAYER                                            |
| DIM_VENUE                                             |
| FACT_MATCH                                            |
| FACT_DELIVERY                                         |
+------------------------------------------------------+
                                     |
                                     |
                                     v
+------------------------------------------------------+
|                       GOLD LAYER                     |
|------------------------------------------------------|
| PLAYER_BATTING_STATS                                  |
| PLAYER_BOWLING_STATS                                  |
| TEAM_STATS                                            |
| VENUE_STATS                                           |
+------------------------------------------------------+
                                     |
                                     |
                                     v
+------------------------------------------------------+
|                 STREAMLIT APPLICATION                |
+------------------------------------------------------+
Technology Stack
Component	Technology
Data Warehouse	Snowflake
Data Processing	Snowflake SQL
Data Pipeline	Streams & Tasks
Visualization	Streamlit in Snowflake
Version Control	GitHub
Dataset Source	IPL Historical Dataset
Architecture	Medallion Architecture
Project Structure
IPL_ANALYTICS/
│
├── docs/
│   ├── architecture.md
│   ├── data_model.md
│   └── setup_guide.md
│
├── sql/
│   ├── 01_roles.sql
│   ├── 02_database_setup.sql
│   ├── 03_file_formats.sql
│   ├── 04_stages.sql
│   ├── 05_bronze_tables.sql
│   ├── 06_silver_tables.sql
│   ├── 07_gold_tables.sql
│   ├── 08_streams.sql
│   ├── 09_tasks.sql
│   └── 10_grants.sql
│
├── streamlit/
│   ├── app.py
│   ├── pages/
│   │   ├── overview.py
│   │   ├── team_analysis.py
│   │   ├── player_analysis.py
│   │   └── venue_analysis.py
│
├── datasets/
│   ├── matches.csv
│   └── deliveries.csv
│
└── README.md
Snowflake Environment Setup
Roles

The project follows enterprise RBAC practices.

Role	Responsibility
IPL_ADMIN	Administrative access
IPL_INGEST	Data ingestion
IPL_TRANSFORM	Data transformation
IPL_REPORTING	Reporting and analytics

Role hierarchy:

SYSADMIN
   |
IPL_ADMIN
 ├── IPL_INGEST
 ├── IPL_TRANSFORM
 └── IPL_REPORTING
Warehouse
CREATE WAREHOUSE IPL_WH
WITH
WAREHOUSE_SIZE='XSMALL'
AUTO_SUSPEND=60
AUTO_RESUME=TRUE;
Database Structure
IPL_ANALYTICS
│
├── BRONZE
├── SILVER
├── GOLD
└── UTIL
Bronze Layer

Raw data ingestion layer.

MATCHES_RAW

Stores match-level data exactly as received.

Columns include:

ID
SEASON
CITY
MATCH_DATE
TEAM1
TEAM2
TOSS_WINNER
WINNER
VENUE
RAW_LOAD_TS
DELIVERIES_RAW

Stores ball-by-ball delivery information.

Columns include:

MATCH_ID
INNING
OVER_NO
BALL_NO
BATSMAN
BOWLER
BATSMAN_RUNS
TOTAL_RUNS
IS_WICKET
RAW_LOAD_TS
Silver Layer

Cleaned and standardized business entities.

Dimension Tables
DIM_TEAM
TEAM_ID
TEAM_NAME
SHORT_NAME
DIM_PLAYER
PLAYER_ID
PLAYER_NAME
COUNTRY
ROLE
BATTING_STYLE
BOWLING_STYLE
DIM_VENUE
VENUE_ID
VENUE_NAME
CITY
Fact Tables
FACT_MATCH
MATCH_ID
SEASON
MATCH_DATE
TEAM1_ID
TEAM2_ID
WINNER_ID
VENUE_ID
FACT_DELIVERY
MATCH_ID
INNINGS
OVER_NO
BALL_NO
BATSMAN_ID
BOWLER_ID
RUNS
IS_FOUR
IS_SIX
IS_WICKET
Gold Layer

Business-ready analytics layer.

PLAYER_BATTING_STATS
PLAYER_ID
MATCHES
RUNS
BALLS
AVERAGE
STRIKE_RATE
FIFTIES
HUNDREDS
PLAYER_BOWLING_STATS
PLAYER_ID
WICKETS
RUNS_CONCEDED
ECONOMY
TEAM_STATS
TEAM_ID
MATCHES
WINS
LOSSES
WIN_PERCENT
VENUE_STATS
VENUE_ID
AVG_SCORE
AVG_FIRST_INNINGS
AVG_SECOND_INNINGS
Data Pipeline
CSV Files
   |
   v
BRONZE
   |
   v
Snowflake Streams
   |
   v
Snowflake Tasks
   |
   v
SILVER
   |
   v
GOLD
   |
   v
STREAMLIT DASHBOARD
Streamlit Application
Features
Dashboard Overview
Total Matches
Total Players
Total Venues
Highest Team Score
Team Analysis
Matches Played
Wins
Losses
Win Percentage
Season-wise Performance
Player Analysis
Runs
Average
Strike Rate
Boundaries
Match Statistics
Player Comparison

Compare:

Player A vs Player B

Metrics:

Runs
Strike Rate
Average
Boundaries
Consistency
Venue Analysis
Average Score
Highest Chase
Win Percentage Batting First
Win Percentage Chasing
Future Enhancements
Phase 2
Incremental Loading using Streams
Automated Transformations using Tasks
Data Quality Framework
Audit Logging
Phase 3
Snowpark Transformations
Cortex AI Integration
Natural Language Queries

Example:

Who scored the most runs in IPL 2023?
Phase 4
Match Prediction Model
Winning Probability Dashboard
Fantasy Team Recommendation Engine
Dataset Source

IPL Historical Dataset

Source:

Kaggle IPL Dataset

Learning Objectives

This project demonstrates:

Enterprise Data Engineering Design
Snowflake Administration
RBAC Implementation
Medallion Architecture
Data Modeling
Incremental Data Processing
Dashboard Development
Analytics Engineering
Author

Amit
Data Engineer | Snowflake | Python | SQL | Azure Data Engineering
