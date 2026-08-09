/***************************************************************************************************
Script Name : 13_gold_analytics.sql

Project      : IPL Analytics Platform
Author       : Amit Jha

Purpose
-------
Creates the Gold Layer of the Medallion Architecture.

The Gold Layer contains business-ready analytical tables used by
Power BI, Streamlit dashboards and reporting applications.

Source Layer
------------
SILVER

Target Layer
------------
GOLD

***************************************************************************************************/

USE ROLE SYSADMIN;
USE DATABASE IPL_ANALYTICS;

CREATE SCHEMA IF NOT EXISTS GOLD;

USE SCHEMA GOLD;

--------------------------------------------------------------------------------
-- TEAM PERFORMANCE
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE TEAM_PERFORMANCE AS

WITH TEAM_MATCHES AS
(
    SELECT
        TEAM1 AS TEAM_NAME,
        MATCH_WINNER
    FROM SILVER.FACT_MATCH

    UNION ALL

    SELECT
        TEAM2 AS TEAM_NAME,
        MATCH_WINNER
    FROM SILVER.FACT_MATCH
)

SELECT

    TEAM_NAME,

    COUNT(*) AS MATCHES_PLAYED,

    SUM(
        CASE
            WHEN TEAM_NAME = MATCH_WINNER
            THEN 1
            ELSE 0
        END
    ) AS MATCHES_WON,

    COUNT(*) -
    SUM(
        CASE
            WHEN TEAM_NAME = MATCH_WINNER
            THEN 1
            ELSE 0
        END
    ) AS MATCHES_LOST,

    ROUND(
        (
            SUM(
                CASE
                    WHEN TEAM_NAME = MATCH_WINNER
                    THEN 1
                    ELSE 0
                END
            ) * 100.0
        ) / COUNT(*),
        2
    ) AS WIN_PERCENTAGE

FROM TEAM_MATCHES

GROUP BY TEAM_NAME

ORDER BY MATCHES_WON DESC;

--------------------------------------------------------------------------------
-- PLAYER BATTING SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE PLAYER_BATTING_SUMMARY AS

