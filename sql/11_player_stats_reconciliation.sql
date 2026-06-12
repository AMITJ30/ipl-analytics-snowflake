/***************************************************************************************************
Script Name    : 11_player_stats_reconciliation.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Validate calculated player batting statistics against
reference statistics dataset.

Why Reconciliation?
-------------------
Data Engineering projects should not only load and transform data,
but also validate that calculations are accurate.

This script compares:

1. Calculated statistics from FACT_DELIVERY
2. Reference statistics from PLAYER_STATS_REFERENCE_RAW

Validation Metrics
------------------
- Total Runs
- Balls Faced
- Outs
- Strike Rate

Benefits
--------
1. Data Quality Validation
2. Auditability
3. Reconciliation Framework
4. Production-Ready Design

Architecture
------------

FACT_DELIVERY
        │
        ▼

CALCULATED PLAYER STATS

        VS

PLAYER_STATS_REFERENCE_RAW

        │
        ▼

RECONCILIATION RESULTS

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

--------------------------------------------------------------------------------
-- Create Reconciliation View
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW SILVER.VW_PLAYER_STATS_RECONCILIATION AS

WITH CALCULATED_STATS AS
(
    SELECT

        BATSMAN,

        SUM(BATSMAN_RUNS) AS CALCULATED_RUNS,

        COUNT(*) AS CALCULATED_BALLS,

        SUM(IS_WICKET) AS CALCULATED_OUTS,

        ROUND
        (
            SUM(BATSMAN_RUNS) * 100.0
            /
            NULLIF(COUNT(*),0),
            2
        ) AS CALCULATED_STRIKE_RATE

    FROM SILVER.FACT_DELIVERY

    GROUP BY BATSMAN
)

SELECT

    C.BATSMAN,

    --------------------------------------------------------------------------
    -- Runs Validation
    --------------------------------------------------------------------------

    C.CALCULATED_RUNS,

    R.TOTAL_RUNS AS REFERENCE_RUNS,

    C.CALCULATED_RUNS - R.TOTAL_RUNS
        AS RUN_VARIANCE,

    --------------------------------------------------------------------------
    -- Balls Validation
    --------------------------------------------------------------------------

    C.CALCULATED_BALLS,

    R.NUMBER_OF_BALLS AS REFERENCE_BALLS,

    C.CALCULATED_BALLS - R.NUMBER_OF_BALLS
        AS BALL_VARIANCE,

    --------------------------------------------------------------------------
    -- Outs Validation
    --------------------------------------------------------------------------

    C.CALCULATED_OUTS,

    R.OUTS AS REFERENCE_OUTS,

    C.CALCULATED_OUTS - R.OUTS
        AS OUT_VARIANCE,

    --------------------------------------------------------------------------
    -- Strike Rate Validation
    --------------------------------------------------------------------------

    C.CALCULATED_STRIKE_RATE,

    R.STRIKE_RATE AS REFERENCE_STRIKE_RATE,

    ROUND
    (
        C.CALCULATED_STRIKE_RATE - R.STRIKE_RATE,
        2
    )
    AS STRIKE_RATE_VARIANCE,

    --------------------------------------------------------------------------
    -- Validation Status
    --------------------------------------------------------------------------

    CASE
        WHEN
            ABS(C.CALCULATED_RUNS - R.TOTAL_RUNS) = 0
        THEN 'PASS'

        ELSE 'FAIL'

    END AS VALIDATION_STATUS

FROM CALCULATED_STATS C

INNER JOIN BRONZE.PLAYER_STATS_REFERENCE_RAW R
ON UPPER(TRIM(C.BATSMAN))
=
UPPER(TRIM(R.BATSMAN));

--------------------------------------------------------------------------------
-- Validation Queries
--------------------------------------------------------------------------------

SELECT *
FROM SILVER.VW_PLAYER_STATS_RECONCILIATION
LIMIT 20;

--------------------------------------------------------------------------------
-- Total Pass / Fail Count
--------------------------------------------------------------------------------

SELECT

    VALIDATION_STATUS,

    COUNT(*) AS PLAYER_COUNT

FROM SILVER.VW_PLAYER_STATS_RECONCILIATION

GROUP BY VALIDATION_STATUS;

--------------------------------------------------------------------------------
-- Players with Variance
--------------------------------------------------------------------------------

SELECT *

FROM SILVER.VW_PLAYER_STATS_RECONCILIATION

WHERE RUN_VARIANCE <> 0

ORDER BY ABS(RUN_VARIANCE) DESC;

--------------------------------------------------------------------------------
-- Top 20 Run Scorers Validation
--------------------------------------------------------------------------------

SELECT *

FROM SILVER.VW_PLAYER_STATS_RECONCILIATION

ORDER BY CALCULATED_RUNS DESC

LIMIT 20;

--------------------------------------------------------------------------------
-- Summary Metrics
--------------------------------------------------------------------------------

SELECT

    COUNT(*) AS TOTAL_PLAYERS,

    SUM
    (
        CASE
            WHEN VALIDATION_STATUS='PASS'
            THEN 1
            ELSE 0
        END
    ) AS PASSED_PLAYERS,

    SUM
    (
        CASE
            WHEN VALIDATION_STATUS='FAIL'
            THEN 1
            ELSE 0
        END
    ) AS FAILED_PLAYERS

FROM SILVER.VW_PLAYER_STATS_RECONCILIATION;

--------------------------------------------------------------------------------
-- Expected Outcome
--------------------------------------------------------------------------------

-- Reconciliation View Created
-- Player Statistics Validated
-- Data Quality Framework Established
-- Ready for Gold Layer Development

--------------------------------------------------------------------------------
