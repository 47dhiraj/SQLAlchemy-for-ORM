from sqlalchemy import URL, create_engine

from sqlalchemy.orm import sessionmaker, Session

from models import Base





url_object = URL.create(
    drivername="sqlite",
    database="db_index.db"
)





engine = create_engine(url_object)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)



Base.metadata.create_all(engine)




def get_session() -> Session:

    return SessionLocal()

