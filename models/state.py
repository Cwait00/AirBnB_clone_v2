#!/usr/bin/python3
"""This is the state class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if models.storage_type == "db":
        cities = relationship("City", cascade='all, delete, delete-orphan',
                              backref="state")
    else:
        @property
        def cities(self):
            """Returns the list of City instances with state_id equal to the current State.id"""
            all_cities = models.storage.all(City)
            return [city for city in all_cities.values() if city.state_id == self.id]
