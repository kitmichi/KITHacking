def delete_database():
    import psycopg2
    from psycopg2 import sql

    # Connect to the default database
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="my_password",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True

    # Create a cursor object
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('mydatabase',))
    exists = cursor.fetchone()

    # Drop the database if it exists
    if exists:
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier('mydatabase')))
        print("Database deleted successfully!")
    else:
        print("Database does not exist.")

    # Close the cursor and connection
    cursor.close()
    conn.close()

def create_database():
    import psycopg2
    from psycopg2 import sql

    # Connect to the default database
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="my_password",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True

    # Create a cursor object
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('mydatabase',))
    exists = cursor.fetchone()

    # Create the new database if it does not exist
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('mydatabase')))
        print("Database created successfully!")
    else:
        print("Database already exists.")

    # Close the cursor and connection
    cursor.close()
    conn.close()

# SQLAlchemy part
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database connection with port 5432
engine = create_engine('postgresql+psycopg2://postgres:my_password@localhost:5432/mydatabase')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

def get_all_users():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the database
    return session.query(User).all()    

def create_user():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert data
    new_user = User(name='Charlie', age=35)
    session.add(new_user)
    session.commit()

    # Query the database
    return session.query(User).all()

def test_postgres_running():
	delete_database()
	create_database()
	actual = get_all_users()
	assert len(actual) == 0
	actual = create_user()
	assert len(actual) == 1