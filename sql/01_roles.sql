/***************************************************************************************************
Script Name    : 01_roles.sql

Project        : IPL Analytics Platform
Author         : Amit

Purpose
-------
This script creates the Role-Based Access Control (RBAC) framework for the IPL Analytics
project.

Why RBAC?
---------
Role-Based Access Control (RBAC) is a security model used by Snowflake to control access
to databases, schemas, tables, warehouses, stages, streams, tasks, and applications.

RBAC helps us:

1. Follow the Principle of Least Privilege.
2. Improve security by restricting unnecessary access.
3. Separate responsibilities across teams.
4. Simplify permission management.
5. Meet enterprise governance requirements.

Business Requirement
--------------------
The IPL Analytics Platform will have multiple personas:

1. Data Ingestion Team
   - Loads IPL CSV files into Bronze layer.
   - Requires write access only to ingestion objects.

2. Data Engineering Team
   - Builds transformations from Bronze → Silver → Gold.
   - Requires access to transformation objects.

3. Reporting Team
   - Consumes Gold layer data.
   - Requires read-only access.

4. Platform Administrator
   - Manages all project resources.

Role Design
-----------

IPL_ADMIN
----------
Project administrator role.

Responsibilities:
- Manage project objects.
- Manage grants.
- Oversee ingestion, transformation, and reporting.

IPL_INGEST
-----------
Responsible for:
- Loading source datasets.
- Managing stages.
- Maintaining Bronze layer.

IPL_TRANSFORM
--------------
Responsible for:
- Data cleansing.
- Data standardization.
- Creating dimensions and fact tables.
- Building Gold layer aggregates.

IPL_REPORTING
--------------
Responsible for:
- Dashboard consumption.
- Read-only access to curated datasets.
- Streamlit reporting layer.

Role Hierarchy
--------------

SYSADMIN
    |
IPL_ADMIN
├── IPL_INGEST
├── IPL_TRANSFORM
└── IPL_REPORTING

Benefits of Hierarchy
---------------------
- Centralized administration.
- Easier privilege inheritance.
- Reduced maintenance effort.

Objects Created
---------------
Roles:
- IPL_ADMIN
- IPL_INGEST
- IPL_TRANSFORM
- IPL_REPORTING

Prerequisites
-------------
- User must have SECURITYADMIN privileges.

***************************************************************************************************/

-- Switch to security administration role
USE ROLE SECURITYADMIN;

-- Create project roles
CREATE ROLE IF NOT EXISTS IPL_ADMIN;
CREATE ROLE IF NOT EXISTS IPL_INGEST;
CREATE ROLE IF NOT EXISTS IPL_TRANSFORM;
CREATE ROLE IF NOT EXISTS IPL_REPORTING;

-- Establish hierarchy
GRANT ROLE IPL_INGEST TO ROLE IPL_ADMIN;
GRANT ROLE IPL_TRANSFORM TO ROLE IPL_ADMIN;
GRANT ROLE IPL_REPORTING TO ROLE IPL_ADMIN;

-- Allow SYSADMIN to inherit project administration capabilities
GRANT ROLE IPL_ADMIN TO ROLE SYSADMIN;

-- Validation
SHOW ROLES LIKE 'IPL%';
