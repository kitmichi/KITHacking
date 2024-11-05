from sqlalchemy import Integer, create_engine, Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from extractor.study_schedule_extractor import get_study_schedule

import shutil
from prettytable import PrettyTable

def print_modules_nicely(modules):
    table = PrettyTable()
    table.field_names = ["Field name", "Module name", "Bricks"]
    
    # Get the current width of the console
    console_width = shutil.get_terminal_size().columns
    
    # Set the maximum width for the columns based on the console width
    max_width = console_width // 3  # Adjust the division as needed
    table.max_width["Field name"] = max_width
    table.max_width["Module name"] = max_width
    table.max_width["Bricks"] = max_width

    for module in modules:
        field_names = ', '.join([field.name for field in module.fields])
        brick_ids = ', '.join([brick.name for brick in module.bricks])
        table.add_row([field_names, module.name, brick_ids])

    print(table)


def print_fields_nicely(fields):
    table = PrettyTable()
    table.field_names = ["Field name", "Modules"]
    
    # Get the current width of the console
    console_width = shutil.get_terminal_size().columns
    
    # Set the maximum width for the columns based on the console width
    max_width = console_width // 2  # Adjust the division as needed
    table.max_width["Field name"] = max_width
    table.max_width["Modules"] = max_width

    for field in fields:
        module_ids = ', '.join([module.id_campus for module in field.modules])
        table.add_row([field.name, module_ids])

    print(table)


Base = declarative_base()

# Association table for the many-to-many relationship
module_brick_association = Table('module_brick', Base.metadata,
    Column('module_id', Integer, ForeignKey('modules.id')),
    Column('brick_id', Integer, ForeignKey('bricks.id'))
)

# Association table for the many-to-many relationship
field_module_association = Table('field_module', Base.metadata,
    Column('field_id', Integer, ForeignKey('fields.id')),
    Column('module_id', Integer, ForeignKey('modules.id'))
)

# Define the Field class
class Field(Base):
    __tablename__ = 'fields'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    CP = Column(String)
    link = Column(String)
    modules = relationship('Module', secondary=field_module_association, back_populates='fields')

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_campus = Column(String)
    name = Column(String)
    type = Column(String)
    CP = Column(String)
    link = Column(String)
    bricks = relationship('Brick', secondary=module_brick_association, back_populates='modules')
    fields = relationship('Field', secondary=field_module_association, back_populates='modules')

class Brick(Base):
    __tablename__ = 'bricks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_campus = Column(String)
    name = Column(String)
    type = Column(String)
    CP = Column(String)
    link = Column(String)
    modules = relationship('Module', secondary=module_brick_association, back_populates='bricks')

def update_study_schedule():

    # Create an engine and a session
    engine = create_engine('postgresql+psycopg2://postgres:my_password@localhost:5432/mydatabase')

    module_brick_association.drop(engine, checkfirst=True)
    field_module_association.drop(engine, checkfirst=True)
    Field.__table__.drop(engine, checkfirst=True)
    Module.__table__.drop(engine, checkfirst=True)
    Brick.__table__.drop(engine, checkfirst=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()



    import re

    # Assuming get_study_schedule() is defined elsewhere
    study_schedule = get_study_schedule()

    # Regular expression pattern to match the part before "–"
    pattern = r'^[^\s]+'

    uninteresting_parts = [
        "type",
        "CP",
        "link"
    ]

    for field_name, field_content in study_schedule['88-048-H-2018 – Elektrotechnik und Informationstechnik Master 2018'].items():
        if field_name in uninteresting_parts:
            continue
        field = Field(
            name=field_name.strip(),
            type=field_content["type"],
            CP=field_content["CP"],
            link=field_content["link"]
        )
        for module_name, module_content in field_content.items():
            if not module_name.startswith("M-"):
                continue
            
            match = re.match(pattern, module_name)
            module = Module(
                id_campus=match.group(),
                name=module_name[match.end()+3:].strip(),
                type=module_content["type"],
                CP=module_content["CP"],
                link=module_content["link"]
            )
            
            for brick_name, brick_content in module_content.items():
                if not brick_name.startswith("T-"):
                    continue
                
                match = re.match(pattern, brick_name)
                brick = Brick(
                    id_campus=match.group(),
                    name=brick_name[match.end()+3:].strip(),
                    type=brick_content["type"],
                    CP=brick_content["CP"],
                    link=brick_content["link"]
                )
                
                module.bricks.append(brick)
                brick.modules.append(module)
                session.add(brick)
            field.modules.append(module)
            module.fields.append(field)
            session.add(module)
        session.add(field)
    session.commit()
    return session
if __name__ == "__main__":
    session = update_study_schedule()
    print_modules_nicely(session.query(Module).all())
    print_fields_nicely(session.query(Field).all())