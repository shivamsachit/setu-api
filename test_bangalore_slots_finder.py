'''
Tests for COVID vaccination slots finder

This module contains tests for the COVID vaccination slots finder

Contains the following classes:

TestAllSuccess:

    func test_no_slots
    func test_one_slot
    func test_three_slots

TestSomeTimeouts:

    func test_no_slots_in_successful_calls
    func test_three_slots_in_successful_calls

TestSomeErrors:

    func test_no_slots_in_successful_calls
    func test_three_slots_in_successful_calls

TestAllFailures:

    func test_failure

TestAllTimeouts:

    func test_timeouts

Can be run by invoking `pytest`
'''

import os
from datetime import datetime, timedelta
from unittest import mock

import pytest
import requests

from bangalore_slots_finder import get_bangalore_vaccine_slots
from fixtures import SUCCESS_WITH_1_SLOT, SUCCESS_WITH_3_SLOTS, SUCCESS_WITH_NO_SLOT

ERROR_STATUS_CODES = [500, 502, 503, 504, 520, 522, 524]


def mocked_get_bangalore_vaccine_slots(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    CASE_MAPPING = {
        1: ([MockResponse(SUCCESS_WITH_NO_SLOT, 200)], [], []),
        2: ([MockResponse(SUCCESS_WITH_1_SLOT, 200)], [], []),
        3: ([MockResponse(SUCCESS_WITH_3_SLOTS, 200)], [], []),
        4: ([MockResponse(SUCCESS_WITH_NO_SLOT, 200)], [], [requests.Timeout('timeout')]),
        5: ([MockResponse(SUCCESS_WITH_3_SLOTS, 200)], [], [requests.Timeout('timeout')]),
        6: (
            [MockResponse(SUCCESS_WITH_NO_SLOT, 200)],
            [requests.RequestException('exception')],
            [],
        ),
        7: (
            [MockResponse(SUCCESS_WITH_3_SLOTS, 200)],
            [requests.RequestException('exception')],
            [],
        ),
        8: (
            [
                MockResponse({}, 500),
                MockResponse({}, 500),
                MockResponse({}, 500),
            ],
            [requests.RequestException('exception'), requests.RequestException('exception')],
            [],
        ),
        9: (
            [],
            [],
            [requests.Timeout('timeout'), requests.Timeout('timeout'), requests.Timeout('timeout')],
        ),
    }

    return CASE_MAPPING.get(kwargs['case'])


@pytest.fixture(scope='class')
def data(request):
    '''
    PyTest fixture for using the same date across all tests
    '''
    request.cls.date = os.getenv(
        'DATE', (datetime.today() + timedelta(days=1)).strftime('%d-%m-%Y')
    )


@pytest.mark.usefixtures("data")
class TestAllSuccess:
    """
    Class containing all methods intended to run tests for when all requests are completed succesfully
    """

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_no_slots(self, mock_get):
        '''
        Function to run test to check if no slots were found
        '''
        # mock_get.return_value = {"sessions": [{'slots': []}]}
        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068', case=1)

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == False

        slots = []

        for response in results:

            print(response)

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                slots.extend(location.get('slots', []))

        assert len(slots) == 0

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_one_slot(self, mock_get):
        '''
        Function to run test to check if 1 slot was found
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034', case=2)

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == False

        slots = []

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                slots.extend(location.get('slots', []))

        assert len(slots) == 1

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_three_slots(self, mock_get):
        '''
        Function to run test to check if 3 slots were found
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034', case=3)

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == False

        slots = []

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                slots.extend(location.get('slots', []))

        assert len(slots) == 3


@pytest.mark.usefixtures("data")
class TestSomeTimeouts:
    """
    Class containing all methods intended to run tests for when some of the requests timeout
    """

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_no_slots_in_successful_calls(self, mock_get):
        '''
        Function to run test to check if no slots were found in any successful calls, along with some requests that timed out
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068', case=4)

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == True

        slots = []

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                slots.extend(location.get('slots', []))

        assert len(slots) == 0

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_three_slots_in_successful_calls(self, mock_get):
        '''
        Function to run test to check if 3 slots were found in any successful calls, along with some requests that timed out
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034', case=5)

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == True

        slots = []

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                slots.extend(location.get('slots', []))

        assert len(slots) == 3


@pytest.mark.usefixtures("data")
class TestSomeErrors:
    """
    Class containing all methods intended to run tests for when some of the requests return a 5xx status code
    """

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_no_slots_in_successful_calls(self, mock_get):
        '''
        Function to run test to check if no slots were found in any successful calls, along with some requests that threw a 5xx status code
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068', case=6)

        assert bool(results) == True and bool(exceptions) == True and bool(timeouts) == False

        slots = []

        for response in results:

            if response.status_code == 200:

                response_json = response.json()

                locations = response_json.get('sessions', [])

                for location in locations:

                    slots.extend(location.get('slots', []))

            else:

                assert response.status_code in ERROR_STATUS_CODES

        assert len(slots) == 0

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_three_slots_in_successful_calls(self, mock_get):
        '''
        Function to run test to check if 3 slots were found in any successful calls, along with some requests that threw a 5xx status code
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034', case=7)

        assert bool(results) == True and bool(exceptions) == True and bool(timeouts) == False

        slots = []

        for response in results:

            if response.status_code == 200:

                response_json = response.json()

                locations = response_json.get('sessions', [])

                for location in locations:

                    slots.extend(location.get('slots', []))

            else:

                assert response.status_code in ERROR_STATUS_CODES

        assert len(slots) == 3


@pytest.mark.usefixtures("data")
class TestAllFailures:
    """
    Class containing all methods intended to run tests for when all of the requests return a 5xx status code
    """

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_failure(self, mock_get):

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068', case=8)

        assert bool(exceptions) == True and bool(timeouts) == False

        for response in results:

            assert response.status_code in ERROR_STATUS_CODES


@pytest.mark.usefixtures("data")
class TestAllTimeouts:
    """
    Class containing all methods intended to run tests for when all of the requests timeout
    """

    @mock.patch(
        'test_bangalore_slots_finder.get_bangalore_vaccine_slots',
        side_effect=mocked_get_bangalore_vaccine_slots,
    )
    def test_timeouts(self, mock_get):

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068', case=9)

        assert bool(results) == False and bool(exceptions) == False and bool(timeouts) == True
