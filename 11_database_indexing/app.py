from database import get_session

from models import User, Post

from sqlalchemy import func, select, text

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import selectinload






session = get_session()





try:

    user_count = session.scalar(select(func.count()).select_from(User))

    if user_count < 1:

        users = [

            User(
                username="johndoe",
                email="john@example.com",
                posts=[
                    Post(
                        title="Getting Started with SQLAlchemy 2.0",
                        published=True,
                        content="SQLAlchemy 2.0 understanding."
                    ),
                    Post(
                        title="Advanced Data Science Patterns",
                        published=False,
                        content="Deep dive into processing large datasets."
                    )
                ]
            ),

            User(
                username="janesmith",
                email="jane@example.com",
                posts=[
                    Post(
                        title="Asyncio in Python 3.14.2",
                        published=True,
                        content="Exploring asynchronous programming."
                    )
                ]
            )

        ]


        session.add_all(users)
        session.commit()

        print("\nDatabase successfully seeded.\n")

    






    ## EXAMPLE 1: Point lookup by indexed unique column

    ## User.username has a unique index → the DB jumps straight to the row.


    stmt = select(User).where(User.username == "johndoe")
    user = session.scalar(stmt)

    print(f"\nUser ID: {user.id} | Username: {user.username} | Email ID: {user.email}\n")






    ## EXAMPLE 2: Filtered lookup using a composite/compound index 

    ## Composite index on (user_id, published, published_at) lets the DB:


    stmt = select(Post).where(Post.user_id == 1, Post.published.is_(True))

    posts = session.scalars(stmt).all()

    for post in posts:
        print(f"\nPost Title: {post.title} | Status: {post.published}\n")







except SQLAlchemyError as e:

    session.rollback()

    print(f"Database error: {e}")




finally:
    session.close()
