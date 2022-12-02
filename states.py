from __future__ import annotations

import pathlib
from typing import List
from main import Creature
import datetime as dt


class StateCalculator():
    def __init__(self, previous: 'StatesManager'):
        self.previous = previous

    def __new_body(self) -> 'Body':
        pass

    def __new_mind(self) -> 'Mind':
        pass

    def new_creature(self, new_name, new_birthdate):
        self.new_name = new_name
        self.new_birthdate  = new_birthdate
        return Creature(new_name, new_birthdate, self.__new_body(), self.__new_mind())


class StatesManager:
    def __init__(self,
                 name: str,
                 birthdate: dt,
                 body_history: List['BodyState'],
                 mind_last: 'MindState'):
        self.name = name
        self.birthdate = birthdate
        self.body_history = body_history
        self.mind_last = mind_last


class PersistenceManager:
    def __init__(self, default_config_path: str | 'Path'):
        self.default_config_path = default_config_path #D:\Rodov_project2\Rodov_project2\states.py

    def read_file(self):
        file = open('saves.txt', 'r', encoding='utf-8')
        print(file.read())
        file.close()

    def write_file(self, save):
        file = open('saves.txt', 'w')
        file.write(save)
        file.close()


class BodyState:
    def __init__(self,
                 timestamp: dt,
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int):
        self.timestamp = timestamp
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst



class MindState:
    def __init__(self,
                 timestamp: dt,
                 joy: int,
                 anger: int,
                 pattern):
        self.timestamp = timestamp
        self.joy = joy
        self.anger = anger
        self.pattern = pattern


# тесты:
if __name__ == '__main__':
    PerM = PersistenceManager('D:\Rodov_project2\Rodov_project2\states.py')
    PerM.read_file()
    PerM.write_file('check')
    PerM.read_file()

