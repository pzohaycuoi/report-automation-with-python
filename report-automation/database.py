import logging
import pyodbc
import common


common.logger_config()


def connection(conn_str):
    """
    Establish connection to the database
    """
    try:
        logging.debug(f"Establishing database connection: {conn_str}")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        logging.debug(f"Completed Establishing database connection: {conn_str}")
        return conn, cursor

    # TODO error handling
    except pyodbc.Error as err:
        logging.critical(f"{err.args[0]}: {err.args[1]}")
        raise SystemError(err)


def exec_stored_procedure(cursor: pyodbc.Cursor, stored_procedure, *args):
    """
    Execute SQL stored procedures
    """
    try:
        query = f"exec {stored_procedure} {args[0]},{args[1]},{args[2]}"
        logging.debug(f"Executing stored procedure: {query}")
        cursor.execute(f"exec {stored_procedure} {args[0]},{args[1]},{args[2]}")
        logging.debug(f"Completed Executing stored procedure: {stored_procedure}")
        logging.debug(f"Fetching data")
        data = cursor.fetchall()
        if data == '' or data is None or data == []:
            logging.warning('This enrollment does not have data in database')
        else:
            logging.debug(f"Completed fetching data")

        return cursor, data

    except pyodbc.Error as err:
        logging.critical(f"{err.args[0]}: {err.args[1]}")
        raise SystemError(err)
