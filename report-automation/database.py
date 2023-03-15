import logging
import pyodbc
import common


common.logger_config()


@common.log_function_call
def connection(conn_str):
    """
    Establish connection to the database
    """
    # TODO error handling
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        return cursor
    except pyodbc.Error as err:
        logging.critical('%s: %s', err.args[0], err.args[1])
        raise err


@common.log_function_call
def exec_stored_procedure(cursor: pyodbc.Cursor, stored_procedure, *args):
    """
    Execute SQL stored procedures
    """
    try:
        query = f"exec {stored_procedure} {args[0]}"
        cursor.execute(query)
        data = cursor.fetchall()
        if data == '' or data is None or data == []:
            logging.info(
                'This enrollment %s does not have data in database', args[0])
        else:
            logging.info('This enrollment %s have data in database', args[0])
        return data
    except pyodbc.Error as err:
        logging.critical('%s: %s', err.args[0], err.args[1])
        raise err


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    db_conn_str = 'DRIVER='+getenv('DB_DRIVER')+';SERVER=tcp:' + \
        getenv('DB_ADDR')+';PORT=1433;DATABASE=' + \
        getenv('DB_NAME')+';UID='+getenv('DB_USER') + \
        ';PWD=' + getenv('DB_USER_PWD')
    db_cursor = connection(db_conn_str)
    params = "@EnrollmentNumber=50902749,@year=2022,@month=12"
    stored_procedures = 'proc_data_report_ea'
    db_data = exec_stored_procedure(db_cursor, stored_procedures, params)
    print(db_data)
