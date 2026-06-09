/***************************************************************************************************
Script Name    : 04_grants.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Grant required permissions to project roles.

Why?
----
Roles alone do not provide access.

Permissions must be granted on:
- Warehouse
- Database
- Schemas
- Future Objects

Role Responsibilities
---------------------

IPL_INGEST
-----------
- Manage file ingestion
- Access Landing layer
- Load data into Bronze layer

IPL_TRANSFORM
--------------
- Build Silver and Gold layers
- Create tables and transformations

IPL_REPORTING
--------------
- Read-only access to Gold layer
- Used by dashboards and analytics users

Security Principle
------------------
Least Privilege Access

***************************************************************************************************/

USE ROLE SECURITYADMIN;

---------------------------------------------------------
-- Warehouse Access
---------------------------------------------------------

GRANT USAGE
ON WAREHOUSE IPL_WH
TO ROLE IPL_INGEST;

GRANT USAGE
ON WAREHOUSE IPL_WH
TO ROLE IPL_TRANSFORM;

GRANT USAGE
ON WAREHOUSE IPL_WH
TO ROLE IPL_REPORTING;

---------------------------------------------------------
-- Database Access
---------------------------------------------------------

GRANT USAGE
ON DATABASE IPL_ANALYTICS
TO ROLE IPL_INGEST;

GRANT USAGE
ON DATABASE IPL_ANALYTICS
TO ROLE IPL_TRANSFORM;

GRANT USAGE
ON DATABASE IPL_ANALYTICS
TO ROLE IPL_REPORTING;

---------------------------------------------------------
-- LANDING Schema
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.LANDING
TO ROLE IPL_INGEST;

GRANT CREATE STAGE
ON SCHEMA IPL_ANALYTICS.LANDING
TO ROLE IPL_INGEST;

GRANT CREATE FILE FORMAT
ON SCHEMA IPL_ANALYTICS.LANDING
TO ROLE IPL_INGEST;

---------------------------------------------------------
-- BRONZE Schema
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.BRONZE
TO ROLE IPL_INGEST;

GRANT CREATE TABLE
ON SCHEMA IPL_ANALYTICS.BRONZE
TO ROLE IPL_INGEST;

---------------------------------------------------------
-- SILVER Schema
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.SILVER
TO ROLE IPL_TRANSFORM;

GRANT CREATE TABLE
ON SCHEMA IPL_ANALYTICS.SILVER
TO ROLE IPL_TRANSFORM;

---------------------------------------------------------
-- GOLD Schema
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.GOLD
TO ROLE IPL_TRANSFORM;

GRANT CREATE TABLE
ON SCHEMA IPL_ANALYTICS.GOLD
TO ROLE IPL_TRANSFORM;

---------------------------------------------------------
-- Reporting Access
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.GOLD
TO ROLE IPL_REPORTING;

---------------------------------------------------------
-- Future Grants
---------------------------------------------------------

GRANT SELECT
ON FUTURE TABLES
IN SCHEMA IPL_ANALYTICS.GOLD
TO ROLE IPL_REPORTING;
