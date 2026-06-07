from database import get_session

from models import User,Address

from sqlalchemy import func, select, union, or_

from sqlalchemy.exc import SQLAlchemyError





session = get_session()





try:


    user_count = session.scalar(select(func.count()).select_from(User))


    if user_count < 1:


        ram = User(username="ram", email="ram@example.com", password="ram_password")
        shyam = User(username="shyam", email="shyam@example.com", password="shyam_password")
        hari = User(username="hari", email="hari@example.com", password="hari_password")
        

        addr1 = Address(location="ktm-putalisadak", user=ram)
        addr2 = Address(location="ktm-dillibazar", user=ram)
        addr3 = Address(location="chitwan-bharatpur", user=shyam)
        addr4 = Address(location="bhaktapur-pepsicola", user=None)
        

        session.add_all([ram, shyam, hari, addr1, addr2, addr3, addr4])

        session.commit()







    ## ************************  FULL JOIN (FULL OUTER JOIN) ************************


    stmt = select(User, Address).outerjoin(User.addresses, full=True)

    result = session.execute(stmt)
    # print(result)



    print("\nFULL JOIN (FULL OUTER JOIN)")

    for user, address in result:
    
        username = user.username if user is not None else "No User"
        location = address.location if address is not None else "No Address"
        
        print(f"\nUser: {username} | Address: {location}")



    print("\n")
    ## ************************ FULL JOIN CLOSES ************************






except SQLAlchemyError as e:

    session.rollback()    

    print(f"Database error: {e}")




finally:
    
    session.close()
