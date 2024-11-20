import pytest
from database import *

# Reset the database before each test
@pytest.fixture(scope='function', autouse=True)
def run_tests():
    database_delete_everything()
    assert is_database_empty()

# Reset the database at the end of the testing session
@pytest.fixture(scope='session', autouse=True)
def teardown():
    database_delete_everything()
