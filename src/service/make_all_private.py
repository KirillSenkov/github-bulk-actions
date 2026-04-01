from src.config.settings import Settings
from src.repo.get_all_repos import get_all_repos
from src.repo.set_repo_private import set_repo_private

def make_all_private(s: Settings) -> str:
    """
    Convert all public repositories of a user to private.

    Prints progress and errors to stdout.

    Args:
        s (Settings): Constants of the .env file.

    Returns:
        str: 'success' | 'partial' | 'fail'
    """
    status: str = 'success'
    repos: list[dict] = []
    all_errors: list[tuple[str, Exception]] = []
    success_cnt: int = 0
    repos_cnt: dict[str, int] = {'public': 0, 'private': 0}
    response : dict = {}

    try:
        repos = get_all_repos(url=s.repos_url, token=s.token)
    except Exception as e:
        status = 'fail'
        all_errors.append(('get_all_repos()', e))
    
    for repo in repos:
        if repo['private']:
            repos_cnt['private'] += 1
            continue
        else:
            repos_cnt['public'] += 1
        
        try:
            response  = set_repo_private(
                url=s.repo_url,
                user=s.gituser,
                repo=repo['name'],
                token=s.token
            )
            if response ['status_code'] == 200:
                success_cnt += 1
                print(f'\'{repo['name']}\' - Ok')
            else:
                body = dict(response ['body'])
                errors = body.get('errors', [])
                messages = [item['message'] for item in errors]
                status = 'partial'
                print(
                    f'\'{repo['name']}\' response :\n'
                    f'    status_code: {response ['status_code']}\n'
                    f'    response: {response ['response']}\n'
                    f'    message: {', '.join(messages)}'
                )
        except Exception as e:
            status = 'partial' if status == 'success' else 'fail'
            all_errors.append((repo['name'], e))

    if all_errors:
        len_errors = len(all_errors)
        print(f'{len_errors} error{'' if len_errors == 1 else 's'}:')
        for name, exception in all_errors:
            print(f'    {name}: {exception}')

    repos_len = len(repos)
    rate_str = f'({(success_cnt / repos_len):.1%})' if repos else ''
    print(
        f'private: {repos_cnt['private']}\n'
        f'public: {repos_cnt['public']}\n'
        f'{success_cnt} made private of '
        f'{repos_len} repo{'' if repos_len == 1 else 's'} total {rate_str}'      
    )
    return status
