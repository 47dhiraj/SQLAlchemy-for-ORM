from sqlalchemy import ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)






class Base(DeclarativeBase):

    pass




class BaseModel(Base):

    __abstract__ = True             
    id: Mapped[int] = mapped_column(Integer, primary_key=True)





class User(BaseModel):

    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    
    addresses: Mapped[list['Address']] = relationship(back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, age='{self.age}')>"
    




class Address(BaseModel):

    __tablename__ = 'addresses'

    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    zip_code: Mapped[int] = mapped_column(Integer)
    street: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    user: Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self):
        return f"<Address (id={self.id}, city='{self.city}')>"
    
