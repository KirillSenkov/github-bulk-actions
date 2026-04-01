from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_project_root() / '.env',
        env_file_encoding='utf-8'
    )
    gituser: str
    token: str
    repos_url: str
    repo_url: str

    @field_validator('gituser', 'token', 'repos_url', 'repo_url')
    @classmethod
    def check_required(cls, v: str, info) -> str:
        if not v:
            raise ValueError(f'{info.field_name} is required but not set in .env')
        return v