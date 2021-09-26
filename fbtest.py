from fb3 import check_credentials
from fb3 import validate_input
import pytest


def test_vu():
    # Checking invalid username and valid password
    assert check_credentials('hulk1', 'myshs')


def test_iu():
    # Checking valid username and valid password
    assert check_credentials('hulk', 'iron')


def test_valid_inputs():
    assert validate_input('hulk', 'a_valid$gmail.com')


def test_invalid_input():
    assert not validate_input('buster', 'jarvis@gmail.com')


@pytest.fixture
def input_value3():
    input = 'https://www.facebook.com/watch/?ref=search&v=985324192028850&external_log_id=bec60ea0-7b76-4df2-9479-70940a5a68fd&q=rollin+down+in+the+deep'
    return input


@pytest.mark.skip('https://www.facebook.com/watch/?ref=search&v=985324192028850&external_log_id=bec60ea0-7b76-4df2-9479-70940a5a68fd&q=rollin+down+in+the+deep')
def test_link(input_value3):
    print('Skipped the video link')
