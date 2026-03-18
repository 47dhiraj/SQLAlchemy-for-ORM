from typing import Optional, List

from sqlalchemy import Integer, String, create_engine, ForeignKey

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



engine = create_engine('sqlite:///connection.db', echo=True)




## Creates a Base SQLAlchemy model
class Base(DeclarativeBase):
    pass



## Creates a User model for DB table
class User(Base):

    __tablename__ = 'users'                         ## Database table name

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[Optional[str]] = mapped_column(String(60))

    age: Mapped[int] = mapped_column(String(30), nullable=True)




## creates table in DB
Base.metadata.create_all(engine)