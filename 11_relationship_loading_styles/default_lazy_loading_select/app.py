from database import get_session                

from models import User, Post

from sqlalchemy import select, func

from sqlalchemy.exc import SQLAlchemyError

from time import perf_counter





session = get_session()




try:

    user_count = session.scalar(select(func.count()).select_from(User))
    


    if user_count < 1:

        users_to_add = [
            User(
                name=f'\nUser: {y+1}',
                posts=[Post(content=f'Post content: {x+1}') for x in range(5)]
            ) for y in range(1_000)
        ]
    
        session.add_all(users_to_add)
        session.commit()



    users = session.scalars(select(User)).all()

    start = perf_counter()

    for user in users:
        user.posts

    print(f'Done in: {perf_counter() - start}')




except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")


finally:
    session.close()
