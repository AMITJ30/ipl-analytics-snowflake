/***************************************************************************************************
Script Name    : 08_silver_dimensions.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Creates Silver Layer Dimension Tables.

What is Silver Layer?
---------------------
The Silver Layer contains cleaned, standardized and business-ready entities.

Data is transformed from Bronze tables into reusable dimensions and facts.

Architecture
------------

BRONZE
│
├── TEAMS_RAW
└── PLAYERS_RAW

        │
        ▼

SILVER
│
├── DIM_TEAM
└── DIM_PLAYER

Benefits
--------
1. Standardized Data
2. Business-Friendly Structure
3. Reusable Across Reports
4. Supports Star Schema Design

Objects Created
---------------
DIM_TEAM
DIM_PLAYER

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

USE SCHEMA SILVER;

--------------------------------------------------------------------------------
-- DIM_TEAM
--------------------------------------------------------------------------------
-- Stores IPL Team Master Data
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_TEAM
(
    TEAM_KEY NUMBER AUTOINCREMENT,

    TEAM_NAME STRING,

    TEAM_SHORT_NAME STRING,

    HOME_CITY STRING,

    HOME_GROUND STRING,

    IS_ACTIVE BOOLEAN,

    CREATED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Load DIM_TEAM
--------------------------------------------------------------------------------

INSERT INTO DIM_TEAM
(
    TEAM_NAME,
    TEAM_SHORT_NAME,
    HOME_CITY,
    HOME_GROUND,
    IS_ACTIVE
)
SELECT
TEAM_NAME,

CASE TEAM_NAME
    WHEN 'Chennai Super Kings' THEN 'CSK'
    WHEN 'Mumbai Indians' THEN 'MI'
    WHEN 'Royal Challengers Bangalore' THEN 'RCB'
    WHEN 'Kolkata Knight Riders' THEN 'KKR'
    WHEN 'Delhi Capitals' THEN 'DC'
    WHEN 'Delhi Daredevils' THEN 'DD'
    WHEN 'Kings XI Punjab' THEN 'KXIP'
    WHEN 'Punjab Kings' THEN 'PBKS'
    WHEN 'Sunrisers Hyderabad' THEN 'SRH'
    WHEN 'Deccan Chargers' THEN 'DCG'
    WHEN 'Rajasthan Royals' THEN 'RR'
    WHEN 'Gujarat Lions' THEN 'GL'
    WHEN 'Pune Warriors' THEN 'PW'
    WHEN 'Kochi Tuskers Kerala' THEN 'KTK'
    WHEN 'Rising Pune Supergiant' THEN 'RPS'
    WHEN 'Rising Pune Supergiants' THEN 'RPS'
END,

CASE TEAM_NAME
    WHEN 'Chennai Super Kings' THEN 'Chennai'
    WHEN 'Mumbai Indians' THEN 'Mumbai'
    WHEN 'Royal Challengers Bangalore' THEN 'Bengaluru'
    WHEN 'Kolkata Knight Riders' THEN 'Kolkata'
    WHEN 'Delhi Capitals' THEN 'Delhi'
    WHEN 'Delhi Daredevils' THEN 'Delhi'
    WHEN 'Kings XI Punjab' THEN 'Mohali'
    WHEN 'Punjab Kings' THEN 'Mohali'
    WHEN 'Sunrisers Hyderabad' THEN 'Hyderabad'
    WHEN 'Deccan Chargers' THEN 'Hyderabad'
    WHEN 'Rajasthan Royals' THEN 'Jaipur'
    WHEN 'Gujarat Lions' THEN 'Rajkot'
    WHEN 'Pune Warriors' THEN 'Pune'
    WHEN 'Kochi Tuskers Kerala' THEN 'Kochi'
    WHEN 'Rising Pune Supergiant' THEN 'Pune'
    WHEN 'Rising Pune Supergiants' THEN 'Pune'
END,

CASE TEAM_NAME
    WHEN 'Chennai Super Kings' THEN 'M. A. Chidambaram Stadium'
    WHEN 'Mumbai Indians' THEN 'Wankhede Stadium'
    WHEN 'Royal Challengers Bangalore' THEN 'M. Chinnaswamy Stadium'
    WHEN 'Kolkata Knight Riders' THEN 'Eden Gardens'
    WHEN 'Delhi Capitals' THEN 'Arun Jaitley Stadium'
    WHEN 'Delhi Daredevils' THEN 'Arun Jaitley Stadium'
    WHEN 'Kings XI Punjab' THEN 'IS Bindra Stadium'
    WHEN 'Punjab Kings' THEN 'IS Bindra Stadium'
    WHEN 'Sunrisers Hyderabad' THEN 'Rajiv Gandhi Stadium'
    WHEN 'Deccan Chargers' THEN 'Rajiv Gandhi Stadium'
    WHEN 'Rajasthan Royals' THEN 'Sawai Mansingh Stadium'
    WHEN 'Gujarat Lions' THEN 'Saurashtra Cricket Association Stadium'
    WHEN 'Pune Warriors' THEN 'MCA Stadium'
    WHEN 'Kochi Tuskers Kerala' THEN 'Jawaharlal Nehru Stadium'
    WHEN 'Rising Pune Supergiant' THEN 'MCA Stadium'
    WHEN 'Rising Pune Supergiants' THEN 'MCA Stadium'
END,

TRUE

FROM BRONZE.TEAMS_RAW;

--------------------------------------------------------------------------------
-- DIM_PLAYER
--------------------------------------------------------------------------------
-- Stores Player Master Data
--------------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_PLAYER
(
    PLAYER_KEY NUMBER AUTOINCREMENT,

    PLAYER_NAME STRING,

    DOB DATE,

    AGE NUMBER,

    COUNTRY STRING,

    BATTING_HAND STRING,

    BOWLING_SKILL STRING,

    CREATED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Load DIM_PLAYER
--------------------------------------------------------------------------------

INSERT INTO DIM_PLAYER
(
    PLAYER_NAME,
    DOB,
    AGE,
    COUNTRY,
    BATTING_HAND,
    BOWLING_SKILL
)
SELECT
PLAYER_NAME,

DOB,

DATEDIFF(YEAR,DOB,CURRENT_DATE()) AS AGE,

COUNTRY,

BATTING_HAND,

BOWLING_SKILL

FROM BRONZE.PLAYERS_RAW;

--------------------------------------------------------------------------------
-- Validation
--------------------------------------------------------------------------------

SELECT COUNT(*) AS TEAM_COUNT
FROM DIM_TEAM;

SELECT COUNT(*) AS PLAYER_COUNT
FROM DIM_PLAYER;

--------------------------------------------------------------------------------
-- Sample Data Validation
--------------------------------------------------------------------------------

SELECT *
FROM DIM_TEAM
LIMIT 10;

SELECT *
FROM DIM_PLAYER
LIMIT 10;
