from sqlalchemy import ForeignKey, Text, Column, create_engine, Table


from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
    sessionmaker,
)




class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(primary_key=True)




class User(Base):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")




class Comment(Base):

    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")





class Category(Base):

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="category")









post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)




class Post(Base):

    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    category: Mapped["Category"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(
        secondary="post_tag", back_populates="posts"
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")   






class Tag(Base):

    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[list["Post"]] = relationship(
        secondary="post_tag", back_populates="tags"
    )






def get_session():

    engine = create_engine("sqlite:///crud_1.db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session()




session = get_session()