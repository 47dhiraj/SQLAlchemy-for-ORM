from database import get_session                

from models import User, SensitiveInformation

from sqlalchemy import select, func

from sqlalchemy.orm import raiseload

from sqlalchemy.exc import SQLAlchemyError

from time import perf_counter





session = get_session()




try:

    user_count = session.scalar(select(func.count()).select_from(User))


    if user_count < 1:

        users_to_add = [
            User(
                name=f'\nUser: {y+1}',
                sensitive_information=[SensitiveInformation(content=f'Sensitive content: {x+1}') for x in range(2)]
            ) for y in range(1_000)
        ]
    
        session.add_all(users_to_add)
        session.commit()



    

    stmt = select(User)
    users = session.scalars(stmt).all()



    
    

    
    



    start = perf_counter()


    for user in users:
        print(user.name)

        try:
            for information in user.sensitive_information:
                print(information.content)

        except Exception as e:
            print('Cannot access, sensetive info: ', e)



    print(f'Done in: {perf_counter() - start}')






except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")



finally:
    session.close()
