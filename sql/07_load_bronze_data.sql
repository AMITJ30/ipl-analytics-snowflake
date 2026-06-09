/***************************************************************************************************
Script Name    : 07_load_bronze_data.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Load source datasets from LANDING stage into Bronze layer tables.

What is Happening?
------------------
Source files are first uploaded to:

IPL_ANALYTICS.LANDING.IPL_STAGE

These files are then loaded into Bronze tables using Snowflake's
COPY INTO command.

Architecture
------------

CSV Files
---------
matches.csv
deliveries.csv
teams.csv
Players.csv
most_runs_average_strikerate.csv
teamwise_home_and_away.csv

                |
                v

LANDING.IPL_STAGE

                |
                v

BRONZE TABLES

Why COPY INTO?
--------------
Snowflake's native bulk loading utility.

Benefits
--------
1. Fast Parallel Loading
2. Error Handling
3. Scalable
4. Production Standard

Metadata Columns
----------------
SOURCE_FILE_NAME
    Tracks source file.

BATCH_ID
    Identifies ingestion batch.

LOAD_TS
    Automatically populated during load.

Prerequisites
-------------
1. Files uploaded to IPL_STAGE
2. Bronze tables created
3. CSV_FORMAT created

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

--------------------------------------------------------------------------------
-- Validate Files in Stage
--------------------------------------------------------------------------------

LIST @IPL_ANALYTICS.LANDING.IPL_STAGE;

--------------------------------------------------------------------------------
-- Load TEAMS_RAW
--------------------------------------------------------------------------------

COPY INTO IPL_ANALYTICS.BRONZE.TEAMS_RAW
(
TEAM_NAME,
SOURCE_FILE_NAME,
BATCH_ID
)
FROM
(
SELECT
$1,
METADATA$FILENAME,
TO_VARCHAR(CURRENT_TIMESTAMP())
FROM @IPL_ANALYTICS.LANDING.IPL_STAGE/teams.csv
)
FILE_FORMAT = (FORMAT_NAME = IPL_ANALYTICS.LANDING.CSV_FORMAT);

--------------------------------------------------------------------------------
-- Load PLAYERS_RAW
--------------------------------------------------------------------------------

COPY INTO IPL_ANALYTICS.BRONZE.PLAYERS_RAW
(
PLAYER_NAME,
DOB,
BATTING_HAND,
BOWLING_SKILL,
COUNTRY,
SOURCE_FILE_NAME,
BATCH_ID
)
FROM
(
SELECT
$1,
TRY_TO_DATE($2),
$3,
$4,
$5,
METADATA$FILENAME,
TO_VARCHAR(CURRENT_TIMESTAMP())
FROM @IPL_ANALYTICS.LANDING.IPL_STAGE/Players.csv
)
FILE_FORMAT = (FORMAT_NAME = IPL_ANALYTICS.LANDING.CSV_FORMAT);

--------------------------------------------------------------------------------
-- Load PLAYER_STATS_REFERENCE_RAW
--------------------------------------------------------------------------------

COPY INTO IPL_ANALYTICS.BRONZE.PLAYER_STATS_REFERENCE_RAW
(
BATSMAN,
TOTAL_RUNS,
OUTS,
NUMBER_OF_BALLS,
AVERAGE,
STRIKE_RATE,
SOURCE_FILE_NAME,
BATCH_ID
)
FROM
(
SELECT
$1,
$2,
$3,
$4,
$5,
$6,
METADATA$FILENAME,
TO_VARCHAR(CURRENT_TIMESTAMP())
FROM @IPL_ANALYTICS.LANDING.IPL_STAGE/most_runs_average_strikerate.csv
)
FILE_FORMAT = (FORMAT_NAME = IPL_ANALYTICS.LANDING.CSV_FORMAT);

--------------------------------------------------------------------------------
-- Load TEAM_HOME_AWAY_RAW
--------------------------------------------------------------------------------

COPY INTO IPL_ANALYTICS.BRONZE.TEAM_HOME_AWAY_RAW
(
TEAM_NAME,
HOME_WINS,
AWAY_WINS,
HOME_MATCHES,
AWAY_MATCHES,
HOME_WIN_PERCENTAGE,
AWAY_WIN_PERCENTAGE,
SOURCE_FILE_NAME,
BATCH_ID
)
FROM
(
SELECT
$1,
$2,
$3,
$4,
$5,
$6,
$7,
METADATA$FILENAME,
TO_VARCHAR(CURRENT_TIMESTAMP())
FROM @IPL_ANALYTICS.LANDING.IPL_STAGE/teamwise_home_and_away.csv
)
FILE_FORMAT = (FORMAT_NAME = IPL_ANALYTICS.LANDING.CSV_FORMAT);

--------------------------------------------------------------------------------
-- Load MATCHES_RAW
--------------------------------------------------------------------------------

COPY INTO IPL_ANALYTICS.BRONZE.MATCHES_RAW
(
ID,
SEASON,
CITY,
MATCH_DATE,
TEAM1,
TEAM2,
TOSS_WINNER,
TOSS_DECISION,
RESULT,
DL_APPLIED,
WINNER,
WIN_BY_RUNS,
WIN_BY_WICKETS,
PLAYER_OF_MATCH,
VENUE,
UMPIRE1,
UMPIRE2,
UMPIRE3,
SOURCE_FILE_NAME,
BATCH_ID
)
FROM
(
SELECT
$1,
$2,
$3,
TRY_TO_DATE($4),
$5,
$6,
$7,
$8,
$9,
$10,
$11,
$12,
$13,
$14,
$15,
$16,
$17,
$18,
METADATA$FILENAME,
TO_VARCHAR(CURRENT_TIMESTAMP())
FROM @IPL_ANALYTICS.LANDING.IPL_STAGE/matches.csv
)
FILE_FORMAT = (FORMAT_NAME = IPL_ANALYTICS.LANDING.CSV_FORMAT);

--------------------------------------------------------------------------------
-- Load DELIVERIES_RAW
--------------------------------------------------------------------------------

COPY INTO IPL_ANALYTICS.BRONZE.DELIVERIES_RAW
(
MATCH_ID,
INNING,
BATTING_TEAM,
BOWLING_TEAM,
OVER_NO,
BALL_NO,
BATSMAN,
NON_STRIKER,
BOWLER,
IS_SUPER_OVER,
WIDE_RUNS,
BYE_RUNS,
LEGBYE_RUNS,
NOBALL_RUNS,
PENALTY_RUNS,
BATSMAN_RUNS,
EXTRA_RUNS,
TOTAL_RUNS,
PLAYER_DISMISSED,
DISMISSAL_KIND,
FIELDER,
SOURCE_FILE_NAME,
BATCH_ID
)
FROM
(
SELECT
$1,$2,$3,$4,$5,$6,$7,$8,$9,
$10,$11,$12,$13,$14,$15,
$16,$17,$18,$19,$20,$21,
METADATA$FILENAME,
TO_VARCHAR(CURRENT_TIMESTAMP())
FROM @IPL_ANALYTICS.LANDING.IPL_STAGE/deliveries.csv
)
FILE_FORMAT = (FORMAT_NAME = IPL_ANALYTICS.LANDING.CSV_FORMAT);

--------------------------------------------------------------------------------
-- Validation
--------------------------------------------------------------------------------

SELECT 'MATCHES_RAW' TABLE_NAME, COUNT(*) RECORD_COUNT
FROM IPL_ANALYTICS.BRONZE.MATCHES_RAW

UNION ALL

SELECT 'DELIVERIES_RAW', COUNT(*)
FROM IPL_ANALYTICS.BRONZE.DELIVERIES_RAW

UNION ALL

SELECT 'TEAMS_RAW', COUNT(*)
FROM IPL_ANALYTICS.BRONZE.TEAMS_RAW

UNION ALL

SELECT 'PLAYERS_RAW', COUNT(*)
FROM IPL_ANALYTICS.BRONZE.PLAYERS_RAW

UNION ALL

SELECT 'PLAYER_STATS_REFERENCE_RAW', COUNT(*)
FROM IPL_ANALYTICS.BRONZE.PLAYER_STATS_REFERENCE_RAW

UNION ALL

SELECT 'TEAM_HOME_AWAY_RAW', COUNT(*)
FROM IPL_ANALYTICS.BRONZE.TEAM_HOME_AWAY_RAW;
