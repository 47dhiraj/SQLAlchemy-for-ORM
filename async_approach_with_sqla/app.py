import asyncio

from database import DatabaseSession, close_db, get_db, init_db, ping_db

from models import User

from sqlalchemy import func, select






async def seed_user(db: DatabaseSession) -> User | None:

    exists_stmt = select(select(User.id).exists())

    result = await db.execute(exists_stmt)
    any_user_exists = result.scalar()


    if any_user_exists:
        print("\n[SKIPPED SEED] Database already contains records. Skipping seeding entirely.\n")
        return None


    user = User(
        username="johndoe", 
        email="johndoe@example.com", 
        full_name="John Doe"
    )

    db.add(user)
    
    await db.commit()
    await db.refresh(user)         

    print(f"\n[DATABASE SEEDED] Created initial user: {user.username} (ID: {user.id})\n")

    return user






async def get_user_by_username(db: DatabaseSession, username: str) -> User | None:
    """
        Helper function to fetch a single user by their username string.
    """

    stmt = select(User).where(User.username == username)

    result = await db.execute(stmt)

    return result.scalar_one_or_none()








async def main() -> None:


    ## checking database connection
    if not await ping_db():
        print("\n[DATABASE ERROR] Database is unreachable\n")
        return
    

    print("\n[CONNECTED TO DATABASE] Database is online. Proceeding to schema check...\n")



    ## creating schemas & tables
    await init_db()

    print("\n[SCHEMAS & TABLES Created] Database schemas and tables are synchronized.\n")



    ## Seeding the database
    async with get_db() as db:
        await seed_user(db)



    ## retreiving/fetching user
    async with get_db() as db:
        user = await get_user_by_username(db, "johndoe")
        
        if user:
            print(f"[main] Verified user in DB: {user.username} (Created: {user.created_at})")



    ## cleans up the global connection pool sockets completely just before exit or before end of the script
    await close_db()













if __name__ == "__main__":

    asyncio.run(main())
