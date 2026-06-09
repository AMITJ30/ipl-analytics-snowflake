/***************************************************************************************************
Script Name    : 07_load_bronze_data.sql

Project        : IPL Analytics Platform

Purpose
-------
Load IPL source files from stage into Bronze layer.

Why COPY INTO?
--------------
COPY INTO is Snowflake's recommended bulk loading mechanism.

Benefits:
---------
- Fast
- Scalable
- Parallelized
- Supports validation

Source
------
@IPL_STAGE

Target
------
BRONZE.MATCHES_RAW
BRONZE.DELIVERIES_RAW

***************************************************************************************************/
