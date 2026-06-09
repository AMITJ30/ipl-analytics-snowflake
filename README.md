# 🏏 IPL Analytics Platform on Snowflake

## Project Overview

The IPL Analytics Platform is an end-to-end Data Engineering project built on Snowflake using the Medallion Architecture (Bronze, Silver, Gold).

This project demonstrates:

- Snowflake Data Warehousing
- Medallion Architecture
- Role-Based Access Control (RBAC)
- Snowflake Streams & Tasks
- Data Modeling
- Streamlit Application Development
- Analytics Engineering

---

## Architecture

```text
CSV Files
    |
    v
BRONZE
    |
    v
SILVER
    |
    v
GOLD
    |
    v
STREAMLIT APP
```

---

## Snowflake Environment

### Roles

```text
SYSADMIN
   |
IPL_ADMIN
├── IPL_INGEST
├── IPL_TRANSFORM
└── IPL_REPORTING
```

### Warehouse

- IPL_WH

### Database

```text
IPL_ANALYTICS
├── BRONZE
├── SILVER
├── GOLD
└── UTIL
```

---

## Medallion Architecture

### Bronze Layer

Raw ingestion layer.

Tables:

- MATCHES_RAW
- DELIVERIES_RAW

### Silver Layer

Business-ready cleaned layer.

Dimension Tables:

- DIM_TEAM
- DIM_PLAYER
- DIM_VENUE

Fact Tables:

- FACT_MATCH
- FACT_DELIVERY

### Gold Layer

Analytics layer.

- PLAYER_BATTING_STATS
- PLAYER_BOWLING_STATS
- TEAM_STATS
- VENUE_STATS

---

## Streamlit Dashboard Features

### Dashboard Overview

- Total Matches
- Total Players
- Total Venues
- Highest Team Score

### Team Analysis

- Win Percentage
- Matches Played
- Season-wise Performance

### Player Analysis

- Runs
- Strike Rate
- Average
- Boundaries

### Player Comparison

- Player vs Player Analysis
- Performance Metrics Comparison

### Venue Analysis

- Average Score
- Win Trends
- Highest Successful Chase

---

## Project Structure

```text
ipl-analytics-snowflake/
│
├── README.md
├── docs/
├── sql/
├── streamlit/
├── screenshots/
└── datasets/
```

---

## Future Enhancements

- Snowflake Streams
- Snowflake Tasks
- Snowpark Transformations
- Cortex AI Integration
- Natural Language Querying
- Match Prediction Engine
- Fantasy Team Recommendation System

---

## Learning Objectives

This project helps demonstrate:

- Enterprise Data Engineering Design
- Snowflake Administration
- RBAC Implementation
- Data Modeling
- ETL/ELT Development
- Analytics Engineering
- Streamlit Development

---

## Author

**Amit**

Data Engineer | Snowflake | Python | SQL | Azure Data Engineering
