from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_database_config


def create_database_engine() -> Engine:
    database_config = get_database_config()

    return create_engine(
        database_config.connection_string,
        pool_pre_ping=True,
    )


engine = create_database_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
