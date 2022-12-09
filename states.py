# импорт из стандартной библиотеки
from __future__ import annotations
import datetime
from datetime import datetime as dt
from dataclasses import dataclass
import json

# импорт дополнительных модулей
import creature
import constants


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
        # self.timestamp = datetime.datetime.timestamp()
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst
        self.intestine = intestine

    def to_dict(self):
        body_dictionary = {'timestamp': self.timestamp,
                      'health': self.health,
                      'stamina': self.stamina,
                      'hunger': self.hunger,
                      'thirst': self.thirst,
                      'intestine': self.intestine}
        return body_dictionary


class MindState:
    def __init__(self,
                 timestamp: dt,
                 joy: int,
                 activity: float,
                 anger: int,
                 anxiety: float):
        self.anxiety = anxiety
        self.activity = activity
        # self.timestamp = datetime.datetime.timestamp()
        self.joy = joy
        self.anger = anger
        # self.pattern = pattern

    def to_dict(self):
        mind_dictionary = {'timestamp': self.timestamp,
                      'joy': self.joy,
                      'activity': self.activity,
                      'anger': self.anger,
                      'anxiety': self.anxiety}
        return mind_dictionary


class StatesManager:
    def __init__(self,
                 kind: constants.Kind,
                 name: str,
                 birthdate: dt,
                 mind_last: MindState,
                 body_last: BodyState):
        self.kind = kind
        self.name = name
        self.birthdate = birthdate
        self.body_last = body_last
        self.mind_last = mind_last

    def to_dict(self):
        dictionary = {'kind': self.kind,
                      'name': self.name,
                      'birthdate': self.birthdate,
                      'body_last': self.body_last,
                      'mind_last': self.mind_last}
        return dictionary


import data # Избавляет от 'circular import'
class StateCalculator:

    def __init__(self, last: 'StatesManager'):
        self.last = last

    # ========== Отложил реализацию ==========
    # def creat_new_creature(self,
    #                    kind: 'Kind',
    #                    name: str,
    #                    birhdate: dt,
    #                    body: creature.Body,
    #                    mind: creature.Mind) -> creature.Creature:
    #     """Создаёт нового зверька"""
    #     # print(constants.BASE_DIR / 'states.json')
    #     save = constants.BASE_DIR / 'states.json'
    #     if not save:
    #         data.PersistenceManager.write_states()

    def __revive_body(self) -> creature.Body:
        """Вычисляет мгновенные значения параметров Body после загрузки данных из файлов состояний"""
        body_states = data.PersistenceManager.read_states()
        return creature.Body(body_states.body_last.health,
                             body_states.body_last.stamina,
                             body_states.body_last.hunger,
                             body_states.body_last.thirst)

    def __revive_mind(self) -> creature.Mind:
        """Вычисляет мгновенные значения параметров Mind после загрузки данных из файлов состояний"""
        mind_states = data.PersistenceManager.read_states()
        return creature.Mind(mind_states.mind_last.pattern,
                             mind_states.mind_last.joy,
                             mind_states.mind_last.anger,
                             mind_states.mind_last.timestamp)

    def revive_creature(self, revive_name, revive_birthdate):
        """Считывает последние состояния Mind, Body зверька и возвращает новые значения"""
        self.revive_name = revive_name
        self.revive_birthdate = revive_birthdate
        return creature.Creature(revive_name, revive_birthdate, self.__revive_body(), self.__revive_mind())


class KindParameters:
    class Ranges:
        def __init__(self,
                     health: 'ParamRanges',
                     stamina: 'ParamRanges',
                     hunger: 'ParamRanges',
                     thirst: 'ParamRanges'):
            self.health = health
            self.stamina = stamina
            self.hunger = hunger
            self.thirst = thirst

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
    st = StatesManager('andrey', '','', '', '')
    # save = st.to_dict()


    # pm = PersistenceManager('')
    # # pm.write_file(saves, 'property_saves.json')
    # print(pm.read_file('property_saves.json'))
