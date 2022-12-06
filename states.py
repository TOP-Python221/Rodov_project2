from __future__ import annotations
# импорт из стандартной библиотеки
import datetime
from datetime import datetime as dt
from dataclasses import dataclass
import json

# импорт дополнительных модулей
import creature
import constants


# saves = {
#     'health': ((1, 2), (3, 9), (10, 16), (17, 20),),
#     'stamina': ((1, 3), (4, 10), (11, 17), (18, 20),),
#     'hunger': ((1), (1), (1), (1),),
#     'thirst': ((1), (1), (1), (1),),
#
# }


class Ranges:
    def __init__(self,
                 health: 'ParamRanges',
                 stamina: 'ParamRanges',
                 hunger: 'ParamRanges',
                 thirst: 'ParamRanges',
                 ):
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst


class KindParameters:
    def __init__(self,
                 title: str,
                 maturity: tuple,
                 egg: Ranges,
                 cub: Ranges,
                 yong: Ranges,
                 adult: Ranges,
                 elder: Ranges):
        self.title = title
        self.maturity = maturity
        self.egg = egg
        self.cub = cub
        self.yong = yong
        self.adult = adult
        self.elder = elder

    def age_ranges(self) -> Ranges:
        pass


class BodyState:
    def __init__(self,
                 timestamp: dt,
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int,
                 intestine: int):
        self.timestamp = timestamp
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst
        self.intestine = intestine

    def to_dict(self) -> dict:
        self.timestamp = dt
        self.health = 'health'
        self.stamina = 'stamina'
        self.hunger = 'hunger'
        self.thirst = 'thirst'
        return {self.timestamp: datetime.datetime.now(), self.health: 1, self.stamina: 2, self.hunger: 3, self.thirst: 4}


class MindState:
    def __init__(self,
                 timestamp: dt,
                 joy: int,
                 activity: float,
                 anger: int,
                 anxiety: float):
        self.anxiety = anxiety
        self.activity = activity
        self.timestamp = timestamp
        self.joy = joy
        self.anger = anger
        # self.pattern = pattern

    def to_dict(self) -> dict:
        self.timestamp = dt
        self.joy = 'joy'
        self.anger = 'anger'
        self.pattern = 'pattern'
        return {self.timestamp: datetime.datetime.now(), self.joy: 1, self.anger: 2, self.pattern: '', }


class StatesManager:
    def __init__(self,
                 kind: creature.Kind,
                 name: str,
                 birthdate: dt,
                 body_last: BodyState,
                 mind_last: MindState,
                 ):
        self.kind = kind
        self.name = name
        self.birthdate = birthdate
        self.body_last = body_last
        self.mind_last = mind_last


class StateCalculator:
    def __init__(self, last: 'StatesManager'):
        self.last = last

    def creat_creature(self,
                       kind: 'Kind',
                       name: str,
                       birhdate: dt,
                       body: creature.Body,
                       mind: creature.Mind) -> creature.Creature:
        pass

    # КОММЕНТАРИЙ: именно эти методы ответственны за вычисления новых мгновенных значений параметров после загрузки данных из файла(-ов) состояний
    def __revive_body(self) -> creature.Body:
        pass

    def __revive_mind(self) -> creature.Mind:
        pass

    def new_creature(self, revive_name, revive_birthdate):
        # from main import Creature  # Избавляет от закальцованного импорта
        self.revive_name = revive_name
        self.revive_birthdate = revive_birthdate
        return creature.Creature(revive_name, revive_birthdate, self.__revive_body(), self.__revive_mind())


# class PersistenceManager:
#     def __init__(self, default_config_path: str | 'Path'):
#         # D:\Rodov_project2\Rodov_project2\states.py
#         self.default_config_path = default_config_path
#
#     @staticmethod
#     def read_file(filename):
#         """Чтение json файлов"""
#         with open(filename, 'r', encoding='utf-8') as file:
#             load_file = json.load(file)
#             name_list = []
#             birthday_list = []
#             for value in load_file.values():
#                 name_list.append(value['name'])
#                 birthday_list.append(value['birthday'])
#             return StatesManager(main.Kind.CAT, name_list, birthday_list, '', '')
#
#     @staticmethod
#     def write_file(file_name, prop_name: str, prop_value='None'):
#         with open(file_name, "r") as file:
#             data = json.load(file)
#
#         data[prop_name] = prop_value
#
#         with open(file_name, "w") as file:
#             json.dump(data, file, indent=2)

# КОММЕНТАРИЙ: эти два класса никто не использует, им грустно и одиноко — поговорите с ними, вдруг пригодятся



class KindParameters:
    def __init__(self,
                 title: str,
                 maturity: tuple,
                 egg: Ranges,
                 cub: Ranges,
                 yong: Ranges,
                 adult: Ranges,
                 elder: Ranges):
        self.title = title
        self.maturity = maturity
        self.egg = egg
        self.cub = cub
        self.yong = yong
        self.adult = adult
        self.elder = elder

    def age_ranges(self) -> Ranges:
        pass




# тесты:
if __name__ == '__main__':
    st = StatesManager('', '', '', '', '')
    print(st)

    # pm = PersistenceManager('')
    # # pm.write_file(saves, 'property_saves.json')
    # print(pm.read_file('property_saves.json'))
