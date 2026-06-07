from sqlalchemy import URL, create_engine

from sqlalchemy.orm import (
    sessionmaker,
    Session,
)


from models import Base




url_object = URL.create(
    drivername="sqlite",
    database="full_join.db"
)



engine = create_engine(url_object)


Base.metadata.create_all(engine)




SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)





def get_session() -> Session:

    return SessionLocal()
