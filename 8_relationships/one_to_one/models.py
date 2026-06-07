from sqlalchemy import ForeignKey, Integer, String, Text, create_engine

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
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan",        
        single_parent=True                    
    )


    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}, age='{self.age}')>"





class UserProfile(BaseModel):

    __tablename__ = 'user_profiles'

    bio: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(String(512))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True, nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="profile")   


    def __repr__(self):
        return f"<Address (id={self.id}, city='{self.bio}')>"
    
