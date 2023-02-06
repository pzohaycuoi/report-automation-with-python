import common
import logging
from dotenv import load_dotenv
import database
import apicostmgmt
import os
from datetime import date
import time
import excel


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

    @common.log_function_call
    def get_enrollment_list(self):
        """
        Get Azure Enterprise Agreement enrollment number list
        """
        data = apicostmgmt.get_enroll_list(os.getenv('API_KEY'))
        self.enroll_list = data['value']

    @common.log_function_call
    def get_previous_month(self):
        """
        Get previous month includes month and year
        """
        today = date.today()
        self.report_year = int(today.strftime("%Y"))
        self.report_month = int(today.strftime("%m"))
        if self.report_month == 1:
            self.report_year = self.report_year - 1
            self.report_month = 12
        else:
            self.report_month = self.report_month - 1
        # report_period = {'report_year': self.report_year,
        #                  'report_month': self.report_month}

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
        if self.report_month is None or self.report_year is None:
            logging.warning('report month and year is not provided, retrying')
            max_retry = 5
            for i in range(max_retry):
                if i > 5:
                    logging.critical('Unable to get report month and year')
                    raise SystemError('Unable to get report month and year')
                i += 1
                ReportAutomation._get_previous_month()
                if self.report_month is not None and self.report_year is not None:
                    continue
                time.sleep(1)
        params = f"@EnrollmentNumber={enrollment_number},@year={self.report_year},@month={self.report_month}"
        data = database.exec_stored_procedure(cursor, stored_procedure, params)
        return data

    @common.log_function_call
    def get_usage_for_an_enrollment(self, template_file, db_cursor, enrollment_number):
        """
        Query the usage data of an Enrollment
        """
        sp_list = {'proc_data_report_ea': 'raw_usage',
                   'proc_data_ri_report_ea': 'raw_ri',
                   'proc_data_balance_summary_report_ea': 'BalanceSummary',
                   'proc_data_marketplace_report_ea': 'raw_marketplace'}
        tbl_list = {'raw_usage': 'raw_usage',
                   'raw_ri': 'raw_ri',
                   'BalanceSummary': 'BalanceSummary',
                   'raw_marketplace': 'raw_marketplace'}
        wb = excel.load_excel(template_file)
        for sp in sp_list:
            data = ReportAutomation()._exec_stored_procedures(db_cursor,
                                                            sp, enrollment_number)
            ws_name = sp_list[sp]
            tbl_name = tbl_list[ws_name]
            excel.write_excel(wb, template_file, data, ws_name, tbl_name)
        file_name = f'{enrollment_number}-report.xlsx'
        destination_path = f'C:/Users/namng/OneDrive/Code/Python/report-automation-with-python/temp/{file_name}'
        excel.refresh_pivot_table(wb)
        excel.save_workbook(wb, destination_path)

    @common.log_function_call
    def get_usage_for_all_enrollment(self):
        """
        Query the usage data for all enrollment
        """
        db_cursor = ReportAutomation._db_connect(self)
        # TODO CHECK JSON IF EMPTY
        template_file = 'C:/Users/namng/OneDrive/Code/Python/report-automation-with-python/template/Book1.xlsx'
        for enrollment in self.enroll_list:
            enrollment_number = enrollment['name']
            # enrollment_name = enrollment['properties']['displayName']
            enrollment_status = enrollment['properties']['accountStatus']
            logging.info(f'Enrollment {enrollment_number} status is: {enrollment_status}')
            if enrollment_status not in self.enrollment_disable_status:
                ReportAutomation().get_usage_for_an_enrollment(template_file, db_cursor, enrollment_number)


if __name__ == "__main__":
    load_dotenv()
    a = ReportAutomation()
    a.get_enrollment_list()
    a.get_previous_month()
    a.get_usage_for_all_enrollment()
