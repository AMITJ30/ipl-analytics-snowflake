/***************************************************************************************************
Script Name    : 05_file_format_stage.sql

Project        : IPL Analytics Platform

Purpose
-------
Creates reusable file format and internal stage for dataset ingestion.

Why File Format?
----------------
Defines how Snowflake should interpret incoming CSV files.

Why Stage?
-----------
Acts as a landing area for source files before loading into tables.

Objects Created
---------------
FILE FORMAT
    CSV_FORMAT

STAGE
    IPL_STAGE

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

---------------------------------------------------------
-- Create CSV File Format
---------------------------------------------------------

CREATE OR REPLACE FILE FORMAT CSV_FORMAT
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY='"'
SKIP_HEADER = 1;

---------------------------------------------------------
-- Create Internal Stage
---------------------------------------------------------

CREATE OR REPLACE STAGE IPL_STAGE
FILE_FORMAT = CSV_FORMAT;

---------------------------------------------------------
-- Validation
---------------------------------------------------------

SHOW FILE FORMATS;

SHOW STAGES;