SELECT

    BATSMAN,

    COUNT(*) AS BALLS_FACED,

    SUM(BATSMAN_RUNS) AS TOTAL_RUNS,

    SUM(IS_FOUR) AS FOURS,

    SUM(IS_SIX) AS SIXES,

    ROUND(
        SUM(BATSMAN_RUNS) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS STRIKE_RATE,

    ROUND(
        SUM(BATSMAN_RUNS) * 1.0 /
        NULLIF(
            SUM(
                CASE
                    WHEN IS_WICKET = 1 THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS BATTING_AVERAGE

FROM SILVER.FACT_DELIVERY

GROUP BY BATSMAN

ORDER BY TOTAL_RUNS DESC;

--------------------------------------------------------------------------------
-- ORANGE CAP LEADERBOARD
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE ORANGE_CAP AS

SELECT

    ROW_NUMBER() OVER
    (
        ORDER BY TOTAL_RUNS DESC,
                 STRIKE_RATE DESC
    ) AS PLAYER_RANK,

    BATSMAN,

    TOTAL_RUNS,

    BALLS_FACED,

    FOURS,

    SIXES,

    STRIKE_RATE,

    BATTING_AVERAGE

FROM PLAYER_BATTING_SUMMARY

ORDER BY PLAYER_RANK;

--------------------------------------------------------------------------------
-- PLAYER BOWLING SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE PLAYER_BOWLING_SUMMARY AS

SELECT

    BOWLER,

    COUNT(*) AS BALLS_BOWLED,

    SUM(TOTAL_RUNS) AS RUNS_CONCEDED,

    SUM(IS_DOT_BALL) AS DOT_BALLS,

    SUM(IS_WICKET) AS WICKETS,

    ROUND(
        (SUM(TOTAL_RUNS) * 6.0) /
        NULLIF(COUNT(*), 0),
        2
    ) AS ECONOMY,

    ROUND(
        COUNT(*) * 1.0 /
        NULLIF(SUM(IS_WICKET), 0),
        2
    ) AS BOWLING_STRIKE_RATE,

    ROUND(
        SUM(TOTAL_RUNS) * 1.0 /
        NULLIF(SUM(IS_WICKET), 0),
        2
    ) AS BOWLING_AVERAGE

FROM SILVER.FACT_DELIVERY

GROUP BY BOWLER

ORDER BY WICKETS DESC;

--------------------------------------------------------------------------------
-- VALIDATION
--------------------------------------------------------------------------------

SELECT *
FROM PLAYER_BOWLING_SUMMARY
LIMIT 10;

--------------------------------------------------------------------------------
-- PURPLE CAP LEADERBOARD
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE PURPLE_CAP AS

SELECT

    ROW_NUMBER() OVER
    (
        ORDER BY WICKETS DESC,
                 ECONOMY ASC,
                 BOWLING_STRIKE_RATE ASC
    ) AS PLAYER_RANK,

    BOWLER,

    WICKETS,

    BALLS_BOWLED,

    RUNS_CONCEDED,

    DOT_BALLS,

    ECONOMY,

    BOWLING_STRIKE_RATE,

    BOWLING_AVERAGE

FROM PLAYER_BOWLING_SUMMARY

ORDER BY PLAYER_RANK;

--------------------------------------------------------------------------------
-- VENUE ANALYTICS
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE VENUE_ANALYTICS AS

WITH MATCH_RUNS AS
(
    SELECT

        MATCH_ID,

        SUM(TOTAL_RUNS) AS TOTAL_MATCH_RUNS,

        SUM(IS_WICKET) AS TOTAL_WICKETS

    FROM SILVER.FACT_DELIVERY

    GROUP BY MATCH_ID
)

SELECT

    FM.VENUE,

    COUNT(FM.MATCH_ID) AS MATCHES_PLAYED,

    SUM(MR.TOTAL_MATCH_RUNS) AS TOTAL_RUNS,

    SUM(MR.TOTAL_WICKETS) AS TOTAL_WICKETS,

    ROUND(
        AVG(MR.TOTAL_MATCH_RUNS),
        2
    ) AS AVERAGE_RUNS_PER_MATCH,

    MAX(MR.TOTAL_MATCH_RUNS) AS HIGHEST_MATCH_SCORE,

    MIN(MR.TOTAL_MATCH_RUNS) AS LOWEST_MATCH_SCORE

FROM SILVER.FACT_MATCH FM

JOIN MATCH_RUNS MR
ON FM.MATCH_ID = MR.MATCH_ID

GROUP BY FM.VENUE

ORDER BY MATCHES_PLAYED DESC;

--------------------------------------------------------------------------------
-- VALIDATION
--------------------------------------------------------------------------------

SELECT *
FROM VENUE_ANALYTICS
LIMIT 10;

--------------------------------------------------------------------------------
-- SEASON SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE SEASON_SUMMARY AS

WITH MATCH_STATS AS
(
    SELECT

        MATCH_ID,

        SUM(TOTAL_RUNS) AS MATCH_RUNS,

        SUM(IS_WICKET) AS MATCH_WICKETS

    FROM SILVER.FACT_DELIVERY

    GROUP BY MATCH_ID
)

SELECT

    FM.SEASON,

    COUNT(FM.MATCH_ID) AS TOTAL_MATCHES,

    SUM(MS.MATCH_RUNS) AS TOTAL_RUNS,

    SUM(MS.MATCH_WICKETS) AS TOTAL_WICKETS,

    ROUND(
        AVG(MS.MATCH_RUNS),
        2
    ) AS AVERAGE_RUNS_PER_MATCH,

    MAX(MS.MATCH_RUNS) AS HIGHEST_MATCH_SCORE,

    MIN(MS.MATCH_RUNS) AS LOWEST_MATCH_SCORE,

    COUNT(DISTINCT FM.VENUE) AS TOTAL_VENUES,

    COUNT(DISTINCT FM.TEAM1)
    + COUNT(DISTINCT FM.TEAM2)
    - COUNT(DISTINCT CASE
            WHEN FM.TEAM1 = FM.TEAM2 THEN FM.TEAM1
        END) AS TEAM_OCCURRENCES,

    COUNT(DISTINCT FM.MATCH_WINNER) AS UNIQUE_WINNERS

FROM SILVER.FACT_MATCH FM

JOIN MATCH_STATS MS
ON FM.MATCH_ID = MS.MATCH_ID

GROUP BY FM.SEASON

ORDER BY FM.SEASON;

--------------------------------------------------------------------------------
-- VALIDATION
--------------------------------------------------------------------------------

SELECT *
FROM SEASON_SUMMARY
ORDER BY SEASON;

--------------------------------------------------------------------------------
-- PLAYER OF THE MATCH SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE PLAYER_OF_MATCH_SUMMARY AS

SELECT

    PLAYER_OF_MATCH,

    COUNT(*) AS AWARDS_WON,

    MIN(SEASON) AS FIRST_SEASON,

    MAX(SEASON) AS LAST_SEASON,

    COUNT(DISTINCT MATCH_WINNER) AS DIFFERENT_WINNING_TEAMS

FROM SILVER.FACT_MATCH

WHERE PLAYER_OF_MATCH IS NOT NULL

GROUP BY PLAYER_OF_MATCH

ORDER BY AWARDS_WON DESC;

--------------------------------------------------------------------------------
-- TEAM HEAD TO HEAD
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE TEAM_HEAD_TO_HEAD AS

SELECT

    TEAM1,

    TEAM2,

    COUNT(*) AS MATCHES_PLAYED,

    SUM(
        CASE
            WHEN MATCH_WINNER = TEAM1 THEN 1
            ELSE 0
        END
    ) AS TEAM1_WINS,

    SUM(
        CASE
            WHEN MATCH_WINNER = TEAM2 THEN 1
            ELSE 0
        END
    ) AS TEAM2_WINS,

    SUM(
        CASE
            WHEN MATCH_WINNER IS NULL THEN 1
            ELSE 0
        END
    ) AS NO_RESULT_MATCHES,

    ROUND(
        SUM(
            CASE
                WHEN MATCH_WINNER = TEAM1 THEN 1
                ELSE 0
            END
        ) * 100.0 /
        COUNT(*),
        2
    ) AS TEAM1_WIN_PERCENTAGE,

    ROUND(
        SUM(
            CASE
                WHEN MATCH_WINNER = TEAM2 THEN 1
                ELSE 0
            END
        ) * 100.0 /
        COUNT(*),
        2
    ) AS TEAM2_WIN_PERCENTAGE

FROM SILVER.FACT_MATCH

GROUP BY
    TEAM1,
    TEAM2

ORDER BY
    MATCHES_PLAYED DESC,
    TEAM1,
    TEAM2;

--------------------------------------------------------------------------------
-- VALIDATION
--------------------------------------------------------------------------------

SELECT *
FROM TEAM_HEAD_TO_HEAD
LIMIT 10;

--------------------------------------------------------------------------------
-- ORANGE_CAP_BY_SEASON
--------------------------------------------------------------------------------
CREATE OR REPLACE TABLE GOLD.ORANGE_CAP_BY_SEASON AS

WITH PLAYER_STATS AS (

    SELECT
        M.SEASON,
        D.BATSMAN,

        SUM(D.BATSMAN_RUNS) AS TOTAL_RUNS,

        COUNT(*) AS BALLS_FACED,

        SUM(
            CASE
                WHEN D.IS_FOUR = TRUE THEN 1
                ELSE 0
            END
        ) AS FOURS,

        SUM(
            CASE
                WHEN D.IS_SIX = TRUE THEN 1
                ELSE 0
            END
        ) AS SIXES,

        COUNT(
            DISTINCT CASE
                WHEN D.PLAYER_DISMISSED = D.BATSMAN
                THEN D.MATCH_ID || '-' || D.INNING
            END
        ) AS DISMISSALS

    FROM SILVER.FACT_DELIVERY D

    INNER JOIN SILVER.FACT_MATCH M
        ON D.MATCH_ID = M.MATCH_ID

    GROUP BY
        M.SEASON,
        D.BATSMAN
),

CALCULATED_STATS AS (

    SELECT
        SEASON,
        BATSMAN,
        TOTAL_RUNS,
        BALLS_FACED,
        FOURS,
        SIXES,

        ROUND(
            TOTAL_RUNS * 100.0 /
            NULLIF(BALLS_FACED, 0),
            2
        ) AS STRIKE_RATE,

        ROUND(
            TOTAL_RUNS * 1.0 /
            NULLIF(DISMISSALS, 0),
            2
        ) AS BATTING_AVERAGE

    FROM PLAYER_STATS
),

RANKED_PLAYERS AS (

    SELECT
        SEASON,

        ROW_NUMBER() OVER (
            PARTITION BY SEASON
            ORDER BY TOTAL_RUNS DESC
        ) AS PLAYER_RANK,

        BATSMAN,
        TOTAL_RUNS,
        BALLS_FACED,
        FOURS,
        SIXES,
        STRIKE_RATE,
        BATTING_AVERAGE

    FROM CALCULATED_STATS
)

SELECT
    SEASON,
    PLAYER_RANK,
    BATSMAN,
    TOTAL_RUNS,
    BALLS_FACED,
    FOURS,
    SIXES,
    STRIKE_RATE,
    BATTING_AVERAGE

FROM RANKED_PLAYERS;
--------------------------------------------------------------------------------
-- VALIDATION
--------------------------------------------------------------------------------
SELECT *
FROM GOLD.ORANGE_CAP_BY_SEASON
WHERE SEASON = 'IPL-2008'
ORDER BY PLAYER_RANK
LIMIT 10;
--------------------------------------------------------------------------------
-- DASHBOARD SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE DASHBOARD_SUMMARY AS

WITH MATCH_STATS AS
(
    SELECT

        MATCH_ID,

        SUM(TOTAL_RUNS) AS MATCH_RUNS,

        SUM(IS_WICKET) AS MATCH_WICKETS

    FROM SILVER.FACT_DELIVERY

    GROUP BY MATCH_ID
)

SELECT

    /* Match Statistics */
    (SELECT COUNT(*) FROM SILVER.FACT_MATCH) AS TOTAL_MATCHES,

    (SELECT COUNT(DISTINCT SEASON)
     FROM SILVER.FACT_MATCH) AS TOTAL_SEASONS,

    /* Team Statistics */
    (SELECT COUNT(*)
     FROM SILVER.DIM_TEAM) AS TOTAL_TEAMS,

    /* Player Statistics */
    (SELECT COUNT(*)
     FROM SILVER.DIM_PLAYER) AS TOTAL_PLAYERS,

    /* Venue Statistics */
    (SELECT COUNT(DISTINCT VENUE)
     FROM SILVER.FACT_MATCH) AS TOTAL_VENUES,

    /* Delivery Statistics */
    (SELECT COUNT(*)
     FROM SILVER.FACT_DELIVERY) AS TOTAL_DELIVERIES,

    /* Runs */
    (SELECT SUM(TOTAL_RUNS)
     FROM SILVER.FACT_DELIVERY) AS TOTAL_RUNS,

    /* Wickets */
    (SELECT SUM(IS_WICKET)
     FROM SILVER.FACT_DELIVERY) AS TOTAL_WICKETS,

    /* Highest Match Score */
    (SELECT MAX(MATCH_RUNS)
     FROM MATCH_STATS) AS HIGHEST_MATCH_SCORE,

    /* Lowest Match Score */
    (SELECT MIN(MATCH_RUNS)
     FROM MATCH_STATS) AS LOWEST_MATCH_SCORE,

    /* Average Match Score */
    (SELECT ROUND(AVG(MATCH_RUNS),2)
     FROM MATCH_STATS) AS AVERAGE_MATCH_SCORE;

--------------------------------------------------------------------------------
-- DASHBOARD SUMMARY
--------------------------------------------------------------------------------

SELECT *
FROM DASHBOARD_SUMMARY;
