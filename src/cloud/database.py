import sqlalchemy
from sqlalchemy import orm

from cloud.settings import settings

engine = sqlalchemy.create_engine(
    url=settings.database_url,
    connect_args={
        "check_same_thread": False,
    },
)

_Session = orm.sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def session() -> _Session:
    s = _Session()
    try:
        yield s
    finally:
        s.close()
