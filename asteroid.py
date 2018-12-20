import math
class Asteroid():
    def __init__(self, location, speed, size):
        self.__x_location = location[0]
        self.__y_location = location[1]
        self.__x_speed = speed[0]
        self.__y_speed = speed[1]
        self.__size = size # int between 1-3

    def get_location(self):
        return self.__x_location, self.__y_location

    def get_direction(self):
        return self.__direction

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_size(self):
        return self.__size
    def __str__(self):
        return str(self.get_location())