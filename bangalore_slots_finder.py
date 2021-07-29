'''
COVID vaccination slots finder

This script allows the user to find vaccination slots for a provided date and
list of pincodes by calling the public Setu API

Contains the following functions:

get_bangalore_vaccine_slots
'''

import json
import os
import pprint

import requests

API_URL = (
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={0}&date={1}"
)

HEADERS = {'accept': 'application/json', 'Accept-Language': 'hi_IN'}


def get_bangalore_vaccine_slots(date, pincodes):
    """
    This function calls the Setu Appointment Availability find by pin API,
    collects all the responses or exceptions, if any, and returns them

    API docs can be found here: https://apisetu.gov.in/public/api/cowin/cowin-public-v2#/Appointment%20Availability%20APIs/findByPin

    Args:
        date (string): Date to query for - accepted as an env var
        pincodes (list): list of pincodes to search for slots in - accepted as an env var

    Returns:
        tuple: Tuple of responses, request exceptions and timeout exceptions occurred as a result of invoking the Setu findByPin API
    """

    if not isinstance(pincodes, list) and isinstance(pincodes, (str, int)):
        pincodes = [pincodes]

    results = []
    timeouts = []
    exceptions = []

    for pincode in pincodes:

        url = API_URL.format(pincode, date)

        try:

            response = requests.get(url, headers=HEADERS, timeout=5)

        except requests.Timeout as t:

            timeouts.append(t)

        except requests.RequestException as e:

            exceptions.append(e)

        else:

            results.append(response)

    return results, exceptions, timeouts


if __name__ == "__main__":

    date = os.getenv('DATE', '30-07-2021')
    pincodes = os.getenv('PINCODES', '[530068, 560004, 560034]')
    pincodes = json.loads(pincodes)

    results, _, _ = get_bangalore_vaccine_slots(date, pincodes)

    for result in results:
        pprint.pprint(result.json())
