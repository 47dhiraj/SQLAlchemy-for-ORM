from sqlalchemy import URL, create_engine

from sqlalchemy.orm import (
    sessionmaker,
)

## importing Base class from models.py
from models import Base


## database.py file is the best place to 
## creates engine, session factory & actually creates all tables in database.


## creating url object for database connection string
url_object = URL.create(
    drivername="sqlite",
    database="one_to_many.db"
)




## Create a database engine.
## The engine is the core interface between SQLAlchemy and the database.
## It manages connections and executes SQL statements.

'''
    Why engine is created outside get_session() ??

    - It is because these objects are heavy infrastructure objects that should be created only once for the entire application, not every time you request a session.

    - SQLAlchemy expects one engine per database, so we create/define it only once. 
    Then reuse it everywhere.

'''


# engine = create_engine(url_object, echo=True)

engine = create_engine(url_object, echo=False)




## this line of code, actually creates all tables in the database only once at the startup of the app.
## It ensures tables exist before any session tries to use them
Base.metadata.create_all(engine)




## Create a session factory bound to the engine (this line doesn't create a session)

## It is only a blueprint or factory to create a session later inside get_session()

## session factory is created only once and reused, avoiding unnecessary recreation, improving performance & resource efficiency
## so, this is the reason we create session factory(i.e SessionLocal) outside get_session()
Session = sessionmaker(bind=engine)




## get_session() is a custom function
## which returns a new database session object each time you call it from app.py
def get_session():

    ## This line only actually instantiate/create new session object
    ## returning session object
    return Session()
