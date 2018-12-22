TORPEDO_RADIUS = 4
STARTING_LIFETIME = 0
LIFETIME_INCREASE_RATE = 1


class Torpedo:
    """
    this class represents a torpedo in the game
    """
    def __init__(self, location, speed, direction):
        """
        this function will create a torpedo
        :param location: a tuple(x,y)
        :param speed: a tuple (x_speed, y_speed)
        :param direction: in degrees
        """
        self.__x_location = location[0]
        self.__y_location = location[1]
        self.__x_speed = speed[0]
        self.__y_speed = speed[1]
        self.__direction = direction
        self.__radius = TORPEDO_RADIUS
        self.__lifetime = STARTING_LIFETIME

    def get_location(self):
        """
        returns the location
        :return: a tuple(x,y)
        """
        return self.__x_location, self.__y_location

    def get_direction(self):
        """
        returns the direction in degrees
        :return: float between 1-360
        """
        return self.__direction

    def get_speed(self):
        """
        returns the speed
        :return: tuple (x_speed, y_speed)
        """
        return self.__x_speed, self.__y_speed

    def set_location(self, x, y):
        """
        sets a new location
        :param x: x_location
        :param y: y_location
        :return:
        """
        self.__x_location = x
        self.__y_location = y

    def get_radius(self):
        """
        returns the radius
        :return: int - radius
        """
        return self.__radius

    def get_lifetime(self):
        """
        returns the torpedo lifetime
        :return: int - lifetime
        """
        return self.__lifetime

    def set_lifetime(self):
        """
        increases the lifetime by 1
        """
        self.__lifetime += LIFETIME_INCREASE_RATE
