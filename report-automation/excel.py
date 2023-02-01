import openpyxl
import os


def write_excel(template_file_path, destination_file_path, data):
    """
    Insert data from database to excel file with excel template
    """
    def _load_workbook(template_file_path):
        """
        Load excel workbook in local host
        """
        if not os.path.exists(template_file_path):
            raise ValueError(f'{template_file_path} not exist')
        wb = openpyxl.load_workbook(filename=template_file_path)
        return wb
    
    def _load_worksheet(workbook, worksheet):
        """
        Active the worksheet of the workbook
        """
        workbook.active = workbook[worksheet]
        ws = workbook.active
        return ws
    
    def _cleanup_worksheet(worksheet):
        """
        Clean up the worksheet - preparation for inserting data into worksheet
        """
        header_row = 1
        max_row = worksheet.max_row()
        worksheet.delete_rows(header_row+1, max_row)
        
    def _insert_data(worksheet, data):
        """
        Insert rows of data into worksheet
        """
        start_row = 2
        worksheet.insert_rows(start_row)
        


# TEST #
a = read_excel('C:/Users/namng/OneDrive/Code/Python/report-automation-with-python/Book1.xlsx', 'raw_ri')
print(a)
