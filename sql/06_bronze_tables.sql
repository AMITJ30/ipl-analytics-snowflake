/***************************************************************************************************
Script Name    : 06_bronze_tables.sql

Project        : IPL Analytics Platform

Purpose
-------
Creates raw ingestion tables in the Bronze layer.

Why Bronze?
-----------
The Bronze layer stores source data exactly as received.

Benefits:
---------
- Data lineage
- Easy reprocessing
- Auditability
- Supports incremental loading

Tables Created
--------------
MATCHES_RAW
DELIVERIES_RAW

Source
------
Kaggle IPL Dataset

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;
USE SCHEMA BRONZE;

CREATE OR REPLACE TABLE MATCHES_RAW
(
    ID NUMBER,
    SEASON STRING,
    CITY STRING,
    MATCH_DATE DATE,
    TEAM1 STRING,
    TEAM2 STRING,
    TOSS_WINNER STRING,
    TOSS_DECISION STRING,
    RESULT STRING,
    WINNER STRING,
    VENUE STRING,

    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE DELIVERIES_RAW
(
    MATCH_ID NUMBER,
    INNING NUMBER,
    BATTING_TEAM STRING,
    BOWLING_TEAM STRING,
    OVER_NO NUMBER,
    BALL_NO NUMBER,

    BATSMAN STRING,
    NON_STRIKER STRING,
    BOWLER STRING,

    BATSMAN_RUNS NUMBER,
    EXTRA_RUNS NUMBER,
    TOTAL_RUNS NUMBER,

    IS_WICKET NUMBER,
    DISMISSAL_KIND STRING,
    PLAYER_DISMISSED STRING,

    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
