from database import get_session

from models import User, Post, Content

from sqlalchemy import func, select

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import joinedload







session = get_session()







try:

    user_count = session.scalar(select(func.count()).select_from(User))


    if user_count < 1:

        seed_users = [

            User(
                username="johndoe",
                email="john@example.com",
                first_name="John",
                last_name="Doe",
                password="password_123",
                posts=[

                    Post(
                        title="Getting Started with SQLAlchemy 2.0",
                        published=True,
                        content=Content(body="SQLAlchemy 2.0 understanding.")
                    ),
                    Post(
                        title="Advanced Data Science Patterns",
                        published=True,
                        content=Content(body="Deep dive into processing large datasets.")
                    )

                ]
            ),

            User(
                username="janesmith",
                email="jane@example.com",
                first_name="Jane",
                last_name="Smith",
                password="password_456",
                posts=[

                    Post(
                        title="Asyncio in Python 3.14.2",
                        published=False,
                        content=Content(body="Exploring asynchronous programming.")
                    )

                ]
            )

        ]


        session.add_all(seed_users)

        session.commit()

        print("\nDatabase successfully seeded with initial data.\n")






    ## query statement, using, joinedload()
    stmt = (
        select(Post)
        .options(
            joinedload(Post.content),
            joinedload(Post.user)
        )
    )

    posts = session.scalars(stmt)


    for post in posts:

        print(f"\nPost title: {post.title} | Post body: {post.content.body} | Author: {post.user.username}")





except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")



finally:
    
    session.close()
