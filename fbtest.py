from fb3 import check_credentials
from fb3 import validate_input
import pytest


def test_vuvp():
    # Checking valid username and valid password
    assert check_credentials('oopsie', '30090')


def test_iuvp():
    # Checking invalid username and valid password
    assert check_credentials('ok', '30090')


def test_valid_inputs():
    assert validate_input('AUniqueUserName', 'a_valid@email.yes', 'V@lid_p@ssw0rd')


def test_invalid_input():
    assert not validate_input('oopsie', 'a_valid@email.yes', 'V@lid_p@ssw0rd')


@pytest.fixture
def input_value3():
    input = 'https://www.facebook.com/watch/?ref=search&v=985324192028850&external_log_id=bec60ea0-7b76-4df2-9479-70940a5a68fd&q=rollin+down+in+the+deep'
    return input


@pytest.mark.skip('https://www.facebook.com/watch/?ref=search&v=985324192028850&external_log_id=bec60ea0-7b76-4df2-9479-70940a5a68fd&q=rollin+down+in+the+deep')
def test_link(input_value3):
    print('Skipped the video link')
