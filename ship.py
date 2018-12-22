import math
STARTING_LIVES = 3
SHIP_RADIUS = 1
FULL_CIRCLE_DEGREES = 360
LIVES_DECREASE = 1


class Ship:
    """
    this class represents a ship in the game.
    """
    def __init__(self, location, speed, direction):
        """
        this function will create a ship
        :param location: a tuple(x,y)
        :param speed: a tuple (x_speed, y_speed)
        :param direction: in degrees
        """
        self.__x_location = location[0]
        self.__y_location = location[1]
        self.__x_speed = speed * math.cos(math.radians(direction))
        self.__y_speed = speed * math.sin(math.radians(direction))
        self.__direction = direction
        self.__lives = STARTING_LIVES
        self.__radius = SHIP_RADIUS

    def get_location(self):
        """
        returns the location
        :return: a tuple(x,y)
        """
        return self.__x_location, self.__y_location

    def set_location(self, x, y):
        """
        sets a ney location
        :param x: x_location
        :param y: y_location
        """
        self.__x_location = x
        self.__y_location = y

    def get_direction(self):
        """
        returns the direction
        :return: float - direction
        """
        return self.__direction

    def set_direction(self, degrees_change):
        """
        changes the ship's direction
        :param degrees_change: could be positive or negative
        :return:
        """
        self.__direction += degrees_change
        self.__direction %= FULL_CIRCLE_DEGREES

    def get_speed(self):
        """
        returns the speed
        :return: a tuple (x_speed, y_speed)
        """
        return self.__x_speed, self.__y_speed

    def accelerate(self):
        """
        accelerates the ship in the direction it is on.
        changes the speed on both axises.
        """
        self.__x_speed += math.cos(math.radians(self.__direction))
        self.__y_speed += math.sin(math.radians(self.__direction))

    def get_radius(self):
        """
        :return: the ship's radius
        """
        return self.__radius

    def get_lives(self):
        """
        :return: int - how many lives does the ship have.
        """
        return self.__lives

    def set_lives(self):
        """
        decreases the amount of lives by a constant number
        """
        self.__lives -= LIVES_DECREASE
