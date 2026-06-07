from typing import Optional


from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
)




class Base(DeclarativeBase):
    pass




class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    age: Mapped[Optional[int]] = mapped_column()

    def __repr__(self) -> str:
        return f'<User id: {self.id:>3}: name: {self.name:<13}, age: {self.age:>3}>'

