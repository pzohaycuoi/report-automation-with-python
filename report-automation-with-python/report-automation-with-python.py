import pandas
import pyodbc
import xlsxwriter
import yaml
import argparse


def load_config(config):
    """
    Load connection info needed for db_query function
    """
    with open(config) as conf:
        data = yaml.load(conf, Loader=yaml.SafeLoader)
    return data


def get_enroll_list(server, db, username, password, table, driver, year, month):
    """
    Query list of enrollment number and out put to file
    """
    conn = pyodbc.connect(
        "DRIVER=" + driver + ";SERVER=tcp:" + server + ";PORT=1433;DATABASE=" + db + ";UID=" + username + ";PWD="
        + password)
    query = "SELECT DISTINCT TOP 200 EnrollmentNumber" \
            f" FROM {table}" \
            f" WHERE year = {year} AND month = {month}"
    cursor = conn.cursor()
    cursor.execute(query)
    for i in cursor:
        print(i)


def db_query(server, db, username, password, table, driver, enroll_number, year, month):
    """
    Create connection to Azure SQL database and run query
    """
    conn = pyodbc.connect(
        "DRIVER=" + driver + ";SERVER=tcp:" + server + ";PORT=1433;DATABASE=" + db + ";UID=" + username + ";PWD="
        + password)
    query = "SELECT TOP 200 Year, Month, EnrollmentNumber, ServiceName, ServiceTier, Cost" \
            f" FROM {table}" \
            f" WHERE EnrollmentNumber = {enroll_number} AND year = {year} AND month = {month}"
    query_result = pandas.read_sql(query, conn)
    return query_result


def write_file(pandas_query, file_name):
    """
    Get data from pandas query and output to file
    """
    writer = pandas.ExcelWriter(f"./{file_name}.xlsx", engine="xlsxwriter", mode="append")
    pandas_query.to_excel(writer, sheet_name="sheet1", index=False)
    writer.save()


def main():
    #
    # Define options
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', "--EnrollmentNumber", help="Input Azure enrollment number", required=True)
    parser.add_argument('-y', "--Year", help="year of the report", required=True)
    parser.add_argument('-m', "--Month", help="month of the report", required=True)
    args = parser.parse_args()
    serv_conf = load_config('config/config.yaml')
    query_tbl = db_query(serv_conf.get("server"), serv_conf.get("database"), serv_conf.get("username"),
                         serv_conf.get("password"), serv_conf.get("table"), serv_conf.get("driver"),
                         args.EnrollmentNumber, args.Year, args.Month)
    print(query_tbl)
    write_file(query_tbl, "cac")
    get_enroll_list(serv_conf.get("server"), serv_conf.get("database"), serv_conf.get("username"),
                    serv_conf.get("password"), serv_conf.get("table"), serv_conf.get("driver"),
                    args.Year, args.Month)


main()
