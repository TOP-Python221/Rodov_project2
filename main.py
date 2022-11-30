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
        pass


    # @staticmethod # Статический только для тестов
    def tired(self):
        """Описывает физическое состояние питомца: устал/не устал"""
        if dt.today().strftime('%H') > '11': # Это, скорее, для тестов сделано, чтобы посмотреть как работает функции
            # модуля datetime
            return 'Ваш питомец устал'
        return 'Ваш питомец, как огурчик ;D'

    def sleep(self):
        pass


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




# тесты:
if __name__ == '__main__':
    print(dt.now().minute)
    print(datetime.time())
