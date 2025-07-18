
import time
import requests
from functools import wraps

def get_credit_balance(api_key: str) -> int:
    """Gets the current credit balance.

    Args:
        api_key: Your Hedra API key.

    Returns:
        The current credit balance.
    """
    url = "https://api.hedra.com/v1/credits"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["balance"]

def retry(exceptions, tries=3, delay=2, backoff=2):
    """Retry decorator with exponential backoff.

    Args:
        exceptions: The exception to check for.
        tries: The number of times to try before giving up.
        delay: The initial delay between retries in seconds.
        backoff: The factor by which to increase the delay.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = f"{e}, Retrying in {mdelay} seconds..."
                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry
