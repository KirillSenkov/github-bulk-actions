from src.config.settings import Settings
from src.service.make_all_private import make_all_private


# 'make all repos private' | 'not implemented yet'
ACTION = 'make all repos private'


def main():
    print('github-bulk-actions begin')
    status: str = 'success'
    s: Settings = Settings() # type: ignore

    match ACTION:
        case 'make all repos private':
            status = make_all_private(s)
        case _:
            raise NotImplementedError
        
    print(f'github-bulk-actions end. status\'={status}\'')
    return 0 if status == 'success' else 1


if __name__ == "__main__":
    raise SystemExit(main())
