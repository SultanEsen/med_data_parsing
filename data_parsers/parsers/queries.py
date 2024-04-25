class Queries:
    VACUUM = "PRAGMA auto_vacuum = FULL"
    CREATE_LATEST_DOCUMENTS_TABLE = """
        CREATE TABLE IF NOT EXISTS latest_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            created_at DATETIME
        )
    """
    DROP_UZBEKISTAN_DATA_TABLE = "DROP TABLE IF EXISTS uzbekistan_data"
    CREATE_UZBEKISTAN_DATA_TABLE = """
        CREATE TABLE IF NOT EXISTS uzbekistan_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER,
            trade_mark_name TEXT,
            mnn TEXT,
            producer TEXT,
            package TEXT,
            registration_number TEXT,
            currency TEXT,
            limit_price REAL,
            current_retail_price REAL,
            current_wholesale_price REAL
        )
    """
    DROP_TURKEY_DATA_TABLE = "DROP TABLE IF EXISTS turkey_data"
    CREATE_TURKEY_DATA_TABLE = """
        CREATE TABLE IF NOT EXISTS turkey_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_info TEXT,
            company_name TEXT,
            price REAL
        )
    """
