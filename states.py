# импорт из стандартной библиотеки
from __future__ import annotations
import datetime
from datetime import datetime as dt
from dataclasses import dataclass
import json

# импорт дополнительных модулей
import creature
import constants
import data


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
        """Вычисляет мгновенные значения параметров Body после загрузки данных из файлов состояний"""
        body_states = data.PersistenceManager.read_states()
        return creature.Body(body_states.body_last.health,
                             body_states.body_last.stamina,
                             body_states.body_last.hunger,
                             body_states.body_last.thirst)

    def __revive_mind(self) -> creature.Mind:
        """Вычисляет мгновенные значения параметров Mind после загрузки данных из файлов состояний"""
        mind_states = data.PersistenceManager.read_states()
        return creature.Body(mind_states.mind_last.pattern,
                             mind_states.mind_last.joy,
                             mind_states.mind_last.anger,
                             mind_states.mind_last.timestamp)

    def revive_creature(self, revive_name, revive_birthdate):
        """Считывает последние состояния Mind, Body зверька и возвращает новые значения"""
        self.revive_name = revive_name
        self.revive_birthdate = revive_birthdate
        return creature.Creature(revive_name, revive_birthdate, self.__revive_body(), self.__revive_mind())


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
    st = StateCalculator('')
    print(st.revive_body())

    # pm = PersistenceManager('')
    # # pm.write_file(saves, 'property_saves.json')
    # print(pm.read_file('property_saves.json'))
