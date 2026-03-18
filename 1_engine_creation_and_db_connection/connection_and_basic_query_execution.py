from sqlalchemy import create_engine, text


engine = create_engine("sqlite:///connection.db", echo=False)

# engine = create_engine("sqlite:///connection.db", echo=True)





# --- PHASE 1: Data Definition Language(DDL) & Data SEEDING ---



# using engine.begin() becoz it provides a transaction context with automatic COMMIT/ROLLBACK


with engine.begin() as conn:


    ## 1. TABLE CREATION


    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            salary INTEGER
        )
    """))


    ## 2. DATA INSERTION

    stmt_insert = text("INSERT OR IGNORE INTO users (id, name, salary) VALUES (:id, :name, :salary)")


    data = [
        {"id": 1, "name": "Alice", "salary": 120000},
        {"id": 2, "name": "Bob", "salary": 75000},
        {"id": 3, "name": "Charlie", "salary": 95000},
    ]

    # We pass the list of dicts directly. SQLAlchemy handles the batching.

    result = conn.execute(stmt_insert, data)

    if result.rowcount != 0:
        # Verification using rowcount (The standard engineering approach)
        print(f"\nData insertion complete.\nRows affected: {result.rowcount}\n")










# --- PHASE 2: DATA RETRIEVAL (The "Seperately see results" phase) ---


# We use engine.connect() for basic DML (Data Manipulation) operations.




with engine.connect() as conn:



    ## using --> result.all()

    # result = conn.execute(text("SELECT id, name, salary FROM users"))

    result = conn.execute(text("SELECT * FROM users"))
    records = result.all()

    # print(type(records), f"\n{records}\n")
    # ## OUTPUT: [(1, 'Alice', 120000), (2, 'Bob', 75000), (3, 'Charlie', 95000)]

    
    # ## To access particular row/record object of a list using for loop
    # for row in records:
    #     # print(type(row))
    #     # Access by each column or field name 
    #     print(f"ID: {row.id} | Name: {row.name} | Salary: {row.salary}")


    # print("\n\n")





    ## using --> result.mappings().all()

    result = conn.execute(text("SELECT * FROM users"))
    records = result.mappings().all()

    # print(type(records), f"\n{records}\n")
    # ## OUTPUT: [{'id': 1, 'name': 'Alice', 'salary': 120000}, {'id': 2, 'name': 'Bob', 'salary': 75000}, {'id': 3, 'name': 'Charlie', 'salary': 95000}]
    

    # ## For accessing each sqlalchemy RowMapping objects
    # for row in records:
    #     # print(type(row))
    #     # Use the keys or field name ('id', 'name', 'salary') to access data separately
    #     user_id = row['id']
    #     user_name = row['name']
    #     user_salary = row['salary']
    #     print(f"ID: {user_id} | Name: {user_name} | Salary: {user_salary}")


    # print("\n\n")







    ## using --> result.scalars().all()

    result = conn.execute(text("SELECT * FROM users"))
    first_column = result.scalars().all()

    # print(first_column)                   ## OUTPUT: [1, 2, 3]


    stmt = text("SELECT name FROM users")
    names = conn.execute(stmt).scalars().all()
    
    # print(names)                          ## OUTPUT: ['Alice', 'Bob', 'Charlie']



    stmt = text("SELECT salary FROM users")
    salaries = conn.execute(stmt).scalars().all()
    
    # print(salaries)                       ## OUTPUT: [120000, 75000, 95000]


    # print("\n\n")






    ## using -->  result.scalar_one()


    ## .scalar_one() only gives the single value result after unwrapping
    ## Best for single-value aggregates (Count, Sum, Avg, Max, Min)
    ## It always returns a single raw value (no data structure or rows/records)

    stmt = text("SELECT count(*) FROM users")

    rows_count = conn.execute(stmt).scalar_one()

    # print(f"\n Total rows count: {rows_count}\n")



    stmt = text("SELECT sum(salary) FROM users")

    total = conn.execute(stmt).scalar_one()

    # print(f"\n Total Salary: {total}\n")



    stmt = text("SELECT avg(salary) FROM users")

    average = conn.execute(stmt).scalar_one()

    # print(f"\n Average Salary: {average}\n")



    stmt = text("SELECT max(salary) FROM users")

    max_salary = conn.execute(stmt).scalar_one()

    # print(f"\n Maximum Salary: {max_salary}\n")



    stmt = text("SELECT min(salary) FROM users")

    max_salary = conn.execute(stmt).scalar_one()

    # print(f"\n Minimum Salary: {max_salary}\n")


    # print("\n\n")








    # using --> Direct Iteration (Stream)

    # Most memory-efficient for large datasets or data enginnering operations like ETL, Data cleaning etc


    result = conn.execute(text("SELECT * FROM users"))

    for row in result:
        print(f"- {row.name} earns {row.salary}")




    result = conn.execute(text("SELECT name, salary FROM users WHERE salary > 80000"))

    for row in result.mappings():
        print(f"- {row['name']} earns {row['salary']}")



    