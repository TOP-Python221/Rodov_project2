from __future__ import annotations

import datetime
import pathlib
from typing import List

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
    def __new_body(self) -> 'Body':
        pass

    def __new_mind(self) -> 'Mind':
        pass

    def new_creature(self, new_name, new_birthdate):
        from main import Creature # Избавляет от закальцованного импорта
        self.new_name = new_name
        self.new_birthdate = new_birthdate
        return Creature(new_name, new_birthdate, self.__new_body(), self.__new_mind())


class StatesManager:
    def __init__(self,
                 name: str,
                 birthdate: dt,
                 ):
        self.name = name
        self.birthdate = birthdate
        self.body_history = List[BodyState]
        self.mind_last = MindState(1, 1, 1, '')

    def append_history(self) -> List[BodyState]:
        """Читает json-файл и берёт оттуда значения"""
        file = PersistenceManager.read_file('property_saves.json')
        self.body_history = list()
        saved_history = self.body_history.append(BodyState('1',
                                                           file['health'][0],
                                                           file['stamina'][1],
                                                           file['hunger'][1],
                                                           file['thirst'][1])
                                                 )
        return saved_history

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
            l_file = json.load(file)
            return StatesManager(l_file['name'], l_file['birthday']) #TypeError: 'StatesManager' object is not subscriptable

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




# тесты:
if __name__ == '__main__':
    st = StatesManager('', '')
    print(st.append_history())

    # pm = PersistenceManager('')
    # # pm.write_file(saves, 'property_saves.json')
    # print(pm.read_file('property_saves.json'))
