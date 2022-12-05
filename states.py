from __future__ import annotations

import datetime
import pathlib
from typing import List
import main
import datetime as dt
import json

# saves = {
#     'health': ((1, 2), (3, 9), (10, 16), (17, 20),),
#     'stamina': ((1, 3), (4, 10), (11, 17), (18, 20),),
#     'hunger': ((1), (1), (1), (1),),
#     'thirst': ((1), (1), (1), (1),),
#
# }

class StateCalculator:

    def __init__(self, previous: 'StatesManager'):
        self.previous = previous

    # КОММЕНТАРИЙ: именно эти методы ответственны за вычисления новых мгновенных значений параметров после загрузки данных из файла(-ов) состояний
    def __new_body(self) -> main.Body:
        pass

    def __new_mind(self) -> main.Mind:
        pass

    def new_creature(self, new_name, new_birthdate):
        from main import Creature # Избавляет от закальцованного импорта
        self.new_name = new_name
        self.new_birthdate = new_birthdate
        return Creature(new_name, new_birthdate, self.__new_body(), self.__new_mind())


class StatesManager:
    def __init__(self,
                 kind: main.Kind,
                 name: str,
                 birthdate: dt,
                 ):
        self.kind = kind
        self.name = name
        self.birthdate = birthdate
        self.body_last = BodyState('timestamp', 1, 1, 1, 1)
        self.mind_last = MindState(1, 1, 1, 'pattern')



class PersistenceManager:
    def __init__(self, default_config_path: str | 'Path'):
        # D:\Rodov_project2\Rodov_project2\states.py
        self.default_config_path = default_config_path

    # ИСПРАВИТЬ: в этом классе мы обычно прописываем не общие методы "чтения любого файла", а вполне конкретные, например: "читать json файл состояний", "читать ini файл конфигурации" (если такой будет) и так далее
    # КОММЕНТАРИЙ: этот метод, например, должен возвращать объект StatesManager, то есть он читает именно состояния — это как раз случай, когда можно и нужно изменить модель в имени метода
    @staticmethod
    def read_file(filename):
        """Чтение json файлов"""
        with open(filename, 'r', encoding='utf-8') as file:
            load_file = json.load(file)
            name = load_file['cat']['title']
            birthday = load_file['cat']['birthday']
            return StatesManager(main.Kind.CAT, name, birthday)

    @staticmethod
    def write_file(save, filename):
        save = json.dumps(save)
        save = json.loads(str(save))
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(save, file, indent=4)

# КОММЕНТАРИЙ: эти два класса никто не использует, им грустно и одиноко — поговорите с ними, вдруг пригодятся
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


# тесты:
if __name__ == '__main__':
    st = StatesManager('', '', '')
    print(st)

    # pm = PersistenceManager('')
    # # pm.write_file(saves, 'property_saves.json')
    # print(pm.read_file('property_saves.json'))
