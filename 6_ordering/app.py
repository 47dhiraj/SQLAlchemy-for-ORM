import random

from database import get_session     

from models import User

from sqlalchemy import select, func

from sqlalchemy.exc import SQLAlchemyError




session = get_session()




names = ['BakraTunda Ganeshaa', 'Hari Sharanam', 'Ram Sharanam', 'Maiyaa Laxmi', 'Bam Bhole']

ages = [10, 25, 100, 60, 10, 15, 70, 40, 120]




try:

    user_count = session.scalar(select(func.count(User.id)))
    # print('user count: ', user_count)

    if user_count < 1:
        
        for __ in range(20):
            user = User(username=random.choice(names), age=random.choice(ages))
            session.add(user)       


        session.commit()         

        print("Seeded 20 random users successfully.")



except SQLAlchemyError as e:

    session.rollback()              
    print(f"Database error: {e}")


finally:
    session.close()






try:


    # users_stmt = select(User).order_by(User.age)    
    users_stmt = select(User).order_by(User.username)    

    all_users = session.scalars(users_stmt).all()

    print(type(all_users), all_users)     

    for user in all_users:
        print(f"id: {user.id}  name: {user.username}  age: {user.age}")




    users_stmt = select(User).order_by(User.age.desc())
    # users_stmt = select(User).order_by(User.id.desc())

    all_users = session.scalars(users_stmt).all()


    for user in all_users:
        print("id: {}  name: {}  age: {}". format(user.id, user.username, user.age))



    users_stmt = select(User).order_by(User.age, User.username)

    all_users = session.scalars(users_stmt).all()

    for user in all_users:
        print(f"id: {user.id}  name: {user.username}  age: {user.age}")



except SQLAlchemyError as e:

    session.rollback()
    print(f"Database error during query: {e}")


finally:

    session.close()
