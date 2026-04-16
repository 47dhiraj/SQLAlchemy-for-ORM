from sqlalchemy import create_engine, text






engine = create_engine("sqlite:///connection.db", echo=False)
## engine = create_engine("sqlite:///connection.db", echo=True)







## --- Phase 1: Data SEEDING ---



## using engine.begin() becoz it provides a transaction context with automatic COMMIT/ROLLBACK
with engine.begin() as conn:


    ## 1. Table Creation

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            salary INTEGER
        )
    """))


    ## 2. Data Insertion

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










## --- Phase 2: Data Retrieval ---


with engine.connect() as conn:

    result = conn.execute(text("SELECT * FROM users"))
    records = result.all()

    print(type(records), f"\n{records}\n")
    ## OUTPUT: [(1, 'Alice', 120000), (2, 'Bob', 75000), (3, 'Charlie', 95000)]

    
    ## To access particular row/record object of a list using for loop
    for row in records:

        # print(type(row))
        print(f"ID: {row.id} | Name: {row.name} | Salary: {row.salary}")




