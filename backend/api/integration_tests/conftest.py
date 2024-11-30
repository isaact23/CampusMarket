import pytest
from api.database.database import Database

@pytest.fixture(scope='function')
def database():
    database = Database()
    database.reset()
    yield database
    database.reset()
    database.dispose() 