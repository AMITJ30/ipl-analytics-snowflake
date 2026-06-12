/***************************************************************************************************
Script Name    : 10_silver_fact_delivery.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Creates Delivery Fact Table.

What is a Fact Table?
---------------------
A fact table stores measurable business events.

In this case:

1 Row = 1 Ball Delivered

Architecture
------------

BRONZE.DELIVERIES_RAW
            │
            ▼
SILVER.FACT_DELIVERY

Business Questions Supported
----------------------------
- Orange Cap Analysis
- Purple Cap Analysis
- Strike Rate Analysis
- Economy Rate Analysis
- Boundary Analysis
- Dot Ball Analysis
- Wicket Analysis
- Batter vs Bowler Analysis

Silver Layer Enhancements
-------------------------
The following derived columns are added:

IS_DOT_BALL
IS_FOUR
IS_SIX
IS_WICKET

Benefits
--------
Business users can directly consume these columns without
repeating calculations in every report.

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

USE SCHEMA SILVER;

--------------------------------------------------------------------------------
-- FACT_DELIVERY
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE FACT_DELIVERY
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

    PLAYER_DISMISSED STRING,

    DISMISSAL_KIND STRING,

    FIELDER STRING,

    --------------------------------------------------------------------------------
    -- Derived Metrics
    --------------------------------------------------------------------------------

    IS_DOT_BALL NUMBER,

    IS_FOUR NUMBER,

    IS_SIX NUMBER,

    IS_WICKET NUMBER,

    CREATED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Load FACT_DELIVERY
--------------------------------------------------------------------------------

INSERT INTO FACT_DELIVERY
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
    BATSMAN_RUNS,
    EXTRA_RUNS,
    TOTAL_RUNS,
    PLAYER_DISMISSED,
    DISMISSAL_KIND,
    FIELDER,
    IS_DOT_BALL,
    IS_FOUR,
    IS_SIX,
    IS_WICKET
)
SELECT

    MATCH_ID,

    INNING,

    BATTING_TEAM,

    BOWLING_TEAM,

    OVER_NO,

    BALL_NO,

    BATSMAN,

    NON_STRIKER,

    BOWLER,

    BATSMAN_RUNS,

    EXTRA_RUNS,

    TOTAL_RUNS,

    PLAYER_DISMISSED,

    DISMISSAL_KIND,

    FIELDER,

    --------------------------------------------------------------------------------
    -- Dot Ball Flag
    --------------------------------------------------------------------------------

    CASE
        WHEN TOTAL_RUNS = 0 THEN 1
        ELSE 0
    END AS IS_DOT_BALL,

    --------------------------------------------------------------------------------
    -- Four Flag
    --------------------------------------------------------------------------------

    CASE
        WHEN BATSMAN_RUNS = 4 THEN 1
        ELSE 0
    END AS IS_FOUR,

    --------------------------------------------------------------------------------
    -- Six Flag
    --------------------------------------------------------------------------------

    CASE
        WHEN BATSMAN_RUNS = 6 THEN 1
        ELSE 0
    END AS IS_SIX,

    --------------------------------------------------------------------------------
    -- Wicket Flag
    --------------------------------------------------------------------------------

    CASE
        WHEN PLAYER_DISMISSED IS NOT NULL THEN 1
        ELSE 0
    END AS IS_WICKET

FROM BRONZE.DELIVERIES_RAW;

--------------------------------------------------------------------------------
-- Validation
--------------------------------------------------------------------------------

SELECT COUNT(*) AS DELIVERY_COUNT
FROM FACT_DELIVERY;

--------------------------------------------------------------------------------
-- Sample Data
--------------------------------------------------------------------------------

SELECT *
FROM FACT_DELIVERY
LIMIT 20;

--------------------------------------------------------------------------------
-- Business Validation Queries
--------------------------------------------------------------------------------

-- Total Fours

SELECT
SUM(IS_FOUR) AS TOTAL_FOURS
FROM FACT_DELIVERY;

--------------------------------------------------------------------------------

-- Total Sixes

SELECT
SUM(IS_SIX) AS TOTAL_SIXES
FROM FACT_DELIVERY;

--------------------------------------------------------------------------------

-- Total Wickets

SELECT
SUM(IS_WICKET) AS TOTAL_WICKETS
FROM FACT_DELIVERY;

--------------------------------------------------------------------------------

-- Total Dot Balls

SELECT
SUM(IS_DOT_BALL) AS TOTAL_DOT_BALLS
FROM FACT_DELIVERY;

--------------------------------------------------------------------------------

-- Top Run Scorers

SELECT
BATSMAN,
SUM(BATSMAN_RUNS) AS RUNS
FROM FACT_DELIVERY
GROUP BY BATSMAN
ORDER BY RUNS DESC
LIMIT 10;

--------------------------------------------------------------------------------

-- Top Wicket Takers

SELECT
BOWLER,
SUM(IS_WICKET) AS WICKETS
FROM FACT_DELIVERY
GROUP BY BOWLER
ORDER BY WICKETS DESC
LIMIT 10;

--------------------------------------------------------------------------------

-- Expected Result

-- FACT_DELIVERY ≈ 179,078 rows

--------------------------------------------------------------------------------
