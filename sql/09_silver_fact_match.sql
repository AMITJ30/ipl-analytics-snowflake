/***************************************************************************************************
Script Name    : 09_silver_fact_match.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Creates Match Fact Table.

What is a Fact Table?
---------------------
A fact table stores measurable business events.

In this case:

1 Row = 1 IPL Match

Architecture
------------

BRONZE.MATCHES_RAW
          │
          ▼
SILVER.FACT_MATCH

Business Questions Supported
----------------------------
- Which team wins most matches?
- Does toss impact match outcome?
- Which venue hosts most matches?
- Who wins Player of Match most often?
- Which season had the most matches?

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

USE SCHEMA SILVER;

--------------------------------------------------------------------------------
-- FACT_MATCH
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE FACT_MATCH
(
    MATCH_ID NUMBER,

    SEASON STRING,

    MATCH_DATE DATE,

    CITY STRING,

    TEAM1 STRING,

    TEAM2 STRING,

    TOSS_WINNER STRING,

    TOSS_DECISION STRING,

    MATCH_WINNER STRING,

    WIN_BY_RUNS NUMBER,

    WIN_BY_WICKETS NUMBER,

    PLAYER_OF_MATCH STRING,

    VENUE STRING,

    CREATED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Load FACT_MATCH
--------------------------------------------------------------------------------

INSERT INTO FACT_MATCH
(
    MATCH_ID,
    SEASON,
    MATCH_DATE,
    CITY,
    TEAM1,
    TEAM2,
    TOSS_WINNER,
    TOSS_DECISION,
    MATCH_WINNER,
    WIN_BY_RUNS,
    WIN_BY_WICKETS,
    PLAYER_OF_MATCH,
    VENUE
)
SELECT
ID,
SEASON,
MATCH_DATE,
CITY,
TEAM1,
TEAM2,
TOSS_WINNER,
TOSS_DECISION,
WINNER,
WIN_BY_RUNS,
WIN_BY_WICKETS,
PLAYER_OF_MATCH,
VENUE
FROM BRONZE.MATCHES_RAW;

--------------------------------------------------------------------------------
-- Validation
--------------------------------------------------------------------------------

SELECT COUNT(*) AS MATCH_COUNT
FROM FACT_MATCH;

--------------------------------------------------------------------------------
-- Sample Data
--------------------------------------------------------------------------------

SELECT *
FROM FACT_MATCH
LIMIT 10;
