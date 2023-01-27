import common
import logging
from dotenv import load_dotenv
import database
import apicostmgmt
import os
from datetime import date


# Setup logging
common.logger_config()

# Loading environment variable
logging.info('Initialize environment variables')
load_dotenv()

# Get Azure enterprise agreement enrollment list
logging.info('Getting enrollment list')
enroll_list = apicostmgmt.get_enroll_list(os.getenv("API_KEY"))
logging.info('Connecting to database')
db_conn, db_cursor = database.connection('DRIVER='+os.getenv('DB_DRIVER')+';SERVER=tcp:'+os.getenv('DB_ADDR')+';PORT=1433;DATABASE='+os.getenv('DB_NAME')+';UID='+os.getenv('DB_USER')+';PWD='+ os.getenv('DB_USER_PWD'))

# Get previous month includes month and year
today = date.today()
year = int(today.strftime("%Y"))
month = int(today.strftime("%m"))
if month == 1:
    year = year - 1
    month = 12
else:
    month = month - 1

logging.info(f'Report month: {month}-{year}')

# Get Azure usage data of enrollments
enrollment_active_status = ('Active', 'Extended')
enrollment_disable_status = ('Deleted', 'Disabled', 'Expired', 'Transferred', 'Terminated', 'ManuallyTerminated')
for enrollment in enroll_list['value']:
    enrollment_number = enrollment['name']
    enrollment_name = enrollment['properties']['displayName']
    enrollment_status = enrollment['properties']['accountStatus']
    logging.info(f'Enrollment {enrollment_number} :: {enrollment_name} status is: {enrollment_status}')
    if enrollment_status not in enrollment_disable_status:
        logging.info(f'Querying data for enrollment: {enrollment_number} :: {enrollment_name}')
        test = database.exec_stored_procedure(db_cursor, "proc_data_report_ea", f'@EnrollmentNumber={enrollment_number}', '@year=2022', '@month=12')
        