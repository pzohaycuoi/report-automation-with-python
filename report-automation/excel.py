import pandas
import xlsxwriter
import openpyxl


def data_to_excel(excel_file_path, excel_sheet):
    """
    Export data from sql to excel sheet
    """
    wb = xlsxwriter.Workbook(excel_file_path)
    wb.add_worksheet('cac')
    wb.close()


def read_excel(excel_file_path)


a = data_to_excel('../Book1.xlsx', 'raw_ri')
print('cac')
