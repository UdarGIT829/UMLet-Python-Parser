from typing import List, Tuple
from enum import Enum

class Existence(Enum):
    ACTIVE = 1
    INACTIVE = 2
    UNKNOWN = 3

class action:
    pass

class entity:
    """
    The base class for anything with a health bar
    """
    _HP     : int
    name    : str
    def __init__(self):
        """
        Set all of the class attributes except for current HP
        """
        self.name = "myNameIs"
    def getName(self)->str:
        return self.name
    def setName(self, newName:str)->None:
        self.name = newName

class creature(thing):
    """
    Based on object, this will be any object that can take actions
    """
    monster_type : str
    def attack(self)->action:
        print("Do attack")

class thing(entity):
    """
    Based on Entity, this will be any Entity that has mass, size, and composition
    """
    object_composition : str
    mass : int
    size : int
    owner: str
    existence: Existence

class location():
    """
    This class will store data about a location, this includes a reference to all entities that are in it and what location they are at in 3 dimensions.
    """
    _location_info : str
    name           : str
    myEntities     : List[entity]

    def getIntersections()->List:
        return list()
    def getEntity(self)->List[entity]:
        return self.myEntities