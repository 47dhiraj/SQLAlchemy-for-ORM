from sqlalchemy import URL, create_engine

from sqlalchemy.orm import (
    sessionmaker,
)

from models import Base




url_object = URL.create(
    drivername="sqlite",
    database="order.db"
)




engine = create_engine(url_object, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)




def get_session():

    return Session()
