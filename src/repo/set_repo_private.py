from src.api.CRUD import patch_with_retry

def set_repo_private(
        url: str,
        user: str,
        repo: str,
        token: str,
        retries: int = 3,
        delay: int = 2,
        timeout: float = 10.0
) -> dict:
    """
    Set a repository visibility to private.

    Args:
        url (str): GitHub API endpoint.
        user (str): GitHub username.
        repo (str): Repository name.
        token (str): Personal access token.

    Returns:
        dict: {
            'status_code': int,
            'response': httpx.Response,
            'body': dict | None
        }
    """
    url = f'{url}/{user}/{repo}'
    headers = {'Authorization': f'Bearer {token}'}
    req_json = {'private': True}

    response = patch_with_retry(
        url=url,
        headers=headers,
        json=req_json,
        retries=retries,
        delay=delay,
        timeout=timeout
    )

    try:
        body = response.json()
    except ValueError:
        body = None

    return {'status_code': response.status_code,
            'response': response,
            'body': body}
