/***************************************************************************************************
Script Name    : 03_database_setup.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Creates the database and schema structure for the IPL Analytics project.

Why are we creating multiple schemas?
-------------------------------------

We are following the Medallion Architecture pattern.

BRONZE
------
Stores raw data exactly as received from source files.

SILVER
------
Stores cleaned and standardized data.

GOLD
----
Stores business-ready aggregated datasets for reporting.

UTIL
----
Stores utility objects such as:
- Streams
- Tasks
- Stored Procedures
- Audit Tables

Architecture
------------

IPL_ANALYTICS
├── BRONZE
├── SILVER
├── GOLD
└── UTIL

Benefits
--------
- Better organization
- Improved governance
- Easier maintenance
- Supports scalable data pipelines

Prerequisites
-------------
- IPL_WH Warehouse created
- SYSADMIN role access

***************************************************************************************************/

USE ROLE SYSADMIN;

---------------------------------------------------------
-- Create Database
---------------------------------------------------------

CREATE DATABASE IF NOT EXISTS IPL_ANALYTICS;

---------------------------------------------------------
-- Create Schemas
---------------------------------------------------------

USE DATABASE IPL_ANALYTICS;

CREATE SCHEMA IF NOT EXISTS BRONZE;
CREATE SCHEMA IF NOT EXISTS SILVER;
CREATE SCHEMA IF NOT EXISTS GOLD;
CREATE SCHEMA IF NOT EXISTS UTIL;

---------------------------------------------------------
-- Validation
---------------------------------------------------------

SHOW SCHEMAS;
