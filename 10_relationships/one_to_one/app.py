from database import get_session             

from models import User, UserProfile

from sqlalchemy import select, func, or_, and_, not_

from sqlalchemy.exc import SQLAlchemyError




session = get_session()





try:

    user_count = session.scalar(select(func.count(User.id)))

    if user_count < 1:

        user = User(
            name="John Doe",
            age=29,
            email="johndoe@gmail.com",
            password_hash="john_doe_123"
        )
        
        profile = UserProfile(
            bio="Once I'm done, u won't see me around for a while",
            avatar_url="https://avatars.githubusercontent.com/u/47978673"
        )

        
        session.add(user)           

        user.profile = profile    

        session.commit()            
        
        # print(f"User {user.name} with bio '{profile.bio}' created.")
    
    else:
        print(f"Database already contains {user_count} user(s). Skipping initialization.")


except SQLAlchemyError as e:

    session.rollback()          
    print(f"Database error: {e}")
    
finally:
    session.close()






try:

    stmt = select(User).where(User.name == "John Doe")
    user = session.scalar(stmt)

    print(user.name)
    print(user.age)
    print(user.email)
    print(user.password_hash)


except SQLAlchemyError as e:

    session.rollback()
    print(f"Database error: {e}")
    
finally:
    session.close()
