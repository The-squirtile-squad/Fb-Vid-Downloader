from main import check_credentials
from main import validate_input
import pytest


def test_vuvp():
    # Checking valid username and valid password
    assert check_credentials('oopsie', '30090')


def test_iuvp():
    # Checking invalid username and valid password
    assert check_credentials('ok', '30090')


def test_valid_inputs():
    assert validate_input('AUniqueUserName', 'a_valid@email.yes', 'V@lid_p@ssw0rd')


def test_invalid_username():
    assert not validate_input('oopsie', 'a_valid@email.yes', 'V@lid_p@ssw0rd')


@pytest.fixture
def input_value3():
    input = 'https://fb.watch/7VIxFyHzEz/'
    return input


@pytest.mark.skip('https://fb.watch/7VIxFyHzEz/')
def test_link(input_value3):
    print('I skipped the video link')