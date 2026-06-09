/***************************************************************************************************
Script Name    : 04_grants.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Grant required permissions to project roles.

Why?
----
Creating roles alone does not provide access.

Roles need permissions on:
- Warehouse
- Database
- Schemas

Role Responsibilities
---------------------

IPL_INGEST
-----------
Loads raw IPL files into Bronze layer.

IPL_TRANSFORM
--------------
Transforms data from Bronze → Silver → Gold.

IPL_REPORTING
--------------
Read-only access to Gold layer for reporting
and Streamlit dashboards.

Security Principle
------------------
Least Privilege Access

Users receive only the permissions necessary
to perform their job responsibilities.

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
-- Bronze Schema Access
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.BRONZE
TO ROLE IPL_INGEST;

---------------------------------------------------------
-- Silver Schema Access
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.SILVER
TO ROLE IPL_TRANSFORM;

---------------------------------------------------------
-- Gold Schema Access
---------------------------------------------------------

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.GOLD
TO ROLE IPL_TRANSFORM;

GRANT USAGE
ON SCHEMA IPL_ANALYTICS.GOLD
TO ROLE IPL_REPORTING;
