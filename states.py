# импорт из стандартной библиотеки
from __future__ import annotations
from datetime import datetime as dt
from dataclasses import dataclass
import json
from random import randrange as rr

# импорт дополнительных модулей
import creature
import constants


class KindParameters:
    """Композиция. Описывает диапазоны состояний."""
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


class BodyState:
    """Описывает состояние физических параметров """
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
        # Записывает физические зверька атрибуты в словарь
        return {'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'health': self.health,
                'stamina': self.stamina,
                'hunger': self.hunger,
                'thirst': self.thirst,
                'intestine': self.intestine}


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

    def to_dict(self):
        # Записывает моральные/ментальные зверька атрибуты в словарь
        return {'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'joy': self.joy,
                'activity': self.activity,
                'anger': self.anger,
                'anxiety': self.anxiety}


class StatesManager:
    """Руководит всеми атрибутами, состояниями зверька"""
    def __init__(self,
                 kind: constants.Kind,
                 name: str,
                 birthdate: dt,
                 body_last: BodyState,
                 mind_last: MindState):
        self.kind = kind
        self.name = name
        self.birthdate = birthdate
        self.body_last = body_last
        self.mind_last = mind_last

    def to_dict(self) -> dict:
        return {'kind': self.kind,
                'name': self.name,
                'birthdate': self.birthdate,
                'body_last': self.body_last.to_dict(),
                'mind_last': self.mind_last.to_dict()}


# УДАЛИТЬ: не так надо от закольцованного импорта избавляться, а разумным распределением кода по модулям
# Избавляет от 'circular import'
import data

class StateCalculator:
    """Рассчитывает состояние зверька"""
    def __init__(self, last: 'StatesManager'):
        self.last = last

    # ========== Отложил реализацию ==========
    def create_new_creature(self,
                       kind: constants.Kind,
                       name: str,
                       birhdate: dt) -> creature.Creature:
        """Создаёт нового зверька"""
        # УДАЛИТЬ: все эти атрибуты уже есть в self.last
        self.kind = kind
        self.name = name
        self.birhdate = birhdate
        # Так как питомец новый - интереса ради рандом распределит параметры для зверька
        self.body = creature.Body(rr(1, 6),rr(-1, 4), rr(-3, 5), rr(-3, 5))
        self.mind = creature.Mind(rr(-4, 4), rr(-3, 4))
        self.kind = input('Введите один из доступных видов питомцев(cat - кот, dog - собака, '
                          'fox - лиса, fox - лиса, bear - медведь, snake - змея, lizard - ящерица) >>> ').lower()
        self.name = input('Введите имя питомца >>> ').lower()
        self.birhdate = input('Дата рождения Вашего питомца(Г.М.Д) >>> ')
        # new_creat = data.PersistenceManager.write_states() Где-то здесь должны быть занесены данные в json-файл о зверьке
        return creature.Creature(self.name, self.birhdate, self.body, self.mind, self.kind)

    def __revive_body(self) -> creature.Body:
        """Вычисляет мгновенные значения параметров Body после загрузки данных из файлов состояний"""
        # УДАЛИТЬ: и эти все параметры уже есть в self.last.body_last
        body_states = data.PersistenceManager.read_states()
        return creature.Body(body_states.mind_last.health,
                             body_states.mind_last.stamina,
                             body_states.mind_last.hunger,
                             body_states.mind_last.thirst)

    def __revive_mind(self) -> creature.Mind:
        """Вычисляет мгновенные значения параметров Mind после загрузки данных из файлов состояний"""
        mind_states = data.PersistenceManager.read_states()
        return creature.Mind(mind_states.body_last.anxiety,
                             mind_states.body_last.joy,
                             mind_states.body_last.anger,
                             )

    def revive_creature(self) -> creature.Creature:
        """Считывает последние состояния Mind, Body зверька и возвращает новые значения"""
        # УДАЛИТЬ: наш экземпляр уже должен содержать все необходимые параметры зверька, мы ведь этот экземпляр StatesManager создали с помощью метода PersistenceManager.read_states(), прочитав и загрузив все необходимые данные — у вас проблема не с импортами, а с последовательностью действий
        self.revive_name = data.PersistenceManager.read_states().name
        self.revive_birthdate = data.PersistenceManager.read_states().birthdate
        revive_body = self.__revive_body()
        revive_mind = self.__revive_mind()
        return creature.Creature(self.revive_name, self.revive_birthdate, revive_body, revive_mind)


# тесты:
if __name__ == '__main__':
    st = StateCalculator(StatesManager)
    print(st.revive_creature().name)
    # st = StatesManager('andrey', '','', '', '')
    # save = st.to_dict()
    # pm = PersistenceManager('')
    # # pm.write_file(saves, 'property_saves.json')
    # print(pm.read_file('property_saves.json'))
