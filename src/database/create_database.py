def create_database():
    import psycopg2
    from psycopg2 import sql

    # Connect to the default database
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="my_password",
        host="localhost",
        port="5432",
    )
    conn.autocommit = True

    # Create a cursor object
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ("mydatabase",))
    exists = cursor.fetchone()

    # Create the new database if it does not exist
    if not exists:
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier("mydatabase"))
        )
        print("Database created successfully!")
    else:
        print("Database already exists.")

    # Close the cursor and connection
    cursor.close()
    conn.close()
