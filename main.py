import time
from datetime import datetime as dt
import datetime
from abc import ABC, abstractmethod
from enum import Enum
from time import perf_counter as pc

class Kind(Enum):
    CAT = 1
    DOG = 2
    FOX = 3
    BEAR = 4
    SNAKE = 5
    LIZARD = 6
    TURTLE = 7
    # ...


class Body:
    def __init__(self,
                 health_ranges: 'ParamRanges',
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int):
        self.health_ranges = health_ranges
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst

    def tick_changes(self) -> dict:
        """Время изменения свойств существа."""
        if game_loop(): # Если запущен игровой цикл, то высчитываем отсутствие нас количества часов
            start = str(dt.now().hour)
            end_r = open('saves.txt', 'r')
            for _ in end_r:
                if 'end_of_game = ' not in end_r.readline():
                    end_r.readline()
                else:
                    end = int(end_r.read(-1))
                    average = end - int(start)
                    self.stamina -= average
                    self.hunger += average
                    self.thirst += average
            time.sleep(900) # Знаю, что пока не пройдёт сие количество секунд, то приложение, по сути, не работает.
            # Пока не имею понятия на данном этапе, как можно реализовать то, что от меня требуется :). Поэтому пока
            # протоптываю дорожку, чтобы дальше по ней можно было уложить асфальт.
            self.stamina -= 1
            self.hunger += 2
            self.thirst += 2
        else:
            end = str(dt.now().hour)
            file = open('saves.txt', 'a+')
            file.write("end_of_game = " + end + '\n')
            file.close()


class Creature():
    def __init__(self, name: str,
                 birthdate: dt,
                 body: 'Body',
                 mind: 'Mind'):
        self.name = name
        self.__birthdate = birthdate
        self.body = Body('health_ranges', 1, 1, 3, 3)
        self.mind = Mind('patterns', 2, 3)

    @property
    def age(self) -> datetime.timedelta:
        return (dt.now() - self.__birthdate)

    def feed(self, food_amount: int):
        self.body.hunger -= food_amount
        self.mind.anger -= food_amount

    def play(self, enjoy_amount: int):
        self.body.stamina -= enjoy_amount
        self.mind.joy += enjoy_amount
        self.mind.anger -= enjoy_amount

    def talk(self, conver_amount):
        self.mind.anger += conver_amount
        self.mind.joy += conver_amount


class Mind:
    def __init__(self,
                 patterns: dict,
                 joy: int,
                 anger: int):
        self.patterns = patterns
        self.joy = joy
        self.anger = anger

    @property
    def pattern(self):
        pass


def game_loop():
    return False


# тесты:
if __name__ == '__main__':
    ex = Body(1, 1, 1, 1, 1)
    ex.tick_changes()

