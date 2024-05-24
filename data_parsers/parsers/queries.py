class Queries:
    VACUUM = "VACUUM"
    CREATE_LATEST_DOCUMENTS_TABLE = """
        CREATE TABLE IF NOT EXISTS latest_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            country TEXT,
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
    DROP_KAZAKHSTAN_DATA_TABLE = "DROP TABLE IF EXISTS kazakhstan_data"
    CREATE_KAZAKHSTAN_DATA_TABLE = """
        CREATE TABLE IF NOT EXISTS kazakhstan_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_mark_name TEXT,
            mnn TEXT,
            dosage_form TEXT,
            producer TEXT,
            registration_number TEXT,
            limit_price REAL
        )
    """
    DROP_RUSSIA_DATA_TABLE = "DROP TABLE IF EXISTS russia_data"
    CREATE_RUSSIA_DATA_TABLE = """
        CREATE TABLE IF NOT EXISTS russia_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mnn TEXT,
            trade_mark_name TEXT,
            medicine_info TEXT,
            producer TEXT,
            ath_code TEXT,
            amount INTEGER,
            limit_price REAL
        )
    """
    DROP_MOLDAVIA_DATA_TABLE = "DROP TABLE IF EXISTS moldova_data"
    CREATE_MOLDAVIA_DATA_TABLE = """
        CREATE TABLE IF NOT EXISTS moldova_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_mark_name TEXT,
            medical_form TEXT,
            dosage_form TEXT,
            volume TEXT,
            producer_country TEXT,
            producer TEXT,
            ath_code TEXT,
            mnn TEXT,
            price REAL,
            currency TEXT
        )
    """
