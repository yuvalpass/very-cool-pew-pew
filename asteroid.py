import math
from ship import *
SIZE_COEFFICIENT = 10
NORMALIZER = 5


class Asteroid:
    """
    this class represents an asteroid in the game.
    """
    def __init__(self, location, speed, size):
        """
        :param location: a tuple (x,y)
        :param speed: a tuple (x_speed, y_speed)
        :param size: an int between 1-3
        """
        self.__x_location = location[0]
        self.__y_location = location[1]
        self.__x_speed = speed[0]
        self.__y_speed = speed[1]
        self.__size = size
        self.__radius = (self.__size*SIZE_COEFFICIENT) - NORMALIZER

    def get_location(self):
        """
        :return: tuple: (x_loc, y_loc)
        """
        return self.__x_location, self.__y_location

    def get_speed(self):
        """
        :return: tuple: (x_speed, y_speed)
        """
        return self.__x_speed, self.__y_speed

    def get_size(self):
        """
        :return: int: size between 1 and 3
        """
        return self.__size

    def set_location(self, x, y):
        """
        sets a ney location
        :param x: x_location
        :param y: y_location
        """
        self.__x_location = x
        self.__y_location = y

    def has_intersection(self, obj):
        """
        this function will check if an asteroid collides with an object
        :param obj: a ship ro a torpedo
        :return: True if collides False if doesn't
        """
        obj_location = obj.get_location()
        distance_from_obj = math.sqrt(
            (obj_location[0] - self.__x_location)**2 +
            (obj_location[1]-self.__y_location)**2)
        return True if distance_from_obj <= self.__radius + obj.get_radius() \
            else False

    def get_radius(self):
        """
        :return: int: asteroid radius
        """
        return self.__radius
