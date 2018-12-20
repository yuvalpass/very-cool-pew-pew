from screen import Screen
import sys
import random
from ship import *
from asteroid import *

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()#todo not to touch
        self.__screen_max_x = Screen.SCREEN_MAX_X#todo not to touch
        self.__screen_max_y = Screen.SCREEN_MAX_Y#todo not to touch
        self.__screen_min_x = Screen.SCREEN_MIN_X#todo not to touch
        self.__screen_min_y = Screen.SCREEN_MIN_Y#todo not to touch
        self.__delta_x_screen = self.__screen_max_x - self.__screen_min_x
        self.__delta_y_screen = self.__screen_max_y - self.__screen_min_y
        #---------------create ship-----------------
        ship_params = self.create_ship()
        self.__ship = Ship(*ship_params)

        #---------------end create ship-----------------
        self.__asteroids_amount = asteroids_amount
        self.asteroids_list = []


        print(self.__screen_min_x,self.__screen_max_x)
        for i in range(asteroids_amount):
            asteroid_params = self.create_one_asteroid()
            self.asteroids_list.append(Asteroid(*asteroid_params))
        self.registered_asteroids = []
        for asteroid in self.asteroids_list:
            self.registered_asteroids.append(self.__screen.register_asteroid(asteroid, asteroid.get_size()))



    def create_one_asteroid(self): #todo to check if colaids with the ship
        asteroid_x_loc = random.randint(self.__screen_min_x, self.__screen_max_x)
        asteroid_y_loc = random.randint(self.__screen_min_y, self.__screen_max_y)
        asteroid_x_speed = random.randint(1, 4)
        asteroid_y_speed = random.randint(1, 4)
        asteroid_size=3#todo i got some magic in me
        #
        #add check part d mission 2


        return (asteroid_x_loc, asteroid_y_loc), (asteroid_x_speed, asteroid_y_speed), asteroid_size

    def create_ship(self):
        ship_x_loc = random.randint(self.__screen_min_x, self.__screen_max_x)
        ship_y_loc = random.randint(self.__screen_min_y, self.__screen_max_y)
        starting_dir = 0 #todo magic num
        starting_speed = 0
        return (ship_x_loc, ship_y_loc), starting_speed, starting_dir

    def move_object(self, object):
        """
        This method will work for every type of object in the game.
        :param object:
        :return: (new_x_cord, new_y_cord)
        """
        object_speed = object.get_speed() #returns a tuple (x_speed, y_speed)
        object_location = object.get_location() #returns a tuple (x_loc, y_loc)
        new_x_cord = ((object_speed[0] + object_location[0] - self.__screen_min_x)
                      % self.__delta_x_screen + self.__screen_min_x)
        new_y_cord = ((object_speed[1] + object_location[1] - self.__screen_min_y)
                      % self.__delta_y_screen + self.__screen_min_y)
        self.__ship.set_location(new_x_cord, new_y_cord)

    def rotate_ship(self):
        """
        for later ,part B  mission  3
        :return:
        """

    def run(self):#todo not to touch
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):#todo not to touch
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):#todo not to touch
        Screen.draw_ship(self.__screen, *self.__ship.get_location(),
                         self.__ship.get_direction())

        count=0
        for asteroid in self.registered_asteroids:

            Screen.draw_asteroid = (self.__screen, asteroid, *self.asteroids_list[count].get_location())
            count+=1


        if self.__screen.is_right_pressed():
            self.__ship.set_direction(-7)
        if self.__screen.is_left_pressed():
            self.__ship.set_direction(7)
        if self.__screen.is_up_pressed():

            self.__ship.accelerate()

        self.move_object(self.__ship)


def main(amount):#todo not to touch
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
