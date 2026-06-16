from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, func, Index

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

    id: Mapped[int] = mapped_column(primary_key=True)   ## every primary key column is automatically given a unique Binary Tree index







class User(BaseModel):

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  ## using index=True for indexing a column (for eg: indexing username field)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)    ## using index=True for indexing a column (for eg: indexing email field)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()                           
    )


    def __repr__(self) -> str:
        return f"<User ID: {self.id} | Username: {self.username} | Email: {self.email}>"








class Post(BaseModel):

    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)     ## index=True for indexing single column

    content: Mapped[str] = mapped_column(String(3500))


    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="posts")


    published: Mapped[bool] = mapped_column(default=True, nullable=False)

    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )




    ## for using compsite(compound) indexes in a table
    __table_args__ = (
        Index('ix_posts_userid_status_date', 'user_id', 'published', 'published_at'),
    )



    def __repr__(self) -> str:
        return f"<Post ID: {self.id} | Title: {self.title} | User ID: {self.user_id}>"

