/***************************************************************************************************
Script Name    : 06_bronze_tables.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Creates Bronze Layer tables for IPL Analytics Platform.

What is Bronze Layer?
---------------------
The Bronze layer is the raw ingestion layer in the Medallion Architecture.

Source files are loaded into Bronze tables with minimal or no transformation.

Architecture
------------

Landing Files
-------------
matches.csv
deliveries.csv
teams.csv
Players.csv
most_runs_average_strikerate.csv
teamwise_home_and_away.csv

                |
                v

BRONZE LAYER
------------
MATCHES_RAW
DELIVERIES_RAW
TEAMS_RAW
PLAYERS_RAW
PLAYER_STATS_REFERENCE_RAW
TEAM_HOME_AWAY_RAW

Why Store Raw Data?
-------------------
1. Data Lineage
   Track data from source to report.

2. Auditability
   Retain original source records.

3. Reprocessing
   Reload Silver and Gold layers without requesting source files again.

4. Troubleshooting
   Compare transformed data with source data.

Audit Columns
-------------
SOURCE_FILE_NAME
    Name of source file loaded.

BATCH_ID
    Unique identifier for ingestion batch.

LOAD_TS
    Timestamp when record was loaded.

Objects Created
---------------
MATCHES_RAW
DELIVERIES_RAW
TEAMS_RAW
PLAYERS_RAW
PLAYER_STATS_REFERENCE_RAW
TEAM_HOME_AWAY_RAW

Prerequisites
-------------
1. IPL_ANALYTICS Database
2. BRONZE Schema
3. LANDING Schema
4. IPL_STAGE
5. CSV_FORMAT

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

USE SCHEMA BRONZE;

--------------------------------------------------------------------------------
-- MATCHES_RAW
-- Stores match-level IPL information.
--------------------------------------------------------------------------------

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
    DL_APPLIED NUMBER,

    WINNER STRING,

    WIN_BY_RUNS NUMBER,
    WIN_BY_WICKETS NUMBER,

    PLAYER_OF_MATCH STRING,

    VENUE STRING,

    UMPIRE1 STRING,
    UMPIRE2 STRING,
    UMPIRE3 STRING,

    SOURCE_FILE_NAME STRING,
    BATCH_ID STRING,
    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- DELIVERIES_RAW
-- Stores ball-by-ball delivery information.
--------------------------------------------------------------------------------

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

    IS_SUPER_OVER NUMBER,

    WIDE_RUNS NUMBER,
    BYE_RUNS NUMBER,
    LEGBYE_RUNS NUMBER,
    NOBALL_RUNS NUMBER,
    PENALTY_RUNS NUMBER,

    BATSMAN_RUNS NUMBER,
    EXTRA_RUNS NUMBER,
    TOTAL_RUNS NUMBER,

    PLAYER_DISMISSED STRING,
    DISMISSAL_KIND STRING,
    FIELDER STRING,

    SOURCE_FILE_NAME STRING,
    BATCH_ID STRING,
    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- TEAMS_RAW
-- Stores team master data.
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE TEAMS_RAW
(
    TEAM_NAME STRING,

    SOURCE_FILE_NAME STRING,
    BATCH_ID STRING,
    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- PLAYERS_RAW
-- Stores player master information.
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE PLAYERS_RAW
(
    PLAYER_NAME STRING,

    DOB DATE,

    BATTING_HAND STRING,

    BOWLING_SKILL STRING,

    COUNTRY STRING,

    SOURCE_FILE_NAME STRING,
    BATCH_ID STRING,
    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- PLAYER_STATS_REFERENCE_RAW
-- Stores reference batting statistics.
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE PLAYER_STATS_REFERENCE_RAW
(
    BATSMAN STRING,

    TOTAL_RUNS NUMBER,

    OUTS NUMBER,

    NUMBER_OF_BALLS NUMBER,

    AVERAGE NUMBER(10,2),

    STRIKE_RATE NUMBER(10,2),

    SOURCE_FILE_NAME STRING,
    BATCH_ID STRING,
    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- TEAM_HOME_AWAY_RAW
-- Stores home and away performance statistics.
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE TEAM_HOME_AWAY_RAW
(
    TEAM_NAME STRING,

    HOME_WINS NUMBER,
    AWAY_WINS NUMBER,

    HOME_MATCHES NUMBER,
    AWAY_MATCHES NUMBER,

    HOME_WIN_PERCENTAGE NUMBER(10,2),
    AWAY_WIN_PERCENTAGE NUMBER(10,2),

    SOURCE_FILE_NAME STRING,
    BATCH_ID STRING,
    LOAD_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Validation
--------------------------------------------------------------------------------

SHOW TABLES;

--------------------------------------------------------------------------------
-- Expected Output
--------------------------------------------------------------------------------

-- MATCHES_RAW
-- DELIVERIES_RAW
-- TEAMS_RAW
-- PLAYERS_RAW
-- PLAYER_STATS_REFERENCE_RAW
-- TEAM_HOME_AWAY_RAW

--------------------------------------------------------------------------------
