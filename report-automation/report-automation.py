import common
import logging
from dotenv import load_dotenv
import database
import apicostmgmt
import os
from datetime import date
import excel
import azurefileshare
from azure.storage.fileshare import ShareDirectoryClient


# Setup logging
common.logger_config()


class ReportAutomation:
    def __init__(self):
        self.enroll_list = []
        self.report_month = 12
        self.report_year = 2022
        self.enrollment_active_staus = ('Active', 'Extended')
        self.enrollment_disable_status = ('Deleted', 'Disabled', 'Expired',
                                          'Transferred', 'Terminated',
                                          'ManuallyTerminated')
        self.report_template_path = ''
        self.local_report_path = ''
        self.cloud_report_path = ''
        self.azure_fileshare_client = ShareDirectoryClient

    @common.log_function_call
    def _get_enrollment_list(self):
        """
        Get Azure Enterprise Agreement enrollment number list
        """
        data = apicostmgmt.get_enroll_list(os.getenv('API_KEY'))
        self.enroll_list = data['value']
        return data

    @common.log_function_call
    def _get_previous_month(self):
        """
        Get previous month includes month and year
        """
        today = date.today()
        year = int(today.strftime("%Y"))
        month = int(today.strftime("%m"))
        if month == 1:
            year = year - 1
            month = 12
        else:
            month = month - 1
        self.report_year = year
        self.report_month = month
        return {'report_year': year,
                'report_month': month}


    @common.log_function_call
    def _db_connect(self):
        """
        Connect to database
        Must run after _load_env method
        """
        cursor = database.connection('DRIVER='+os.getenv('DB_DRIVER')+';SERVER=tcp:'+os.getenv('DB_ADDR')+';PORT=1433;DATABASE='+os.getenv('DB_NAME')+';UID='+os.getenv('DB_USER')+';PWD='+ os.getenv('DB_USER_PWD'))
        return cursor

    @common.log_function_call
    def _exec_stored_procedures(self, cursor, stored_procedure,
                                enrollment_number):
        """
        Exectute SQL stored procedure to get the data
        Must execute after _get_previous_month
        """
        if enrollment_number is None or enrollment_number == '':
            logging.error('Enrollment Number is not provided')
            return False
        if self.report_month == 0 or self.report_year == 0:
            logging.warning('report month and year is not provided, setting')
            ReportAutomation._get_previous_month(self)
        params = f"@EnrollmentNumber={enrollment_number},@year={self.report_year},@month={self.report_month}"
        data = database.exec_stored_procedure(cursor, stored_procedure, params)
        return data
        
    @common.log_function_call
    def _create_fileshare_client(self):
        """
        Establish Azure file share directory client
        """
        file_client = azurefileshare.fileshare_client(os.getenv('SA_CONN_STR'),
                                                      os.getenv('FS_NAME'),
                                                      dir='./',
                                                      mode='dir')
        self.azure_fileshare_client = file_client
        return file_client
        
    @common.log_function_call
    def _download_template(self):
        """
        Download report template inside Azure Fileshare
        """
        # TODO: implement this
        
    
    @common.log_function_call
    def _upload_report(self, dir_client, report_type, customer_name, enrollment_number):
        """
        Upload report from source folder to Azure file share with dir pattern
        """
        cloud_dir_path = f"./{report_type}/{customer_name}/{enrollment_number}/{self.report_year}/{self.report_month}/"
        azurefileshare.upload_file(dir_client, cloud_dir_path, self.local_report_path)
        self.cloud_report_path = cloud_dir_path

    @common.log_function_call
    def get_usage_enroll(self, template_file, db_cursor, enrollment_number):
        """
        Query the usage data of an Enrollment
        """
        sp_list = ('proc_data_report_ea': 'raw_usage',
                   'proc_data_ri_report_ea': 'raw_ri',
                   'proc_data_balance_summary_report_ea': 'BalanceSummary',
                   'proc_data_marketplace_report_ea': 'raw_marketplace')
        tbl_list = ('raw_usage': 'raw_usage',
                    'raw_ri': 'raw_ri',
                    'BalanceSummary': 'BalanceSummary',
                    'raw_marketplace': 'raw_marketplace')
        wb = excel.load_excel(template_file)
        data_dict = {}
        for sp in sp_list:
            data = ReportAutomation()._exec_stored_procedures(db_cursor, sp,
                                                              enrollment_number)
            try:
                ws_name = sp_list[sp]
                tbl_name = tbl_list[ws_name]
            except IndexError:
                logging.critical(IndexError)
                raise IndexError

            data_of_tbl = {tbl_name: data}
            data_dict.update(data_of_tbl)

        # Check if the enrollment actually have any value,
        # if not then don't create the file
        count_tbl_without_data = 0
        for tbl in tbl_list:
            try:
                if data_dict[tbl] == []:
                    count_tbl_without_data += 1
            except IndexError:  # Index Error = Table not exist > count increase
                logging.critical(IndexError)
                count_tbl_without_data += 1

        if count_tbl_without_data != len(tbl_list):  # 
            for ws_name in data_dict:
                try:
                    if data_dict[ws_name] == []:
                        continue
                except IndexError:
                    logging.critical(IndexError)
                    raise IndexError

                tbl_name = tbl_list[ws_name]
                data = data_dict[ws_name]
                excel.write_excel(wb, template_file, data, ws_name,
                                  tbl_name)

            file_name = f'{enrollment_number}-report.xlsx'
            local_dest_path =f'../temp/{file_name}' # USE COMMON FUNCTION REAL PATH FOR CONSISTENCE PATH
            excel.refresh_pivot_table(wb)
            excel.save_workbook(wb, local_dest_path)
            self.local_report_path = local_dest_path

    @common.log_function_call
    def get_ea_report(self):
        """
        Query the usage data for all enrollment
        """
        db_cursor = ReportAutomation._db_connect(self)
        ReportAutomation._get_enrollment_list(self)
        # TODO CHECK JSON IF EMPTY
        fileshare_dir_client = ReportAutomation._create_fileshare_client(self)
        
        template_file = azurefileshare.download_file()
        ReportAutomation._create_fileshare_client(self)
        for enrollment in self.enroll_list:
            try:
                enrollment_number = enrollment['name']
                enrollment_name = enrollment['properties']['displayName']
                enrollment_status = enrollment['properties']['accountStatus']
            except IndexError:
                raise IndexError
            logging.info(f'enrollment {enrollment_number} status is: {enrollment_status}')
            if enrollment_status not in self.enrollment_disable_status:
                ReportAutomation.get_usage_enroll(self, template_file,
                                                  db_cursor,
                                                  enrollment_number)
                ReportAutomation._upload_report(self, fileshare_dir_client, "EA", enrollment_name,
                                                enrollment_number)


if __name__ == "__main__":
    load_dotenv()
    a = ReportAutomation()
    a.get_usage_all_enroll()
