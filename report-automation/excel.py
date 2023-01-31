import openpyxl


def write_excel(template_file_path, destination_file_path):
    """
    Insert data from database to excel file with excel template
    """
    def _read_workbook(template_file_path)
    """
    Read excel workbook in local host
    """
    wb = openpyxl.load_workbook(filename=template_file_path)
    
    wb.active = wb[worksheet]
    ws = wb.active
    max_row = ws.max_row()
    return max_row


# TEST #
a = read_excel('C:/Users/namng/OneDrive/Code/Python/report-automation-with-python/Book1.xlsx', 'raw_ri')
print(a)
