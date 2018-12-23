from screen import Screen
import sys
import random
import math
from ship import *
from asteroid import *
from torpedo import *

DEFUALT_CLASS_SETTING=0
SPECIAL_MOVE_DEGREE_CHANGE=45
SPECIAL_MOVE_MIN=2
DEFAULT_ASTEROIDS_NUM = 5
STARTING_SCORE = 0
STARTING_DIRECTION = 0
STARTING_SPEED = 0
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 4
ASTEROID_STARTING_SIZE = 3
ASTEROID_MID_SIZE = 2
ASTEROID_MIN_SIZE = 1
BIG_ASTEROID_POINTS = 20
MID_ASTEROID_POINTS = 50
SMALL_ASTEROID_POINTS = 100
MAX_TORPEDO_NUM = 10
TORPEDO_LIFETIME_MAX = 200
CHANGE_DEGREE=7
HIT_TITLE = "You were hit!"
HIT_MSG = "You have lost 1 life"
END_TITLE = "End of game"
WON_MSG = "YOU WON! \n I knew you could do it!"
LOST_MSG = "YOU LOST \n better luck next time"
QUIT_MSG = "YOU QUIT \n boo you"


class GameRunner:

    def __init__(self, asteroids_amount):
        """
        this function will create the settings for a single game
        :param asteroids_amount: int - the amount of initial asteroids
        """
        self.__screen = Screen()#todo not to touch
        self.__screen_max_x = Screen.SCREEN_MAX_X#todo not to touch
        self.__screen_max_y = Screen.SCREEN_MAX_Y#todo not to touch
        self.__screen_min_x = Screen.SCREEN_MIN_X#todo not to touch
        self.__screen_min_y = Screen.SCREEN_MIN_Y#todo not to touch
        self.__delta_x_screen = self.__screen_max_x - self.__screen_min_x
        self.__delta_y_screen = self.__screen_max_y - self.__screen_min_y
        self.__score = STARTING_SCORE

        # ---------------create ship-----------------------------
        self.__ship = self.create_ship()

        # ---------------create asteroids------------------------
        self.__asteroids_amount = asteroids_amount
        self.asteroids_list = self.create_asteroids(asteroids_amount)

        # ----------------create torpedo list -------------------
        self.torpedo_list = []

    def create_asteroids(self, asteroids_amount):#to check if the else is okay
        """
        this function will create all the initial asteroids for te game
        :param asteroids_amount: int - how many asteroids
        :return: a list off registered asteroids
        """
        asteroids_list = []
        for i in range(asteroids_amount):
            asteroid = self.create_one_asteroid()
            if not asteroid.has_intersection(self.__ship):
                # it has no intersection with the ship
                asteroids_list.append(asteroid)
            else:
                # we will create a different asteroid instead
                asteroids_amount += 1
        for asteroid in asteroids_list:
            self.__screen.register_asteroid(asteroid, asteroid.get_size())
        return asteroids_list

    def create_one_asteroid(self):
        """
        this function will create a single asteroid.
        :return: an asteroid object
        """
        asteroid_x_loc = random.randint(self.__screen_min_x, self.__screen_max_x)
        asteroid_y_loc = random.randint(self.__screen_min_y, self.__screen_max_y)
        asteroid_x_speed = random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        asteroid_y_speed = random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        asteroid_size = ASTEROID_STARTING_SIZE
        asteroid = Asteroid((asteroid_x_loc, asteroid_y_loc),
                            (asteroid_x_speed, asteroid_y_speed), asteroid_size)
        return asteroid

    def create_ship(self):
        """
        this function will create the ship for the game
        :return: a ship object
        """
        ship_x_loc = random.randint(self.__screen_min_x, self.__screen_max_x)
        ship_y_loc = random.randint(self.__screen_min_y, self.__screen_max_y)
        starting_dir = STARTING_DIRECTION
        starting_speed = STARTING_SPEED
        ship = Ship((ship_x_loc, ship_y_loc), starting_speed, starting_dir)
        return ship

    def move_object(self, obj):
        """
        This method will work for every type of object in the game.
        :param obj: an object - ship, asteroid or torpedo
        sets a new location for the obj:
           a tuple for new location - (new_x_cord, new_y_cord)
        """
        object_speed = obj.get_speed()
        # returns a tuple (x_speed, y_speed)
        object_location = obj.get_location()
        # returns a tuple (x_loc, y_loc)
        new_x_cord = ((object_speed[0] + object_location[0] - self.__screen_min_x)
                      % self.__delta_x_screen + self.__screen_min_x)
        new_y_cord = ((object_speed[1] + object_location[1] - self.__screen_min_y)
                      % self.__delta_y_screen + self.__screen_min_y)
        obj.set_location(new_x_cord, new_y_cord)

    def run(self):#todo not to touch
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):#todo not to touch
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # ----------------draw objects---------------------
        self.__screen.draw_ship(*self.__ship.get_location(),
                           self.__ship.get_direction())

        for asteroid in self.asteroids_list:
            self.__screen.draw_asteroid(asteroid, *asteroid.get_location())

        for torpedo in self.torpedo_list:
            self.__screen.draw_torpedo(torpedo, *torpedo.get_location(),
                           torpedo.get_direction())

        # ------------------move objects------------------------

        # ----------------ship------------------
        if self.__screen.is_right_pressed():
            self.__ship.set_direction(- CHANGE_DEGREE)
        if self.__screen.is_left_pressed():
            self.__ship.set_direction(CHANGE_DEGREE)
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        self.move_object(self.__ship)

        # -----------------asteroids-------------
        for asteroid in self.asteroids_list:
            self.update_asteroid(asteroid)

        # -----------------torpedoes-------------
        if self.__screen.is_space_pressed():
            if len(self.torpedo_list) < MAX_TORPEDO_NUM:
                torpedo = self.create_torpedo()
                self.torpedo_list.append(torpedo)
        for torpedo in self.torpedo_list:
            self.torpedo_update(torpedo)

        # -------------------ending----------------------------

        #--------------------check for teleport----------------

        if self.__screen.is_teleport_pressed():
            self.teleport()

        #--------------------special move----------------------
        if self.__screen.is_special_pressed():
            self.special_move()
        #--------------------ending----------------------

        self.check_ending()

    def special_move(self):
       """
        this function makes the ship shoot 8 torpedos that are 45 degrees apart
        from each other.starting from the same location
       :return:
       """
       if len(self.torpedo_list)<=SPECIAL_MOVE_MIN:
           for i in range(8):#todo make 8 constant
               self.__ship.set_direction(SPECIAL_MOVE_DEGREE_CHANGE)

               torpedo = self.create_torpedo()
               self.torpedo_list.append(torpedo)


           for torpedo in self.torpedo_list:
               self.torpedo_update(torpedo)




    def teleport(self):
        """
        this function teleports the ship to a new random location that doesnt
        collide with any astroid
        :return:
        """
        teleport_x_loc,teleport_y_loc=0,0
        while True:
            teleport_x_loc = random.randint(self.__screen_min_x,
                         self.__screen_max_x)
            teleport_y_loc = random.randint(self.__screen_min_y,
                         self.__screen_max_y)
            ship_check=Ship((teleport_x_loc,teleport_y_loc), 
                DEFUALT_CLASS_SETTING,DEFUALT_CLASS_SETTING)
            for i in self.asteroids_list:
                if i.has_intersection(ship_check):
                    break
            else:
                break
        self.__ship.set_location(teleport_x_loc,teleport_y_loc)



    def check_ending(self):
        """
        this function will check if the game should end and end it if it
        should. It will also print an informative message.
        """
        is_exit = False
        if self.__ship.get_lives() == 0:
            self.__screen.show_message(END_TITLE, LOST_MSG)
            is_exit = True
        elif self.asteroids_list == []:
            self.__screen.show_message(END_TITLE, WON_MSG)
            is_exit = True
        elif self.__screen.should_end():
            self.__screen.show_message(END_TITLE, QUIT_MSG)
            is_exit = True
        if is_exit:
            self.__screen.end_game()
            sys.exit()

    def update_asteroid(self, asteroid):
        """
        this function will update the status of an asteroid. it will move it,
        check if it intersects with the ship and torpedoes and adjust it
        accordingly.
        :param asteroid: an asteroid object
        """
        self.move_object(asteroid)
        if asteroid.has_intersection(self.__ship):
            self.ship_asteroid_intersection(asteroid)
        for torpedo in self.torpedo_list:
            if asteroid.has_intersection(torpedo):
                self.torpedo_asteroid_intersection(torpedo, asteroid)

    def torpedo_update(self, torpedo):
        """
        this function will handle a torpedo. it will check its lifetime,
        update it and move the torpedo. if the lifetime is over the limit
        it will remove the torpedo.
        :param torpedo: a torpedo object
        """
        if torpedo.get_lifetime() < TORPEDO_LIFETIME_MAX:
            torpedo.set_lifetime()
            self.move_object(torpedo)
        else:
            self.__screen.unregister_torpedo(torpedo)
            self.torpedo_list.remove(torpedo)

    def ship_asteroid_intersection(self, asteroid):
        """
        this function handles a ship - asteroid intersection
        :param asteroid: an asteroid object that hit the ship
        removes lives from the ship. deletes the hit asteroid.
        """
        self.__ship.set_lives()
        self.__screen.show_message(HIT_TITLE, HIT_MSG)
        self.__screen.remove_life()
        self.__screen.unregister_asteroid(asteroid)
        self.asteroids_list.remove(asteroid)

    def create_torpedo(self):
        """
        this function creates one torpedo.
        :return: a torpedo object
        """
        location = self.__ship.get_location()
        direction = self.__ship.get_direction()
        x_speed = self.__ship.get_speed()[0] + 2 * math.cos(
            math.radians(direction))
        y_speed = self.__ship.get_speed()[1] + 2 * math.sin(
            math.radians(direction))
        torpedo = Torpedo(location, (x_speed, y_speed), direction)
        self.__screen.register_torpedo(torpedo)
        return torpedo

    def torpedo_asteroid_intersection(self, torpedo, asteroid):
        """
        this function works the intersection between a torpedo and an asteroid.
        :param torpedo: a torpedo object
        :param asteroid: an asteroid object
        the function will add the correct score and split or earse the asteroid
        """
        if asteroid.get_size() == ASTEROID_STARTING_SIZE:
            self.__score += BIG_ASTEROID_POINTS
            self.split_asteroid(asteroid, torpedo)
        elif asteroid.get_size() == ASTEROID_MID_SIZE:
            self.__score += MID_ASTEROID_POINTS
            self.split_asteroid(asteroid, torpedo)
        else:
            self.__score += SMALL_ASTEROID_POINTS
            # remove the asteroid
            self.__screen.unregister_asteroid(asteroid)
            self.asteroids_list.remove(asteroid)

        print(len(self.asteroids_list))#todo remove this
        self.__screen.set_score(self.__score)

        # ------------remove the torpedo-------------
        self.__screen.unregister_torpedo(torpedo)
        self.torpedo_list.remove(torpedo)

    def split_asteroid(self, asteroid, torpedo):
        """
        this function will split a hit asteroid.
        :param asteroid: an asteroid object
        :param torpedo: a torpedo object (that hit the asteroid)
        :return:
        """
        asteroid_location = asteroid.get_location()
        asteroid_speed = asteroid.get_speed()
        torpedo_speed = torpedo.get_speed()
        new_x_speed = (torpedo_speed[0] + asteroid_speed[0]) / math.sqrt(
            (asteroid_speed[0])**2 + (asteroid_speed[1])**2)
        new_y_speed = (torpedo_speed[1] + asteroid_speed[1]) / math.sqrt(
            (asteroid_speed[0])**2 + (asteroid_speed[1])**2)
        new_size = asteroid.get_size() - 1

        # -------------------create two new asteroids---------------------
        asteroid1 = Asteroid(asteroid_location,
                             (new_x_speed, new_y_speed), new_size)
        asteroid2 = Asteroid(asteroid_location,
                             ((new_x_speed*(-1)), (new_y_speed*(-1))),
                             new_size)
        self.__screen.register_asteroid(asteroid1, new_size)
        self.__screen.register_asteroid(asteroid2, new_size)
        self.asteroids_list.extend([asteroid1, asteroid2])

        # --------------------delete former asteroid-----------------------
        self.__screen.unregister_asteroid(asteroid)
        self.asteroids_list.remove(asteroid)




def main(amount): #todo not to touch
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
