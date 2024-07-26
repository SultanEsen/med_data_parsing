class Queries:
    VACUUM = "VACUUM"

    SELECT_RUSSIA_MNN = """
        SELECT mnn, trade_mark_name, producer, medicine_info AS package,    
        limit_price FROM russia_data WHERE mnn ILIKE $1 AND medicine_info ILIKE $2
    """

    SELECT_RUSSIA_MNN_TRADEMARK = """
        SELECT mnn, trade_mark_name, producer,
        medicine_form AS package, limit_price FROM russia_data WHERE mnn ILIKE $1 AND trade_mark_name ILIKE $2
        AND medicine_info ILIKE $3
    """

    SELECT_UZBEKISTAN_MNN_TRADEMARK = """
        SELECT * FROM uzbekistan_data WHERE mnn ILIKE $1 AND trade_mark_name ILIKE $2
    """

    SELECT_UZBEKISTAN_MNN = """
        SELECT * FROM uzbekistan_data WHERE mnn ILIKE $1
    """

    SELECT_KAZAKHSTAN_MNN = """
        SELECT trade_mark_name, mnn, 
        dosage_form AS package, producer, limit_price
        FROM kazakhstan_data 
        WHERE mnn ILIKE $1 AND dosage_form ILIKE $2    
    """

    SELECT_KAZAKHSTAN_MNN_TRADEMARK = """
        SELECT trade_mark_name, mnn, 
        dosage_form AS package, producer, limit_price
        FROM kazakhstan_data 
        WHERE mnn ILIKE $1 AND trade_mark_name ILIKE $2
        AND dosage_form ILIKE $3
    """

