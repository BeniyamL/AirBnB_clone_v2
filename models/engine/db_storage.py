#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in database"""
    __engine = None
    __session = None

    def __init__(self):
        """ method that initializes the DB storage class """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        self.reload()
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all object from the database"""
        if cls is None:
            all_objs = self.__session.query(State).all()
            all_objs.extend(self.__session.query(City).all())
            all_objs.extend(self.__session.query(User).all())
            all_objs.extend(self.__session.query(Place).all())
            all_objs.extend(self.__session.query(Review).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            all_objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in all_objs}

    def new(self, obj):
        """Adds new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes to the current database """
        self.__session.commit()

    def reload(self):
        """creates all tables in the database and create a current session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def delete(self, obj=None):
        """ method to delete from the current database session"""
        if obj is not None:
            obj.__session.delete(obj)

    def close(self):
        """ a method to close the session """
        self.__session.close()
