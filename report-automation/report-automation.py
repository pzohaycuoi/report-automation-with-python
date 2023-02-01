import common
import logging
from dotenv import load_dotenv
import database
import apicostmgmt
import os
from datetime import date
import time


# Setup logging
common.logger_config()


class ReportAutomation():
    def __init__(self):
        self.enroll_list = None
        self.report_month = None
        self.report_year = None
        self.enrollment_active_staus = ('Active', 'Extended')
        self.enrollment_disable_status = ('Deleted', 'Disabled', 'Expired',
                                          'Transferred', 'Terminated',
                                          'ManuallyTerminated')

    def get_enrollment_list(self, api_key):
        """
        Get Azure Enterprise Agreement enrollment number list
        """
        self.enroll_list = apicostmgmt.get_enroll_list(api_key)

    def _get_previous_month(self):
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

    def query_usage_data(self, enrollment, ):
        """
        """
        def _load_env(self):
            """
            Load environment variables
            """
            load_dotenv()

        def _db_connect(self):
            """
            Connect to database
            Must run after _load_env method
            """
            conn, cursor = database.connection('DRIVER='+os.getenv('DB_DRIVER')+';SERVER=tcp:'+os.getenv('DB_ADDR')+';PORT=1433;DATABASE='+os.getenv('DB_NAME')+';UID='+os.getenv('DB_USER')+';PWD='+ os.getenv('DB_USER_PWD'))
            # TODO ERROR HANDLING
            return conn, cursor

        def _exec_stored_procedures(cursor, stored_procedure,
                                    enrollment_number):
            """
            Exectute SQL stored procedure to get the data
            Must execute after _get_previous_month
            """
            if enrollment_number is None or enrollment_number == '':
                logging.error('Enrollment Number is not provided')
                return False
            if self.report_month is None or self.report_year is None:
                logging.warning('report month and year is not provided, retrying...')
                max_retry = 5
                for i in range(max_retry):
                    if i > 5:
                        logging.critical('Unable to get report month and year, terminating...')
                        raise SystemError('Unable to get report month and year, terminating...')
                    logging.warning(f"Report month and year is not provided, retrying after 1s, {max_retry - i} retries left")
                    i += 1
                    ReportAutomation._get_previous_month()
                    if self.report_month is not None or self.report_year is not None:
                        logging.info(f"Success: Got report month is {self.report_month} and year is {self.report_year}")
                        continue
                    time.sleep(1)

            logging.info(f'Executing stored procedure {stored_procedure} for enrollment: {enrollment_number} :: {enrollment_name}')
            params = f"'@EnrollmentNumber={enrollment_number}','@year={self.report_year}','@month={self.report_month}'"
            data = database.exec_stored_procedure(cursor,
                                                  stored_procedure, params)
            return data

        logging.info('Initialize environment variables')
        _load_env()
        logging.info('Connecting to database')
        db_conn, db_cursor = _db_connect()
        ReportAutomation._get_previous_month()
        logging.info(f'Report month: {self.report_month}-{self.report_year}')
        sp_list = ("proc_data_report_ea",
                   "proc_data_ri_report_ea",
                   "proc_data_balance_summary_report_ea",
                   "proc_data_marketplace_report_ea")

        for enrollment in self.enroll_list:
            # TODO CHECK JSON IF EMPTY
            enrollment_number = enrollment['name']
            enrollment_name = enrollment['properties']['displayName']
            enrollment_status = enrollment['properties']['accountStatus']
            logging.info(f'Enrollment {enrollment_number} :: {enrollment_name} status is: {enrollment_status}')
            if enrollment_status not in self.enrollment_disable_status:
                logging.info(f'Querying data for enrollment: {enrollment_number} :: {enrollment_name}')
                for sp in sp_list:
                    data = _exec_stored_procedures(db_cursor, sp, enrollment_number)
