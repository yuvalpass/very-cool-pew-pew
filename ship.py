import math


class Ship:
    def __init__(self, location, speed, direction):
        self.__x_location = location[0]
        self.__y_location = location[1]
        self.__x_speed = speed * math.cos(math.radians(direction))
        self.__y_speed = speed * math.sin(math.radians(direction))
        self.__direction = direction

    def get_location(self):
        return self.__x_location, self.__y_location

    def set_location(self, x, y):
        self.__x_location = x
        self.__y_location = y

    def get_direction(self):
        return self.__direction

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def set_direction(self, degrees_change):
        self.__direction += degrees_change
        self.__direction %= 360

    def accelerate(self):
        self.__x_speed += math.cos(math.radians(self.__direction))
        self.__y_speed += math.sin(math.radians(self.__direction))

# ship1 = Ship((250,250), 0, 30)
# ship1.accelerate()
# print(ship1.get_speed())