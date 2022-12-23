# импорт из стандартной библиотеки
from __future__ import annotations
from datetime import datetime as dt
from random import randrange as rr

# импорт дополнительных модулей текущего пакета

from src.model import creature
from src.utils import constants


class KindParameters:
    """Композиция. Описывает диапазоны состояний."""
    class Ranges:
        def __init__(self, health_ranges, stamina_ranges,
                     hunger_ranges, thirst_ranges, intestine_ranges,
                     activity, anxiety, anger_coeff, joy_coeff):
            self.health = health_ranges
            self.stamina = stamina_ranges
            self.hunger = hunger_ranges
            self.thirst = thirst_ranges
            self.intestine = intestine_ranges
            self.joy = (0, 100)
            self.joy_coeff = joy_coeff
            self.activity= activity
            self.anger = (0, 100)
            self.anger_coeff = anger_coeff
            self.anxiety= anxiety

            def __iter__(self):
                return iter(self.__dict__.items())

    # СДЕЛАТЬ: изучите конструктор KindParameters в референсе и все вопросы по нему пишите в комментариях здесь

    # Вопросов не то, что бы не было, но... Меня пугает тот объём кода, что я вижу в нашем референсе: посидеть,
    # разобраться проблем бы не было, будь у меня на этой неделе столь же свободного времени, как на прошлой.
    # Признаться честно, думал чууууть-чуть полегче будет. Хотя и, опять же, посидеть - подумать, чай,
    # легче код будет восприниматься. Ладно, вопрос таков: за что начинать браться то? :) Работать с puml моделью.
    # Так у меня ж в голову то при работе с ней толком ничего не лезет. Думаю, глобально, как Вы,
    # ничего менять не буду. Да, не столь лаконично и изящно всё будет выглядеть, но и тырить Ваши строчки кода тоже
    # нет желания. Хоть я и местами это сделал, но, всё же, хочется своими ручками всё сделать. Хотя бы бОльшую часть :)

    def __init__(self,
                 title: str,
                 maturity: tuple,
                 cub: Ranges,
                 young: Ranges,
                 adult: Ranges,
                 elder: Ranges):
        self.title = title
        self.maturity = maturity
        self.cub = cub
        self.young = young
        self.adult = adult
        self.elder = elder

    def __eq__(self, other):
        if not isinstance(other, KindParameters):
            raise TypeError('Операнд справа должен иметь тип KindParameters')

        elder = other if isinstance(other, tuple) else other.elder
        young = other if isinstance(other, tuple) else other.young
        adult = other if isinstance(other, tuple) else other.adult
        title = other if isinstance(other, str) else other.title
        maturity = other if isinstance(other, tuple) else other.maturity
        cub = other if isinstance(other, tuple) else other.cub

        return self.elder == elder, self.young == young, self.adult == adult, self.title == title, self.maturity == \
               maturity, self.cub == cub


    def age_ranges(self, days: int) -> Ranges:
        """"""
        for age, attr in zip(self.maturity, list(constants.Matureness)):
            if days in age:
                return getattr(self, attr)


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
# Я, вроде, распределил код по модулям, но всё равно какая-то каша получилась :`(
from src.model import data
class StateCalculator:
    """Рассчитывает состояние зверька"""
    def __init__(self):
        self.last = data.PersistenceManager.read_states()


    def create_new_creature(self) -> creature.Creature:
        import data
        """Создаёт нового зверька"""
        # Так как питомец новый - интереса ради рандом распределит параметры для зверька
        self.body = creature.Body(rr(1, 6), rr(-1, 4), rr(-3, 5), rr(-3, 5))
        self.mind = creature.Mind(rr(-4, 4), rr(-3, 4), rr(0, 5))
        # self.kind = input('Введите один из доступных видов питомцев(cat - кот, dog - собака, '
        #                   'fox - лиса, fox - лиса, bear - медведь, snake - змея, lizard - ящерица) >>> ').lower()
        self.kind = 'cat'
        # self.name = input('Введите имя питомца >>> ').lower()
        self.name = 'кот'
        # self.birhdate = input('Дата рождения Вашего питомца(Г.М.Д) >>> ')
        self.birhdate = '2020-12-12'
        # new_creat = data.PersistenceManager.write_states() Где-то здесь должны быть занесены данные в json-файл о зверьке
        return creature.Creature(self.body, self.mind,
                                 self.kind, self.name,
                                 self.birhdate)

    def __revive_body(self) -> creature.Body:
        """Вычисляет мгновенные значения параметров Body после загрузки данных из файлов состояний"""
        return creature.Body(self.last.body_last.health,
                             self.last.body_last.stamina,
                             self.last.body_last.hunger,
                             self.last.body_last.thirst)

    def __revive_mind(self) -> creature.Mind:
        """Вычисляет мгновенные значения параметров Mind после загрузки данных из файлов состояний"""
        return creature.Mind(self.last.mind_last.anxiety,
                             self.last.mind_last.joy,
                             self.last.mind_last.anger)

    def revive_creature(self) -> creature.Creature:
        """Считывает последние состояния Mind, Body зверька и возвращает новые значения"""
        return creature.Creature(self.last.name,
                                 self.last.birthdate,
                                 self.last.body_last,
                                 self.last.mind_last,
                                 self.last.kind)


# тесты:
if __name__ == '__main__':
    pet = StateCalculator()
    print(pet.create_new_creature().__dir__())

