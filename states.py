# импорт из стандартной библиотеки
from datetime import datetime as dt
from dataclasses import dataclass

# импорт дополнительных модулей
import creature
import constants


# КОММЕНТАРИЙ: располагайте классы в порядке использования: сначала самые вложенные, затем те, которые их используют, и так далее


class Ranges:
    """
    Диапазоны параметров вида !! и влияния !!
    """
    def __init__(self,
                 health: constants.ParamRanges,
                 stamina: constants.ParamRanges,
                 hunger: constants.ParamRanges,
                 thirst: constants.ParamRanges,
                 ):
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst


class KindParameters:
    """
    Описывает параметры, диапазоны и взаимные влияния параметров для разных возрастных этапов вида питомцев.
    """
    def __init__(self,
                 title: str,
                 maturity: tuple,
                 cub: Ranges,
                 yong: Ranges,
                 adult: Ranges,
                 elder: Ranges):
        self.title = title
        self.maturity = maturity
        self.cub = cub
        self.yong = yong
        self.adult = adult
        self.elder = elder

    def age_ranges(self) -> Ranges:
        pass


@dataclass
class BodyState:
    """
    Снимок (хранитель) физиологических параметров питомца определённый момент.
    """
    timestamp: dt
    health: int
    stamina: int
    hunger: int
    thirst: int
    intestine: int


@dataclass
class MindState:
    """
    Снимок (хранитель) эмоциональных параметров питомца определённый момент.
    """
    timestamp: dt
    joy: int
    activity: float
    anger: int
    anxiety: float



class StatesManager:
    """
    Полностью описывает ранее сохранённого питомца.
    """
    def __init__(self,
                 kind: constants.Kind,
                 name: str,
                 birthdate: dt,
                 body_last: BodyState,
                 mind_last: MindState,
                 ):
        self.kind = kind
        self.name = name
        self.birthdate = birthdate
        self.body = body_last
        self.mind = mind_last


class StateCalculator:
    """
    Предоставляет методы для вычисления нового состояния питомца на основании ранее сохранённого.
    ?? Предоставляет метод(-ы) для создания новорождённого питомца ??
    """
    def __init__(self, previous: StatesManager):
        self.previous = previous

    def __new_body(self) -> creature.Body:
        pass

    def __new_mind(self) -> creature.Mind:
        pass

    # ОТВЕТИТЬ: это метод создания экземпляра для уже существующего питомца или для новорождённого? в зависимости от этого у вас, очевидно, будут различные источники данных — да и сами действия отличаться будут скорее всего, ведь для уже существующего питомца надо ещё расчёты нового состояния провести
    def new_creature(self, new_name, new_birthdate):
        return creature.Creature(
            new_name,
            new_birthdate,
            self.__new_body(),
            self.__new_mind()
        )


# тесты:
if __name__ == '__main__':
    # saves = {
    #     'health': ((1, 2), (3, 9), (10, 16), (17, 20),),
    #     'stamina': ((1, 3), (4, 10), (11, 17), (18, 20),),
    #     'hunger': ((1), (1), (1), (1),),
    #     'thirst': ((1), (1), (1), (1),),
    # }
    pass
