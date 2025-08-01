# backend/query_executor.py
import duckdb
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def run_sql_query(sql: str) -> pd.DataFrame:
    con = duckdb.connect(database=":memory:")  # use in-memory DB for speed

    # Register all four CSVs as views
    for csv_path in DATA_DIR.glob("*.csv"):
        view_name = csv_path.stem  # e.g., claims.csv → claims
        con.execute(f"""
            CREATE OR REPLACE VIEW {view_name} AS
            SELECT * FROM '{csv_path.as_posix()}'
        """)

    try:
        return con.execute(sql).fetchdf()
    finally:
        con.close()
