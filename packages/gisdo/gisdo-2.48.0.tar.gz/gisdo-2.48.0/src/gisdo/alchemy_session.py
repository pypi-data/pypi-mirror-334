from contextlib import (
    contextmanager,
)

from sqlalchemy.orm import (
    sessionmaker,
)

from gisdo.settings import (
    engine,
)


Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
    except:
        raise
    finally:
        session.close()
