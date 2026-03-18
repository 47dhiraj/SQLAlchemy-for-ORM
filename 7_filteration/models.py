from typing import Optional


from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
)



## Important Note

## models.py file is the place, where you only write the code to define the database tables

## No other bullshit codes, not even database connection code at all



## creating Base model class
class Base(DeclarativeBase):

    """
        Base class for all ORM models.

        - No columns defined here.
        - Used only to register child models and manage metadata.
    """

    pass





## creating a User model class
class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    age: Mapped[Optional[int]] = mapped_column()

    def __repr__(self) -> str:
        return f'<User id: {self.id:>3}: name: {self.name:<13}, age: {self.age:>3}>'


