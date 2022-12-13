import pandas
import pyodbc
import xlsxwriter
import argparse
import azure.storage.fileshare as azfs
import os
from dotenv import load_dotenv
from xlsxwriter.utility import xl_rowcol_to_cell


def db_conn(serv, db, usr, pwd, driver):
    """
    Establish connection to the database
    """
    odbc_conn = pyodbc.connect(
        f"DRIVER={driver};SERVER=tcp:{serv};PORT=1433;DATABASE={db};UID={usr};PWD={pwd}")
    cursor = odbc_conn.cursor()
    return odbc_conn, cursor


def get_enroll_list(cursor, table, year, month):
    """
    Query list of enrollment number and out put to file
    """
    cursor.execute(
        f"SELECT DISTINCT TOP 200 EnrollmentNumber FROM {table}  WHERE year = {year} AND month = {month}")
    return cursor.fetchall()


def usage_query(odbc_conn, table, enroll_num, year, month):
    """
    Create connection to Azure SQL database and run query
    """
    query = "SELECT TOP 200 Year, Month, EnrollmentNumber, ServiceName, ServiceTier, Cost" \
            f" FROM {table} WHERE EnrollmentNumber = {enroll_num} AND year = {year} AND month = {month}"
    usage_result = pandas.read_sql(query, odbc_conn)
    return usage_result


def write_file(pandas_query, file_name):
    """
    Get data from pandas query and output to file
    """
    def find_lastrow(count_row, start_row, column):
        toal_row = count_row + start_row
        start_range = xl_rowcol_to_cell(start_row, column)
        end_range = xl_rowcol_to_cell(toal_row, column)
        return start_range, end_range
    
    start_row = 4
    cost_row = 5
    cost_col = 5
    number_rows = len(pandas_query.index)
    first_row, last_row = find_lastrow(number_rows, start_row, cost_row)
    print(first_row)
    print(last_row)
    
    writer = pandas.ExcelWriter(f"./{file_name}.xlsx", engine="xlsxwriter")
    pandas_query.to_excel(writer, sheet_name="usage",
                          index=False, startrow=start_row, header=False)
    workbook = writer.book
    worksheet = writer.sheets["usage"]
    
    # set header format
    header_fmt = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'middle',
        'fg_color': '#D7E4BC',
        'border': 1})
    # format table header
    for col_num, value in enumerate(pandas_query.columns.values):
        worksheet.write(first_row, col_num, value, header_fmt)
        
    # add format for cost
    cost_fmt = workbook.add_format(
        {'num_format': '_($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_)'})
    worksheet.set_column("F:F", 12, cost_fmt)

    # total format
    total_fmt = workbook.add_format(
        {'align': 'right', 'num_format': '$#,##0', 'bold': True, 'bottom': 6})
    # Add total row
    formula = "=SUM({:s}:{:s})".format(first_row, last_row)
    sum_cell = xl_rowcol_to_cell(first_row-1, cost_col)
    total_text_cell = xl_rowcol_to_cell(first_row-1, cost_col-1)
    worksheet.write_formula(sum_cell, formula, total_fmt)
    worksheet.write_string(total_text_cell, "Total",total_fmt)
    
    # format date column
    worksheet.set_column("A:B", 10)
    
    # format product info column
    worksheet.set_column("C:F", 20)
    writer.save()


# Define options
parser = argparse.ArgumentParser()
parser.add_argument('-e', "--EnrollmentNumber",
                    help="Input Azure enrollment number", required=True)
parser.add_argument(
    '-y', "--Year", help="year of the report", required=True)
parser.add_argument(
    '-m', "--Month", help="month of the report", required=True)
args = parser.parse_args()

# load .env
load_dotenv()
DB_ADDR = os.getenv("DB_ADDR")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_USER_PWD = os.getenv("DB_USER_PWD")
DB_TBL = os.getenv("DB_TBL")
DB_DRIVER = os.getenv("DB_DRIVER")

conn, cur = db_conn(DB_ADDR, DB_NAME, DB_USER, DB_USER_PWD, DB_DRIVER)
usage_tbl = usage_query(
    conn, DB_TBL, args.EnrollmentNumber, args.Year, args.Month)
print(usage_tbl)
write_file(usage_tbl, "cac")
enroll_list = get_enroll_list(cur, DB_TBL, args.Year, args.Month)
print(enroll_list)
