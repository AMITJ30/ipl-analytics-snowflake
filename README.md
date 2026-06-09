# 🏏 IPL Analytics Platform on Snowflake

## Overview

IPL Analytics Platform is an end-to-end Data Engineering project built on Snowflake using the Medallion Architecture (Landing → Bronze → Silver → Gold).

The objective of this project is to design and implement a modern analytics platform capable of ingesting IPL datasets, transforming them into business-ready data models, and exposing insights through a Streamlit application hosted directly within Snowflake.

This project follows industry-standard data engineering practices including:

* Role-Based Access Control (RBAC)
* Medallion Architecture
* Data Lineage
* Auditability
* Dimensional Modeling
* Scalable ELT Design
* Dashboard Development

---

# Business Problem

The IPL generates massive amounts of match and player data.

Stakeholders often want answers to questions such as:

* Which team has the highest win percentage?
* Which venue produces the highest scores?
* Which players consistently perform under pressure?
* How does home advantage impact team performance?
* Which players have the best strike rate and batting average?

This platform aims to centralize IPL data and provide interactive analytics for teams, players, venues, and match outcomes.

---

# Solution Architecture

```text
Source Files
│
├── matches.csv
├── deliveries.csv
├── teams.csv
├── Players.csv
├── most_runs_average_strikerate.csv
└── teamwise_home_and_away.csv

        │
        ▼

LANDING LAYER
│
├── CSV_FORMAT
└── IPL_STAGE

        │
        ▼

BRONZE LAYER
│
├── MATCHES_RAW
├── DELIVERIES_RAW
├── TEAMS_RAW
├── PLAYERS_RAW
├── PLAYER_STATS_REFERENCE_RAW
└── TEAM_HOME_AWAY_RAW

        │
        ▼

SILVER LAYER
│
├── DIM_TEAM
├── DIM_PLAYER
├── FACT_MATCH
└── FACT_DELIVERY

        │
        ▼

GOLD LAYER
│
├── TEAM_STATS
├── PLAYER_STATS
├── VENUE_STATS
├── HOME_AWAY_ANALYSIS
└── SEASON_SUMMARY

        │
        ▼

SNOWFLAKE STREAMLIT APP
```

---

# Snowflake Environment

## Warehouse

```text
IPL_WH
```

## Database

```text
IPL_ANALYTICS
```

## Schemas

```text
LANDING
BRONZE
SILVER
GOLD
UTIL
```

---

# Security Architecture (RBAC)

The project implements Role-Based Access Control following the Principle of Least Privilege.

```text
SYSADMIN
    │
    ▼
IPL_ADMIN
├── IPL_INGEST
├── IPL_TRANSFORM
└── IPL_REPORTING
```

## Role Responsibilities

### IPL_ADMIN

Responsible for overall project administration.

### IPL_INGEST

Responsible for:

* File ingestion
* Stage management
* Bronze layer maintenance

### IPL_TRANSFORM

Responsible for:

* Silver transformations
* Gold transformations
* Data quality implementation

### IPL_REPORTING

Responsible for:

* Dashboard access
* Read-only analytics consumption

---

# Source Datasets

## matches.csv

Contains match-level information.

Examples:

* Teams
* Toss details
* Match winner
* Venue
* Umpires
* Player of the match

---

## deliveries.csv

Contains ball-by-ball delivery information.

Examples:

* Runs
* Extras
* Wickets
* Bowlers
* Batters

---

## teams.csv

Contains IPL team master data.

---

## Players.csv

Contains player metadata.

Examples:

* Player Name
* Date of Birth
* Batting Hand
* Bowling Skill
* Country

---

## most_runs_average_strikerate.csv

Reference batting statistics used for validation and reconciliation.

---

## teamwise_home_and_away.csv

Contains home and away performance metrics for IPL teams.

---

# Medallion Architecture

## Landing Layer

Purpose:

* Store source files
* Manage ingestion process

Objects:

* IPL_STAGE
* CSV_FORMAT

---

## Bronze Layer

Purpose:

Store raw data exactly as received from source systems.

Characteristics:

* No business logic
* No transformations
* Audit columns maintained

Audit Columns:

```text
SOURCE_FILE_NAME
BATCH_ID
LOAD_TS
```

---

## Silver Layer

Purpose:

Create cleaned and standardized business entities.

Planned Objects:

### DIM_TEAM

Attributes:

* Team Name
* Team Short Name
* Home City
* Home Ground
* Active Flag

### DIM_PLAYER

Attributes:

* Country
* Batting Hand
* Bowling Skill
* Age

### FACT_MATCH

Match-level fact table.

### FACT_DELIVERY

Ball-by-ball fact table.

---

## Gold Layer

Purpose:

Provide business-ready analytics datasets.

Planned Objects:

### TEAM_STATS

* Matches
* Wins
* Losses
* Win Percentage

### PLAYER_STATS

* Runs
* Average
* Strike Rate
* Boundaries

### VENUE_STATS

* Average Score
* Highest Score
* Venue Trends

### HOME_AWAY_ANALYSIS

* Home Wins
* Away Wins
* Home Advantage Metrics

### SEASON_SUMMARY

Season-level performance metrics.

---

# Streamlit Dashboard

The final Streamlit application will be hosted directly within Snowflake.

## Dashboard Pages

### Overview Dashboard

* Total Matches
* Total Players
* Total Teams
* Total Venues

### Team Analysis

* Win Percentage
* Home vs Away Performance
* Team Trends

### Player Analysis

* Runs
* Strike Rate
* Average
* Dismissals

### Venue Analysis

* Average Score
* Highest Totals
* Win Patterns

### Home Advantage Dashboard

* Home Wins
* Away Wins
* Team Performance Comparison

---

# Future Enhancements

* Snowflake Streams
* Snowflake Tasks
* Incremental Loading
* Snowpark Transformations
* Data Quality Framework
* Cortex AI Integration
* Match Prediction Models
* Fantasy Team Recommendation Engine

---

# Current Project Status

## Completed

* Repository Setup
* RBAC Design
* Warehouse Setup
* Database Setup
* Schema Setup
* Grants & Permissions
* Landing Layer Setup
* File Format Creation
* Stage Creation
* Bronze Layer Design
* Source File Upload

## In Progress

* Bronze Data Loading

## Planned

* Silver Layer
* Gold Layer
* Streamlit Dashboard
* Streams & Tasks

---

# Author

Amit

Data Engineer | Snowflake | SQL | Python | Azure Data Engineering
