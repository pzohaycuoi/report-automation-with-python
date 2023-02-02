import openpyxl
import os
import common


@common.log_function_call
def load_excel(template_file_path):
    """
    Load excel workbook in local host
    """
    default_template_path = 'C:/Users/namng/OneDrive/Code/Python/report-automation-with-python/template/Book1.xlsx'
    if not os.path.exists(template_file_path):
        if os.path.exists(default_template_path):
            wb = openpyxl.load_workbook(default_template_path)
        else:
            raise ValueError(f'{template_file_path} not exist')
    wb = openpyxl.load_workbook(filename=template_file_path)
    return wb


@common.log_function_call
def save_workbook(workbook, destination_file_path):
    """
    Save the workbook to new destination
    """
    workbook.save(destination_file_path)


@common.log_function_call
def write_excel(workbook, template_file_path, data, worksheet):
    """
    Insert data from database to excel file with excel template
    """
    @common.log_function_call
    def _load_worksheet(workbook, worksheet):
        """
        Active the worksheet of the workbook
        """
        ws = workbook[worksheet]
        return ws

    @common.log_function_call
    def _cleanup_worksheet(worksheet):
        """
        Clean up the worksheet - preparation for inserting data into worksheet
        """
        start_row = 2
        max_row = worksheet.max_row
        worksheet.delete_rows(start_row, max_row)

    @common.log_function_call
    def _insert_data(worksheet, data):
        """
        Insert rows of data into worksheet
        """
        start_row = 2
        for i, row_data in enumerate(data, start=start_row):
            for j, value in enumerate(row_data):
                worksheet.cell(row=i, column=j+1, value=value)
                
    @common.log_function_call
    def _refresh_pivot_table(worksheet): # TODO: FIX THIS The raw data worksheet does not pivot table
        """
        Refresh the pivot tables in a worksheet
        """
        for pivot_table in worksheet.pivot_tables:
            pivot_table.refresh()
            
    @common.log_function_call
    def _refresh_multi_pivot_table(workbook):  # TODO: FIX THIS The raw data worksheet does not pivot table
        """
        Refresh pivot tables in workbook
        """
        for ws in workbook.worksheets:
            _refresh_pivot_table(ws)
        
    ws = _load_worksheet(workbook, worksheet)
    _cleanup_worksheet(ws)
    _insert_data(ws, data)
    # _refresh_pivot_table(ws)
    
    
# if __name__ == '__main__':
    
