from src.api.CRUD import get_with_retry

def get_all_repos(
        url: str,
        token: str,
        retries: int = 3,
        delay: int = 2,
        timeout: float = 10.0
) -> list[dict]:
    """
    Fetch all repositories for a user via GitHub API with pagination.

    Args:
        url (str): GitHub API endpoint.
        token (str): Personal access token.

    Returns:
        list[dict]: List of repository objects.
    """
    result = []
    headers = {'Authorization': f'Bearer {token}'}
    params = {'per_page': 100, 'type': 'all'}
    page = 1

    while True:
        params['page'] = page
        response = get_with_retry(
            url=url,
            headers=headers,
            params=params,
            retries=retries,
            delay=delay,
            timeout=timeout
        )
        try:
            body = response.json()
        except ValueError:
            body = {}
        result.extend(body)
        if 'rel="next"' not in dict(response.headers).get('link', ''):
            break
        page += 1

    return result