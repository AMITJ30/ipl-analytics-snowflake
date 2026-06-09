/***************************************************************************************************
Script Name    : 03_database_setup.sql

Project        : IPL Analytics Platform
Author         : Amit

## Purpose

Creates the database and schema structure for the IPL Analytics project.

## Why are we creating multiple schemas?

We are following the Medallion Architecture pattern.

## LANDING

Stores source files before they are loaded into Snowflake tables.
Examples:

* CSV files
* JSON files
* Parquet files

## BRONZE

Stores raw data exactly as received from source systems.

## SILVER

Stores cleaned, validated, and standardized data.

## GOLD

Stores business-ready datasets used for reporting,
analytics, and dashboarding.

## UTIL

Stores utility objects such as:

* Streams
* Tasks
* Stored Procedures
* Audit Tables

## Architecture

IPL_ANALYTICS
│
├── LANDING
├── BRONZE
├── SILVER
├── GOLD
└── UTIL

## Benefits

* Better organization
* Improved governance
* Easier maintenance
* Supports scalable data pipelines
* Aligns with enterprise data architecture standards

## Prerequisites

* IPL_WH Warehouse created
* SYSADMIN role access

## Objects Created

Database:

* IPL_ANALYTICS

Schemas:

* LANDING
* BRONZE
* SILVER
* GOLD
* UTIL

***************************************************************************************************/

-- Switch to administrative role
USE ROLE SYSADMIN;

---

## -- Create Database

CREATE DATABASE IF NOT EXISTS IPL_ANALYTICS;

---

## -- Use Database

USE DATABASE IPL_ANALYTICS;

---

## -- Create Schemas

CREATE SCHEMA IF NOT EXISTS LANDING;

CREATE SCHEMA IF NOT EXISTS BRONZE;

CREATE SCHEMA IF NOT EXISTS SILVER;

CREATE SCHEMA IF NOT EXISTS GOLD;

CREATE SCHEMA IF NOT EXISTS UTIL;

---

## -- Validation

SHOW SCHEMAS;
