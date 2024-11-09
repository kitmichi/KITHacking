# SQLAlchemy part
from sqlalchemy import Column, Integer, Sequence, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from database import create_database, delete_database

# Set up the database connection with port 5432
engine = create_engine(
    "postgresql+psycopg2://postgres:my_password@localhost:5432/mydatabase"
)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
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
    new_user = User(name="Charlie", age=35)
    session.add(new_user)
    session.commit()

    # Query the database
    return session.query(User).all()


def test_postgres_running():
    delete_database.delete_database()
    create_database.create_database()
    actual = get_all_users()
    assert len(actual) == 0
    actual = create_user()
    assert len(actual) == 1
