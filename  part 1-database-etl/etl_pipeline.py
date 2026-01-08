import pandas as pd
import re
from sqlalchemy import create_engine
from io import StringIO

# Database Configuration
DB_TYPE = 'mysql'  # or 'postgresql'
DB_USER = 'root'
DB_PASS = 'password'
DB_HOST = 'localhost'
DB_NAME = 'fleximart'

def get_db_engine():
    connection_string = f"{DB_TYPE}+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    return create_engine(connection_string)

def clean_phone(phone):
    if pd.isna(phone): return None
    # Extract digits only
    digits = re.sub(r'\D', '', str(phone))
    # Standardize to +91-XXXXXXXXXX
    if len(digits) == 10:
        return f"+91-{digits}"
    elif len(digits) == 11 and digits.startswith('0'):
        return f"+91-{digits[1:]}"
    elif len(digits) == 12 and digits.startswith('91'):
        return f"+91-{digits[2:]}"
    return phone

def clean_date(date_str):
    if pd.isna(date_str) or date_str == '': return None
    try:
        # Handles various formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY
        return pd.to_datetime(date_str, dayfirst=True, errors='coerce').strftime('%Y-%m-%d')
    except:
        return None

def run_etl():
    report = {}
    
    # --- 1. EXTRACT ---
    # In a real scenario, use pd.read_csv('customers_raw.csv')
    # For this demo, we use the provided text data
    cust_df = pd.read_csv('customers_raw.csv')
    prod_df = pd.read_csv('products_raw.csv')
    sales_df = pd.read_csv('sales_raw.csv')

    # --- 2. TRANSFORM ---
    
    # A. Customers
    report['cust_raw'] = len(cust_df)
    cust_df.drop_duplicates(subset=['first_name', 'last_name', 'email'], inplace=True)
    report['cust_dup_removed'] = report['cust_raw'] - len(cust_df)
    
    cust_df['email'] = cust_df['email'].fillna('unknown@fleximart.com')
    cust_df['phone'] = cust_df['phone'].apply(clean_phone)
    cust_df['registration_date'] = cust_df['registration_date'].apply(clean_date)
    report['cust_missing_handled'] = cust_df.isnull().sum().sum()
    
    # B. Products
    report['prod_raw'] = len(prod_df)
    prod_df.drop_duplicates(inplace=True)
    report['prod_dup_removed'] = report['prod_raw'] - len(prod_df)
    
    prod_df['category'] = prod_df['category'].str.capitalize()
    prod_df['price'] = pd.to_numeric(prod_df['price'], errors='coerce').fillna(0.0)
    prod_df['stock_quantity'] = pd.to_numeric(prod_df['stock_quantity'], errors='coerce').fillna(0).astype(int)
    report['prod_missing_handled'] = (prod_df['price'] == 0).sum() + (prod_df['stock_quantity'] == 0).sum()

    # C. Sales (Orders & Order Items)
    report['sales_raw'] = len(sales_df)
    sales_df.drop_duplicates(subset=['transaction_id'], inplace=True)
    report['sales_dup_removed'] = report['sales_raw'] - len(sales_df)
    
    # Drop records missing critical IDs
    sales_df = sales_df.dropna(subset=['customer_id', 'product_id'])
    sales_df['transaction_date'] = sales_df['transaction_date'].apply(clean_date)
    report['sales_missing_handled'] = report['sales_raw'] - len(sales_df)

    # --- 3. LOAD ---
    try:
        engine = get_db_engine()
        
        # Load Customers
        cust_load = cust_df[['first_name', 'last_name', 'email', 'phone', 'city', 'registration_date']]
        cust_load.to_sql('customers', engine, if_exists='append', index=False)
        
        # Load Products
        prod_load = prod_df[['product_name', 'category', 'price', 'stock_quantity']]
        prod_load.to_sql('products', engine, if_exists='append', index=False)
        
        # Load Orders (Mapping to the provided Schema)
        # Note: In a real system, we would map the auto-incremented IDs. 
        # Here we map the transaction data to the 'orders' and 'order_items' tables.
        orders_df = sales_df[['customer_id', 'transaction_date', 'unit_price', 'status']].copy()
        orders_df.columns = ['customer_id', 'order_date', 'total_amount', 'status']
        # Convert alphanumeric C001 to integer 1 for the schema
        orders_df['customer_id'] = orders_df['customer_id'].str.extract('(\d+)').astype(int)
        orders_df.to_sql('orders', engine, if_exists='append', index=False)
        
        report['status'] = "Success"
    except Exception as e:
        report['status'] = f"Failed: {str(e)}"

    # Write Quality Report
    with open('data_quality_report.txt', 'w') as f:
        f.write("ETL DATA QUALITY REPORT\n")
        f.write("========================\n")
        f.write(f"Customers: Processed {report['cust_raw']}, Duplicates Removed {report['cust_dup_removed']}, Missing Handled {report['cust_missing_handled']}\n")
        f.write(f"Products: Processed {report['prod_raw']}, Duplicates Removed {report['prod_dup_removed']}, Missing Handled {report['prod_missing_handled']}\n")
        f.write(f"Sales: Processed {report['sales_raw']}, Duplicates Removed {report['sales_dup_removed']}, Dropped (Missing IDs) {report['sales_missing_handled']}\n")
        f.write(f"Database Load Status: {report['status']}\n")

if __name__ == "__main__":
    run_etl()