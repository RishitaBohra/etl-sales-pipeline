import pandas as pd
import logging
from sqlalchemy import create_engine

# =========================
# LOGGING SETUP
# =========================

logging.basicConfig(
    filename='logs/etl_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 50)
print("ETL PIPELINE STARTED")
print("=" * 50)

logging.info("ETL Pipeline Started")

try:

    # =========================
    # EXTRACT
    # =========================

    print("\n[1] Extracting Data...")

    df = pd.read_csv("data/sales_data.csv")

    print("\nOriginal Dataset:")
    print(df)

    logging.info("Data extracted successfully")

    # =========================
    # TRANSFORM
    # =========================

    print("\n[2] Transforming Data...")

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove missing values
    df = df.dropna()

    # Create TotalSales column
    df["TotalSales"] = df["Price"] * df["Quantity"]

    print("\nTransformed Dataset:")
    print(df)

    logging.info("Data transformed successfully")

    # Generate sales summary
    summary = df.groupby("Region")["TotalSales"].sum().reset_index()

    print("\nSales Summary By Region:")
    print(summary)

    # Save summary CSV
    summary.to_csv("output/sales_summary.csv", index=False)

    logging.info("Summary report generated")

    # =========================
    # LOAD TO MYSQL
    # =========================

    print("\n[3] Loading Data into MySQL...")

    username = "root"
    password = "ganeshji:)123"
    host = "localhost"
    database = "salesdb"

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@{host}/{database}"
    )

    # Load table into MySQL
    df.to_sql(
        name="sales_data",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("\nData loaded into MySQL successfully!")

    logging.info("Data loaded into MySQL successfully")

    print("\nETL PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 50)

    logging.info("ETL Pipeline Completed")

except Exception as e:

    print("\nError occurred:")
    print(e)

    logging.error(f"Error occurred: {e}")