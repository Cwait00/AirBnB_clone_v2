#!/usr/bin/python3

from models.base_model import BaseModel, Base
from models.city import City
import models

class State(BaseModel, Base):
    """
    State class for AirBnB project.
    """
    if models.storage_type != 'db':
        @property
        def cities(self):
            """
            Getter method to return the list of City objects
            from storage linked to the current State.
            """
            from models import storage
            city_objs = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_objs.append(city)
            return city_objs
