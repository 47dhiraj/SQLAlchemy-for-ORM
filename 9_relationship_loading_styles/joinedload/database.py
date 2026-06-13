from sqlalchemy import URL, create_engine

from sqlalchemy.orm import (
    sessionmaker,
    Session,
)

from models import Base





url_object = URL.create(
    drivername="sqlite",
    database="joinedload.db"
)



engine = create_engine(url_object, echo=True)


Base.metadata.create_all(engine)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)





def get_session() -> Session:

    return SessionLocal()
