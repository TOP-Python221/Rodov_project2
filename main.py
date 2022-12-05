import json
import time
from datetime import datetime as dt
import datetime
from abc import ABC, abstractmethod
from enum import Enum
from time import perf_counter as pc

from typing import Tuple

import states


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
                 # ИСПРАВИТЬ: ParamRanges — это не отдельный класс, а переменная типа для аннотации — она подписана на диаграмме в заметке над классом
                 health_ranges: Tuple[Tuple[int, int], ...],
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int):
        self.health_ranges = health_ranges
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst

    # ОТВЕТИТЬ: зачем на диаграмме мы аннотировали возвращаемое значение этого метода словарём?
    def tick_changes(self) -> dict: # Решил пока отложить реализацию метода
        """Время изменения свойств существа."""


        # ИСПРАВИТЬ: в чём для этого метода заключается разница между состояниями "запущен игровой цикл" и "не запущен"?
        # Если запущен игровой цикл, то высчитываем отсутствие нас количества часов
        # if game_loop():
        #     start = str(dt.now().hour)
        #     # ИСПРАВИТЬ: мы специально создали отдельный класс, через который должны выполняться все операции чтения/записи — именно в его методах мы проводим нужное нам преобразование прочитанных данных в структуры объектов python
        #     end_r = open('saves.txt', 'r')
        #КОММЕНТАРИЙ: судя по коду ниже, вы всё ещё мыслите программу как линейную процедурную последовательность: в
        # нужный момент открыть файл, читать строки, как нашли нужную строку, преобразовать, и т.п. — напоминаю, что мы с вами работаем в объектно-ориентированном подходе: у вас должны быть классы, ответственные за разные действия и возвращающие различные структуры данных, а код перебрасывает эти объекты от метода к методу между разными классами
        #     for _ in end_r:
        #         if 'end_of_game = ' not in end_r.readline():
        #             end_r.readline()
        #         else:
        #             # КОММЕНТАРИЙ: крайне грустный код... вообще, предполагалось, что состояния мы будем хранить в json файле(-ах); а ещё мы зачем-то создавали классы BodyState и MindState... (подсказка: чтобы словари из json файлов загружать сразу в соответствующие экземпляры с нужными полями и методами)
        #             end = int(end_r.read(-1))
        #             average = end - int(start)
        #             self.stamina -= average
        #             self.hunger += average
        #             self.thirst += average
        #     # Знаю, что пока не пройдёт сие количество секунд, то приложение, по сути, не работает.
        #     # Пока не имею понятия на данном этапе, как можно реализовать то, что от меня требуется :). Поэтому пока протаптываю дорожку, чтобы дальше по ней можно было уложить асфальт.
        #     time.sleep(900)
        #     self.stamina -= 1
        #     self.hunger += 2
        #     self.thirst += 2
        # else:
        #     end = str(dt.now().hour)
        #     # КОММЕНТАРИЙ: а PersistenceManager смотрит на это дело из другого модуля и недоумевает: "и зачем меня вообще писали?"
        #     file = open('saves.txt', 'a+')
        #     file.write("end_of_game = " + end + '\n')
        #     file.close()


class Creature:
    def __init__(self,
                 name: str,
                 birthdate: dt):
        self.name = name
        self.__birthdate = birthdate
        # ИСПРАВИТЬ: что-то в толк не возьму: мы же вроде передали только что эти объекты аргументами в метод — вы хотите это изменить? зачем тогда параметры прописывали. ну и текстовые комментарии нужны по такому случаю
        self.body = Body('health_ranges', 1, 1, 3, 3)
        self.mind = Mind('patterns', 2, 3)

    @property
    def age(self) -> datetime.timedelta:
        return dt.now() - self.__birthdate

    def apply_changes(self):
        for state in (self.mind, self.body):
            for attr, delta in state.tick_changes().items():
                new_value = getattr(self.mind, attr) + delta
                setattr(self.mind, attr, new_value)
            for attr, delta in state.tick_changes().items():
                new_value = getattr(self.body, attr) + delta
                setattr(self.body, attr, new_value)

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
    patterns = {}
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

# КОММЕНТАРИЙ: очень похоже, что нужно внимательно пересмотреть оба занятия по проекту

# тесты:
if __name__ == '__main__':
    ex = Body(1, 1, 1, 1, 1)
    ex.tick_changes()

