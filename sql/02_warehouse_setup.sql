/********************************************************************
 Script Name : 02_warehouse_setup.sql

 Purpose:
 --------
 This script creates the compute warehouse used by the IPL Analytics
 project.

 Why do we need a Warehouse?
 ---------------------------
 In Snowflake, storage and compute are separated.

 Database/Tables  -> Store data
 Warehouse        -> Executes queries and transformations

 We are creating a dedicated warehouse for:
 - Data ingestion
 - Data transformation
 - Streamlit dashboards

 Notes:
 ------
 - XSMALL is sufficient for development.
 - AUTO_SUSPEND helps reduce costs.
 - AUTO_RESUME starts the warehouse automatically when needed.

 Author : Amit
 Project: IPL Analytics Platform
********************************************************************/

USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS IPL_WH
WITH
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE;

-- Verify warehouse creation
SHOW WAREHOUSES LIKE 'IPL_WH';
