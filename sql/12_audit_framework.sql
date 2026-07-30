/***************************************************************************************************

Script Name    : 12_audit_framework.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
Create an Audit Framework to monitor ETL pipeline execution.

Why Audit Framework?
--------------------
Enterprise ETL pipelines should provide visibility into every data load.

The framework should answer:

1. Which pipeline executed?
2. Which table was loaded?
3. Which file was processed?
4. How many rows were loaded?
5. Was the execution successful?
6. If failed, what was the reason?

Objects Created
---------------
1. LOAD_AUDIT
2. ERROR_LOG
3. PIPELINE_RUN

Benefits
--------
1. ETL Monitoring
2. Data Load Auditing
3. Error Tracking
4. Operational Visibility
5. Production Ready Design

Architecture
------------

                ETL PIPELINE
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 LOAD_AUDIT                 ERROR_LOG
        │
        ▼
 PIPELINE_RUN

***************************************************************************************************/

USE ROLE SYSADMIN;

USE DATABASE IPL_ANALYTICS;

--------------------------------------------------------------------------------
-- Create UTIL Schema
--------------------------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS UTIL;

USE SCHEMA UTIL;

--------------------------------------------------------------------------------
-- Create Audit Sequence
--------------------------------------------------------------------------------

CREATE SEQUENCE IF NOT EXISTS LOAD_AUDIT_SEQ
START = 1
INCREMENT = 1;

--------------------------------------------------------------------------------
-- Create LOAD_AUDIT Table
--------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS LOAD_AUDIT
(
    AUDIT_ID           NUMBER
                       DEFAULT LOAD_AUDIT_SEQ.NEXTVAL,

    PIPELINE_NAME      VARCHAR(100),

    TABLE_NAME         VARCHAR(100),

    FILE_NAME          VARCHAR(255),

    BATCH_ID           VARCHAR(50),

    LOAD_START_TIME    TIMESTAMP_NTZ,

    LOAD_END_TIME      TIMESTAMP_NTZ,

    ROWS_LOADED        NUMBER,

    LOAD_STATUS        VARCHAR(20),

    ERROR_MESSAGE      VARCHAR(1000),

    CREATED_BY         VARCHAR(100)
                       DEFAULT CURRENT_USER(),

    CREATED_TS         TIMESTAMP_NTZ
                       DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Create ERROR_LOG Table
--------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS ERROR_LOG
(
    ERROR_ID           NUMBER AUTOINCREMENT,

    PIPELINE_NAME      VARCHAR(100),

    OBJECT_NAME        VARCHAR(100),

    ERROR_MESSAGE      VARCHAR(2000),

    ERROR_TIMESTAMP    TIMESTAMP_NTZ
                       DEFAULT CURRENT_TIMESTAMP(),

    CREATED_BY         VARCHAR(100)
                       DEFAULT CURRENT_USER()
);

--------------------------------------------------------------------------------
-- Create PIPELINE_RUN Table
--------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS PIPELINE_RUN
(
    RUN_ID             NUMBER AUTOINCREMENT,

    PIPELINE_NAME      VARCHAR(100),

    BATCH_ID           VARCHAR(50),

    START_TIME         TIMESTAMP_NTZ,

    END_TIME           TIMESTAMP_NTZ,

    RUN_STATUS         VARCHAR(20),

    CREATED_BY         VARCHAR(100)
                       DEFAULT CURRENT_USER(),

    CREATED_TS         TIMESTAMP_NTZ
                       DEFAULT CURRENT_TIMESTAMP()
);

--------------------------------------------------------------------------------
-- Validation Queries
--------------------------------------------------------------------------------

SHOW TABLES IN SCHEMA UTIL;

--------------------------------------------------------------------------------
-- Verify LOAD_AUDIT
--------------------------------------------------------------------------------

SELECT *

FROM UTIL.LOAD_AUDIT;

--------------------------------------------------------------------------------
-- Verify ERROR_LOG
--------------------------------------------------------------------------------

SELECT *

FROM UTIL.ERROR_LOG;

--------------------------------------------------------------------------------
-- Verify PIPELINE_RUN
--------------------------------------------------------------------------------

SELECT *

FROM UTIL.PIPELINE_RUN;

--------------------------------------------------------------------------------
-- Object Count
--------------------------------------------------------------------------------

SELECT
    COUNT(*) AS TOTAL_TABLES
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'UTIL'
AND TABLE_NAME IN
(
    'LOAD_AUDIT',
    'ERROR_LOG',
    'PIPELINE_RUN'
);

--------------------------------------------------------------------------------
-- Expected Outcome
--------------------------------------------------------------------------------

-- UTIL Schema Available
-- LOAD_AUDIT Created
-- ERROR_LOG Created
-- PIPELINE_RUN Created
-- Audit Framework Ready
-- Ready for Stored Procedure Development

--------------------------------------------------------------------------------
