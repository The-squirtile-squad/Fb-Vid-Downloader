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


def test_tes(input_value1):
   assert input_value1 == 'oopsie'
   # assert input_value == 30090


def test_tes1(input_value2):
   assert input_value2 == 30090