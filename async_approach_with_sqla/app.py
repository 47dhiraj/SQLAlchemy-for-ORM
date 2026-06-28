import asyncio
from datetime import date
from sqlalchemy import select
from database import async_engine, AsyncSessionLocal, Base, DatabaseSession
from models import User






async def seed_initial_data(db: DatabaseSession) -> None:

    try:

        stmt = select(select(User.id).exists())

        result = await db.execute(stmt)
        user_exists = result.scalar()


        if user_exists:
            print("\n[Seed Skipped] Database already contains user records.\n")
            return


        new_user = User(
            username="johndoe",
            email="john@example.com",
            password="secure_hashed_password_here",
            dob=date(2000, 1, 21),
            address={"street": "456789", "city": "Parallel Universe", "zip": "00000"}
        )


        db.add(new_user)
        await db.commit()

        print("\n[Transaction Success] User seeded successfully.\n")



    except Exception as error:

        print(f"\n[Transaction Error] Exception caught. Executing manual rollback: {error}\n")

        await db.rollback()
        raise error











async def fetch_user_by_username(db: DatabaseSession, username: str) -> User | None:

    stmt = select(User).where(User.username == username)
    

    try:

        result = await db.execute(stmt)

        return result.scalars().first()
        

    except Exception as error:

        print(f"\n[Read Error] Query failed. Executing manual rollback: {error}\n")

        await db.rollback()

        raise error











async def main():

    async with async_engine.begin() as conn:
        
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)                  



    async with AsyncSessionLocal() as session:
        await seed_initial_data(session)



    async with AsyncSessionLocal() as session:
        user = await fetch_user_by_username(session, "johndoe")



    if user:
        print(f"\n[Production Read] User Found: {user.username} | Email: {user.email}\n")

    else:
        print("\n[Production Read] User not found.\n")









if __name__ == "__main__":

    asyncio.run(main())

