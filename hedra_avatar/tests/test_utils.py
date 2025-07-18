
import pytest
import requests_mock
from hedra_avatar.core.utils import get_credit_balance, retry

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_get_credit_balance(mock_requests):
    mock_requests.get("https://api.hedra.com/v1/credits", json={"balance": 100})
    balance = get_credit_balance("test_api_key")
    assert balance == 100

def test_retry_decorator():
    @retry(ValueError, tries=3, delay=0.1)
    def test_func():
        if call_count[0] < 2:
            call_count[0] += 1
            raise ValueError("Temporary error")
        return "Success"

    call_count = [0]
    assert test_func() == "Success"
    assert call_count[0] == 2

def test_retry_decorator_fails():
    @retry(ValueError, tries=3, delay=0.1)
    def test_func():
        raise ValueError("Persistent error")

    with pytest.raises(ValueError, match="Persistent error"):
        test_func()
