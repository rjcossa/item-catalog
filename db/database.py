from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """
    This is a class for storing user information in the database using SQL
    Alchemy to interact with the DB
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True, nullable=False)
    picture = Column(String)
    email = Column(String)


class Category(Base):
    """
    This is a class for storing category information in the database using SQL
    Alchemy to interact with the DB
    """
    __tablename__ = 'category'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    __table_args__ = (
                        UniqueConstraint(
                                        'name',
                                        name='_account_branch_uc'),
                     )

    # JSON Serializer Function
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Item(Base):
    """
    This is a class for storing item information in the database using SQL
    Alchemy to interact with the DB
    """
    __tablename__ = 'item'

    # Fields
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String, nullable=False)
    picture = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # JSON Serializer Function
    @property
    def serialize(self):
        return {
          'id': self.id,
          'name': self.name,
          'description': self.description,
          'picture': self.picture,
          'category_id': self.category_id
         }


if __name__ == '__main__':
    engine = create_engine('sqlite:///catalog.db')
else:
    engine = create_engine('sqlite:///db/catalog.db')
Base.metadata.create_all(engine)
