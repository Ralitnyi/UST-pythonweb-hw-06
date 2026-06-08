import os
from importlib.util import find_spec

from sqlalchemy import create_engine

def get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        return "sqlite:///./dev.db"

    # If psycopg (v3) is installed, prefer the `psycopg` dialect name
    if url.startswith("postgresql://") and find_spec("psycopg") is not None:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


def get_engine(echo: bool = False):
    return create_engine(get_database_url(), echo=echo)