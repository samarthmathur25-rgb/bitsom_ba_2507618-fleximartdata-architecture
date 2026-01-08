Star Schema Design: FlexiMart Sales Analysis
Section 1: Schema Overview
FACT TABLE: fact_sales

Grain: One row per product per order line item.

Business Process: Sales transactions captured at the Point of Sale.

Measures (Numeric Facts):

quantity_sold: Number of units sold.

unit_price: Price per unit at the time of sale.

discount_amount: Total discount value applied to the line item.

total_amount: Final revenue amount calculated as (quantity_sold×unit_price)−discount_amount.

Foreign Keys:

date_key → links to dim_date.

product_key → links to dim_product.

customer_key → links to dim_customer.

DIMENSION TABLE: dim_date

Purpose: Time-based analysis (trends, seasonality).

Type: Conformed dimension.

Attributes:

date_key (PK): Surrogate key (Integer, YYYYMMDD).

full_date: Date object.

day_of_week: Monday, Tuesday, etc.

month: 1-12.

month_name: January, February, etc.

quarter: Q1, Q2, Q3, Q4.

year: 2023, 2024, etc.

is_weekend: Boolean.

DIMENSION TABLE: dim_product

Purpose: Descriptive context for items sold.

Attributes:

product_key (PK): Surrogate key.

product_id: Original SKU/Natural key.

product_name: Name of the item.

category: e.g., Electronics, Grocery.

brand: Manufacturer name.

supplier_name: Source of the product.

DIMENSION TABLE: dim_customer

Purpose: Demographic and geographic analysis.

Attributes:

customer_key (PK): Surrogate key.

customer_id: Natural key from CRM.

customer_name: Full name.

email: Contact info.

city: Resident city.

region: State or territory.

customer_segment: e.g., Corporate, Individual.

Section 2: Design Decisions
Granularity: The "transaction line-item" level was chosen to ensure maximum flexibility. By capturing data at the lowest possible level, FlexiMart can answer highly specific queries (e.g., "What is the average discount for Laptops in Mumbai?") without losing detail. Aggregated grains would prevent us from filtering by specific product attributes later.

Surrogate Keys: Surrogate keys (integers) are used instead of natural keys (like Product SKU or Email) to decouple the Data Warehouse from source system changes. They improve join performance and allow for Slowly Changing Dimensions (SCD) tracking, ensuring historical accuracy if a product changes category or a customer moves cities.

Drill-down and Roll-up: This star schema supports roll-up by allowing measures to be summed across hierarchies (e.g., from full_date to month to year). Conversely, it supports drill-down by allowing users to start at a high-level summary (Total Sales) and navigate into specific dimensions (Sales by Brand or Sales by City) due to the descriptive attributes in our dimension tables.

Section 3: Sample Data Flow
Source Transaction

Order #101, Customer: "John Doe", Product: "Laptop", Qty: 2, Price: 50,000, Date: 2024-01-15.

Data Warehouse Transformation

fact_sales: | date_key | product_key | customer_key | quantity_sold | unit_price | total_amount | | :--- | :--- | :--- | :--- | :--- | :--- | | 20240115 | 5 | 12 | 2 | 50000 | 100000 |

dim_date:

{date_key: 20240115, full_date: '2024-01-15', month: 1, month_name: 'January', quarter: 'Q1', year: 2024, is_weekend: false}

dim_product:

{product_key: 5, product_id: 'PROD-001', product_name: 'Laptop', category: 'Electronics', brand: 'TechCorp'}

dim_customer:

{customer_key: 12, customer_id: 'CUST-99', customer_name: 'John Doe', city: 'Mumbai', region: 'Maharashtra'}