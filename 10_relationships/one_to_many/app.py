from database import get_session                

from models import User, Address

from sqlalchemy import select, func, or_, and_, not_

from sqlalchemy.exc import SQLAlchemyError




session = get_session()





## To insert fake initial data to database

try:

    user_count = session.scalar(select(func.count(User.id)))
    

    if user_count < 1:

        user_data = [
                    {"name": "Alice", "age": 25, "street": "123 Apple Ln", "city": "New York", "zip": 10001},
                    {"name": "Bob", "age": 30, "street": "456 Birch St", "city": "Chicago", "zip": 60601},
                    {"name": "Charlie", "age": 35, "street": "789 Cherry Dr", "city": "Austin", "zip": 73301},
                    {"name": "Diana", "age": 28, "street": "101 Dogwood Ct", "city": "Seattle", "zip": 98101},
                    {"name": "Ethan", "age": 40, "street": "202 Elm Ave", "city": "Miami", "zip": 33101},
                ]


        all_users_to_add = []

        for data in user_data:

            user = User(name=data["name"], age=data["age"])
            
            address = Address(
                street=data["street"], 
                city=data["city"], 
                state="USA",
                zip_code=data["zip"]
            )
            
            user.addresses.append(address)
            all_users_to_add.append(user)



        session.add_all(all_users_to_add)
        session.commit()


except SQLAlchemyError as e:
    session.rollback()          
    print(f"Database error: {e}")
    
finally:
    session.close()
