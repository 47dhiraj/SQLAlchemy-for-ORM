from database import get_session                

from models import User

from sqlalchemy import select, func, or_, and_, not_

from sqlalchemy.exc import SQLAlchemyError



session = get_session()






try:

    user_count = session.scalar(select(func.count(User.id)))
    
    if user_count < 1:

        seed_users = [
            User(name='Anita Sharma', age=18),
            User(name='Sunita BK', age=18),
            User(name='Radha Tripathi', age=22),
            User(name='Ramesh Poudel', age=22),
            User(name='Hira Maharjan', age=28),
            User(name='Seema Karki', age=28),
            User(name='Sarita Shrestha', age=30),
            User(name='Dipak Thakur', age=30)
        ]

        session.add_all(seed_users)
        session.commit()


except SQLAlchemyError as e:
    session.rollback()          
    print(f"Database error: {e}")
finally:
    session.close()






## group_by() concept

try:

    ## To fetch unique age categories/groups
    stmt = select(User.age).group_by(User.age)


    ## Using .execute() --> best to use when you want to grab multiple columns
    age_groups = session.execute(stmt).all()
    # print(age_groups)


    ## To fetch the count of users of each age categories/groups

    stmt = select(User.age, func.count(User.id)).group_by(User.age)
    users_count_by_age = session.execute(stmt).all()

    for user in users_count_by_age:
        print("age: ", user.age, "count: ", user.count)





except SQLAlchemyError as e:

    session.rollback()      

    print(f"Database error: {e}")

finally:
    session.close()
