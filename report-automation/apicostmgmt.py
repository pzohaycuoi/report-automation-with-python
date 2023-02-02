import logging
import common
import requests
import time
import json


common.logger_config()


# @common.log_function_call
def get_enroll_list(token):
    """
    Get list of Azure enterprise agreement's enrollment
    """
    headers = {"Content-Type": "application/json", "Authorization": f"bearer {token}"}
    url = 'https://management.azure.com/providers/Microsoft.Billing/billingAccounts/?api-version=2019-10-01-preview'
    try:
        req = requests.get(url, headers=headers, verify=True)
        req.raise_for_status()
        return json.loads(req.text)
    except requests.exceptions.Timeout as errt:
        max_retry = 5
        for i in range(max_retry):
            logging.warning(f"API request timed out, retrying after 10s, {max_retry - i} retry left")
            i += 1
            time.sleep(10)
            req = requests.get(url, headers=headers, verify=True)
            if req != '':
                return json.loads(req.text)
        logging.critical("API request timed out, no retry left: {errt}")
        raise errt
    except requests.exceptions.HTTPError as errh:
        # TODO if error response code 401 400 then have to renew the API token
        logging.critical(f"Http Error: {errh}")
        raise errh
    except requests.exceptions.ConnectionError as errc:
        logging.critical(f"Error Connecting: {errc}")
        raise errc
    except requests.exceptions.RequestException as err:
        logging.critical(f"OOps: Something Else {err}")
        raise err


if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()
    get_enroll_list(getenv('API_KEY'))
