from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)





class Base(DeclarativeBase):
    pass




class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)







class User(BaseModel):

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    first_name: Mapped[str | None] = mapped_column(String(100))      
    last_name: Mapped[str | None] = mapped_column(String(100))

    password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )


    posts: Mapped[list["Post"]] = relationship(
        "Post", 
        back_populates="user", 
        cascade="all, delete-orphan", 
        lazy="raise"
    )


    def __repr__(self) -> str:
        return f"<User ID: {self.id} | Username: {self.username} | Email: {self.email}>"







class Post(BaseModel):

    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    published: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    user: Mapped[User | None] = relationship(
        "User", 
        back_populates="posts", 
        lazy="raise"
    )

    content: Mapped["Content"] = relationship(
        "Content", 
        back_populates="post", 
        cascade="all, delete-orphan", 
        lazy="raise"
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )


    def __repr__(self) -> str:
        return f"<Post ID: {self.id} | Title: {self.title}> | User ID: {self.user_id}"






class Content(BaseModel):

    __tablename__ = 'contents'

    body: Mapped[str] = mapped_column(String(10000), nullable=False)


    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete="CASCADE"), unique=True, nullable=False)

    post: Mapped["Post"] = relationship(
        "Post", 
        back_populates="content", 
        lazy="raise"
    )



    def __repr__(self) -> str:
        return f"<Content ID: {self.id} | Post ID: {self.post_id}>"
