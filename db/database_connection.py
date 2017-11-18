from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from database import Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///catalog.db')
else:
    engine = create_engine('sqlite:///db/catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
