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

import pytest

from bangalore_slots_finder import get_bangalore_vaccine_slots

ERROR_STATUS_CODES = [500, 502, 503, 504, 520, 522, 524]


@pytest.fixture(scope='class')
def data(request):
    '''
    PyTest fixture for using the same date across all tests
    '''
    request.cls.date = os.getenv('DATE', '30-07-2021')


@pytest.mark.usefixtures("data")
class TestAllSuccess:
    """
    Class containing all methods intended to run tests for when all requests are completed succesfully
    """

    def test_no_slots(self):
        '''
        Function to run test to check if no slots were found
        '''
        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068')

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == False

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) == 0

    def test_one_slot(self):
        '''
        Function to run test to check if 1 slot was found
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034')

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == False

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) == 1

    def test_three_slots(self):
        '''
        Function to run test to check if 3 slots were found
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034')

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == False

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) >= 3


@pytest.mark.usefixtures("data")
class TestSomeTimeouts:
    """
    Class containing all methods intended to run tests for when some of the requests timeout
    """

    def test_no_slots_in_successful_calls(self):
        '''
        Function to run test to check if no slots were found in any successful calls, along with some requests that timed out
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068')

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == True

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) == 0

    def test_three_slots_in_successful_calls(self):
        '''
        Function to run test to check if 3 slots were found in any successful calls, along with some requests that timed out
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034')

        assert bool(results) == True and bool(exceptions) == False and bool(timeouts) == True

        for response in results:

            assert response.status_code == 200

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) >= 3


@pytest.mark.usefixtures("data")
class TestSomeErrors:
    """
    Class containing all methods intended to run tests for when some of the requests return a 5xx status code
    """

    def test_no_slots_in_successful_calls(self):
        '''
        Function to run test to check if no slots were found in any successful calls, along with some requests that threw a 5xx status code
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068')

        assert bool(results) == True and bool(exceptions) == True and bool(timeouts) == False

        for response in results:

            assert response.status_code in ERROR_STATUS_CODES

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) == 0

    def test_three_slots_in_successful_calls(self):
        '''
        Function to run test to check if 3 slots were found in any successful calls, along with some requests that threw a 5xx status code
        '''

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '560034')

        assert bool(results) == True and bool(exceptions) == True and bool(timeouts) == False

        for response in results:

            assert response.status_code in ERROR_STATUS_CODES

            response_json = response.json()

            locations = response_json.get('sessions', [])

            for location in locations:

                assert len(location.get('slots', [])) >= 3


@pytest.mark.usefixtures("data")
class TestAllFailures:
    """
    Class containing all methods intended to run tests for when all of the requests return a 5xx status code
    """

    def test_failure(self):

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068')

        assert bool(exceptions) == True and bool(timeouts) == False

        for response in results:

            assert response.status_code in ERROR_STATUS_CODES


@pytest.mark.usefixtures("data")
class TestAllTimeouts:
    """
    Class containing all methods intended to run tests for when all of the requests timeout
    """

    def test_timeouts(self):

        results, exceptions, timeouts = get_bangalore_vaccine_slots(self.date, '530068')

        assert bool(results) == False and bool(exceptions) == False and bool(timeouts) == True
