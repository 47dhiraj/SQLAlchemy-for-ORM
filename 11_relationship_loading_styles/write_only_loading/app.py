from database import get_session               

from models import User, Post

from sqlalchemy import select, func

from sqlalchemy.orm import joinedload

from sqlalchemy.exc import SQLAlchemyError

from time import perf_counter



## creates session object
session = get_session()



try:

    user_count = session.scalar(select(func.count()).select_from(User))

    if user_count < 1:

        users_to_add = [
            User(
                name=f'\nUser: {y+1}',
                posts=[Post(content=f'Post content: {x+1}') for x in range(2)]
            ) for y in range(100)
        ]
    
        session.add_all(users_to_add)
        session.commit()


    stmt = select(User).where(User.id == 1)
    
    user = session.scalars(stmt).unique().first()


    start = perf_counter()


    if user:
        print(user.name)

        # for (post) in user.posts:               ## this line throws error: TypeError: WriteOnly collections don't support iteration in-place
        #     print(post.content)


    print(f'Done in: {perf_counter() - start}')



except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")



finally:
    session.close()
