USE ROLE SYSADMIN;
USE DATABASE IPL_ANALYTICS;

CREATE SCHEMA IF NOT EXISTS REPORTING;

--------------------------------------------------------------------------------
-- TEAM PERFORMANCE
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_TEAM_PERFORMANCE AS
SELECT *
FROM GOLD.TEAM_PERFORMANCE;

--------------------------------------------------------------------------------
-- ORANGE CAP
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_ORANGE_CAP AS
SELECT *
FROM GOLD.ORANGE_CAP;

--------------------------------------------------------------------------------
-- PURPLE CAP
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_PURPLE_CAP AS
SELECT *
FROM GOLD.PURPLE_CAP;

--------------------------------------------------------------------------------
-- PLAYER BATTING SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_PLAYER_BATTING_SUMMARY AS
SELECT *
FROM GOLD.PLAYER_BATTING_SUMMARY;

--------------------------------------------------------------------------------
-- PLAYER BOWLING SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_PLAYER_BOWLING_SUMMARY AS
SELECT *
FROM GOLD.PLAYER_BOWLING_SUMMARY;

--------------------------------------------------------------------------------
-- VENUE ANALYTICS
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_VENUE_ANALYTICS AS
SELECT *
FROM GOLD.VENUE_ANALYTICS;

--------------------------------------------------------------------------------
-- SEASON SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_SEASON_SUMMARY AS
SELECT *
FROM GOLD.SEASON_SUMMARY;

--------------------------------------------------------------------------------
-- PLAYER OF MATCH SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_PLAYER_OF_MATCH_SUMMARY AS
SELECT *
FROM GOLD.PLAYER_OF_MATCH_SUMMARY;

--------------------------------------------------------------------------------
-- TEAM HEAD TO HEAD
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_TEAM_HEAD_TO_HEAD AS
SELECT *
FROM GOLD.TEAM_HEAD_TO_HEAD;

--------------------------------------------------------------------------------
-- DASHBOARD SUMMARY
--------------------------------------------------------------------------------

CREATE OR REPLACE VIEW REPORTING.VW_DASHBOARD_SUMMARY AS
SELECT *
FROM GOLD.DASHBOARD_SUMMARY;
