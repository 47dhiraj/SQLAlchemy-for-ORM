from database import get_session               

from models import User

from sqlalchemy import select, func, or_, and_, not_

from sqlalchemy.exc import SQLAlchemyError






session = get_session()





try:

    

    user_count = session.scalar(select(func.count(User.id)))
    

    if user_count < 1:

        seed_users = [
            User(name='Ramesh Sankamaila', age=25),
            User(name='Lakhhan Babluwa', age=56),
            User(name='Torpee Sasur', age=25),
            User(name='Suddo Man', age=99)
        ]


        session.add_all(seed_users)

        session.commit()


        stmt = select(User)

        all_users = session.scalars(stmt).all()

        # print('All Users:', len(all_users))
        # print(all_users)








    # ******************************** .where(), filter_by()  OPERATIONS ********************************


    stmt = select(User).where(User.age >= 25)     
    # stmt = select(User).filter_by(age = 25)

    adult_users = session.scalars(stmt).all()
    

    print('Filtered Users:', len(adult_users))

    for user in adult_users:
        print(user.id, user.name, user.age)











    ## ******************************** OR OPERATION ********************************


    stmt = select(User).where(or_(User.age >= 30, User.name == 'Lakhhan Babluwa'))

    users = session.scalars(stmt).all()

    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)









    ## **************** AND & OPERATION ****************


    ## default use case of and operation

    stmt = select(User).where(User.age >= 30, User.name == 'Lakhhan Babluwa')
    users = session.scalars(stmt).all()

    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)




    ## explicitly using and_() function

    stmt = select(User).where(and_(User.age >= 30, User.name == 'Lakhhan Babluwa'))
    users = session.scalars(stmt).all()

    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)












    ## **************** NOT OPERATION ****************


    ## using: not_() function
    stmt = select(User).where(not_(User.name == 'Lakhhan Babluwa'))

    ## using: '!=' operator
    # stmt = select(User).where(User.name != 'Lakhhan Babluwa')


    users = session.scalars(stmt).all()

    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)












    ## **************** COMBINE MIX OPERATIONS ****************



    ## comboo condition inside or_
    stmt = select(User).where(
                                or_(
                                    User.name != 'Lakhhan Babluwa', 
                                    and_(User.age > 35, User.age < 60)
                                )
                            )
    

    ## comboo condition inside and_
    stmt = select(User).where(
                                and_(
                                    User.name != 'Lakhhan Babluwa', 
                                    and_(User.age > 35, User.age < 60)
                                )
                            )



    users = session.scalars(stmt).all()


    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)










    ## ****************  .in_()  OPERATION ****************


    possible_names = ['Ramesh Sankamaila', 'Torpee Sasur']

    stmt = select(User).where(User.name.in_(possible_names))
    
    users = session.scalars(stmt).all()


    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)









    ## ****************  .between()  OPERATION ****************


    stmt = select(User).where(User.age.between(25, 99))

    users = session.scalars(stmt).all()



    print(f'Users: {len(users)}')

    for user in users:
        print(user.id, user.name, user.age)










except SQLAlchemyError as e:

    session.rollback()         

    print(f"Database error: {e}")


finally:

    session.close()