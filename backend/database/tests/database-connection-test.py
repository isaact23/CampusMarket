import pytest
from database import *
from market_types import *
from unittest.mock import patch

@patch('pyodbc.connect')
def test_fail_connection(mock_connect):
    mock_connect.side_effect = pyodbc.OperationalError("Mocked error")

    with pytest.raises(RuntimeError):
        get_conn()
