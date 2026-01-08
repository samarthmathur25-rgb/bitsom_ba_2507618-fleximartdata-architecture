Student Name: Samarth Mathur

Student ID: bitsom_ba_2507618

Email: samarthmathur25@gmail.com

Date: January 6, 2026

Project Overview
This project involves the design and implementation of a robust data ecosystem for FlexiMart, an omni-channel retail platform. I built a multi-layered architecture featuring a relational ETL pipeline for transactional data, a NoSQL document store for flexible product cataloging, and a centralized Star Schema Data Warehouse to support complex business intelligence and analytical reporting.

Repository Structure
Plaintext
├── part1-database-etl/
│   ├── etl_pipeline.py         # Python script for data extraction and transformation
│   ├── schema_documentation.md # Detailed breakdown of the relational model
│   ├── business_queries.sql    # SQL scripts for operational insights
│   └── data_quality_report.txt # Validation results of the processed data
├── part2-nosql/
│   ├── nosql_analysis.md      # Comparison of SQL vs NoSQL for retail use cases
│   ├── mongodb_operations.js   # CRUD operations and aggregation pipelines
│   └── products_catalog.json   # Sample semi-structured product data
├── part3-datawarehouse/
│   ├── star_schema_design.md   # Documentation of Facts and Dimensions
│   ├── warehouse_schema.sql    # DDL for the Data Warehouse tables
│   ├── warehouse_data.sql      # Seed data for the analytical environment
│   └── analytics_queries.sql   # Complex OLAP queries for business trends
└── README.md                   # Project documentation (this file)
Technologies Used
Languages: Python 3.10+, SQL (MySQL/PostgreSQL Dialects), JavaScript (MongoDB Shell)

Databases: MySQL 8.0 (Transactional & Warehouse), MongoDB 6.0 (Document Store)

Libraries: pandas (Data Manipulation), mysql-connector-python (Database Connectivity)

Tools: Git/GitHub, Data Modeling (ERDs)

Setup Instructions
Database Setup

To initialize the relational environments, execute the following commands in your terminal:

Bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
# Ensure you have installed dependencies: pip install pandas mysql-connector-python
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse Setup and Analysis
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql
MongoDB Setup

For the NoSQL product catalog, ensure MongoDB service is running and execute:

Bash
mongosh < part2-nosql/mongodb_operations.js
Key Learnings
Through this project, I mastered the art of transitioning data from highly normalized transactional systems to denormalized analytical formats using Star Schemas. I gained practical experience in handling data quality issues during the ETL process and learned how to leverage NoSQL's schema flexibility for diverse product attributes that don't fit well into traditional tables. Additionally, I improved my ability to write complex SQL aggregations for identifying high-value business trends.

Challenges Faced
Handling Data Type Mismatches: During the ETL process, some source CSV data contained inconsistent date formats. I resolved this by implementing a robust try-except block within the Python transformation logic to standardize all dates to ISO format before database insertion.

Mapping Hierarchical Product Data: Representing deeply nested product categories in a relational database proved difficult. I overcame this by utilizing MongoDB for the product catalog, which allowed for a natural document-based representation of varying attributes without needing a massive join table.