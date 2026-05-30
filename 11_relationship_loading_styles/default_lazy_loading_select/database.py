from sqlalchemy import URL, create_engine

from sqlalchemy.orm import (
    sessionmaker,
)


from models import Base





url_object = URL.create(
    drivername="sqlite",
    database="lazy_load.db"
)




'''
    Why engine is created outside get_session() ??

    - It is because these objects are heavy infrastructure objects that should be created only once for the entire application, not every time you request a session.

    - SQLAlchemy expects one engine per database, so we create/define it only once. 
    Then reuse it everywhere.

'''


engine = create_engine(url_object, echo=True)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)





def get_session():    
    
    return Session()


