from database import get_session

from models import User, Post, Content

from sqlalchemy import func, select

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import lazyload







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

        print("Database successfully seeded with initial data.")






    ## query statement, using, lazyload()
    stmt = (
        select(User)
        .where(User.username == "johndoe")
        .options(
            lazyload(User.posts).lazyload(Post.content)
        )
    )


    user = session.scalar(stmt)




    if user:

        for post in user.posts:
            print(f"\nUser ID: {user.id} | Username: {user.username} | Post ID: {post.id} | Post Title: {post.title} | Content: {post.content.body}\n")


    else:
        print("\nUser not found !\n")








except SQLAlchemyError as e:

    session.rollback()      

    print(f"Database error: {e}")



finally:
    
    session.close()
