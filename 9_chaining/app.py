from database import get_session                ## importing get_session() function from database.py

from models import User

from sqlalchemy import select, func, or_, and_, not_

from sqlalchemy.exc import SQLAlchemyError




## creates session object
session = get_session()





## To insert fake initial data to database

try:

    user_count = session.scalar(select(func.count(User.id)))
    
    if user_count < 1:

        seed_users = [
            User(name='Anita Sharma', age=18),
            User(name='Sunita BK', age=18),
            User(name='Radha Tripathi', age=22),
            User(name='Ramesh Poudel', age=22),
            User(name='Hira Maharjan', age=30),
            User(name='Seema Karki', age=30),
            User(name='Sarita Shrestha', age=40),
            User(name='Dipak Thakur', age=40)
        ]

        session.add_all(seed_users)
        session.commit()



except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")
    
finally:
    session.close()








## chaining multiple clause/methods


try:


    stmt = (
        select(User.age, func.count(User.id).label("users_count"))
        .where(User.age > 16)
        .where(User.age < 50)
        .group_by(User.age)
        .order_by(User.age)
    )


    users_age_count = session.execute(stmt).all()

    for age, count in users_age_count:
        print(f'Age: {age} - Users: {count}')





except SQLAlchemyError as e:
    session.rollback()      
    print(f"Database error: {e}")

finally:
    session.close()
