from sqlalchemy import ForeignKey, String, Text

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

    id: Mapped[int] = mapped_column(primary_key=True)




class User(BaseModel):

    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(50))
    
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan",
        ## lazy="subquery"                           
    )

    def __repr__(self) -> str:
        return f'<User {self.name}>'




class Post(BaseModel):

    __tablename__ = 'posts'

    content: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f'<Post {self.id}>'
