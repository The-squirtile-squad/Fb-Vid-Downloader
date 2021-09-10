import pytest
import draft0


@pytest.fixture
def input_value1():
    input = 'oopsie'
    return input


@pytest.fixture
def input_value2():
    input = 30090
    return input


@pytest.fixture
def input_value3():
    input = 'https://fb.watch/7VOkuVaols/'
    return input


@pytest.fixture
def input_value4():
    input = 'C:/Videos/downloader project'
    return input


@pytest.fixture
def input_value5():
    input = 'Rahul'
    return input


def test_tes(input_value1):
    assert input_value1 == 'oopsie'


def test_tes1(input_value2):
    assert input_value2 == 30090


def test_tes2(input_value3):
   assert input_value3 == 'https://fb.watch/7VOkuVaols/'


def test_tes3(input_value4):
   assert input_value4 == 'C:/Videos/downloader project'


def test_tes4(input_value5):
   assert input_value5 == 'Rahul'