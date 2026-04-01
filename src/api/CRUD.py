import time

import httpx

def post_with_retry() -> httpx.Response:
    raise NotImplementedError

def get_with_retry(
        url: str,
        headers: dict,
        params: dict,
        retries: int = 3,
        delay: int = 2,
        timeout: float = 10.0
) -> httpx.Response:
    if not url or retries < 1 or delay < 0 or timeout <= 0:
        return httpx.Response(status_code=400)
    for attempt in range(retries):
        try:
            return httpx.get(url=url, headers=headers, params=params, timeout=timeout)
        except httpx.TransportError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise
    raise RuntimeError('unreachable')

def patch_with_retry(
        url: str,
        headers: dict,
        json: dict, 
        retries: int = 3,
        delay: int = 2,
        timeout: float = 10.0
) -> httpx.Response:
    if not url or retries < 1 or delay < 0 or timeout <= 0:
        return httpx.Response(status_code=400)
    for attempt in range(retries):
        try:
            return httpx.patch(url=url, headers=headers, json=json, timeout=timeout)
        except httpx.TransportError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise
    raise RuntimeError('unreachable')

def delete_with_retry() -> httpx.Response:
    raise NotImplementedError
