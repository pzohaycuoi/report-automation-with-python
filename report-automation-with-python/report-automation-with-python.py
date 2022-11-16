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
    enroll_list = pandas.read_sql(query, conn)
    return enroll_list


def usage_query(server, db, username, password, table, driver, enroll_number, year, month):
    """
    Create connection to Azure SQL database and run query
    """
    conn = pyodbc.connect(
        "DRIVER=" + driver + ";SERVER=tcp:" + server + ";PORT=1433;DATABASE=" + db + ";UID=" + username + ";PWD="
        + password)
    query = "SELECT TOP 200 Year, Month, EnrollmentNumber, ServiceName, ServiceTier, Cost" \
            f" FROM {table}" \
            f" WHERE EnrollmentNumber = {enroll_number} AND year = {year} AND month = {month}"
    usage_result = pandas.read_sql(query, conn)
    return usage_result


def write_file(pandas_query, file_name):
    """
    Get data from pandas query and output to file
    """
    writer = pandas.ExcelWriter(f"./{file_name}.xlsx", engine="xlsxwriter")
    pandas_query.to_excel(writer, sheet_name="sheet1", index=False, startrow=4, header=False)
    workbook = writer.book
    worksheet = writer.sheets["sheet1"]
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})
    for col_num, value in enumerate(pandas_query.columns.values):
        worksheet.write(4, col_num, value, header_format)
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
    usage_tbl = usage_query(serv_conf.get("server"), serv_conf.get("database"), serv_conf.get("username"),
                            serv_conf.get("password"), serv_conf.get("table"), serv_conf.get("driver"),
                            args.EnrollmentNumber, args.Year, args.Month)
    print(usage_tbl)
    write_file(usage_tbl, "cac")
    enroll_list = get_enroll_list(serv_conf.get("server"), serv_conf.get("database"), serv_conf.get("username"),
                                  serv_conf.get("password"), serv_conf.get("table"), serv_conf.get("driver"),
                                  args.Year, args.Month)
    print(enroll_list)


main()
