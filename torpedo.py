import math
class Torpedo:
    def __init__(self, location, speed, direction):
        self.__x_location = location[0]
        self.__y_location = location[1]
        self.__x_speed = speed * math.cos(math.radians(direction))
        self.__y_speed = speed * math.sin(math.radians(direction))
        self.__direction = direction

    def get_location(self):
        return self.__x_location, self.__y_location

    def get_direction(self):
        return self.__direction

    def get_speed(self):
        return self.__x_speed, self.__y_speed