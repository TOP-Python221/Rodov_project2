# импорт из стандартной библиотеки
import datetime
from datetime import datetime as dt, timedelta as td, date
from random import choice
from random import randrange as rr

# импорт дополнительных модулей текущего пакета
from src.utils import constants

class Body:
    """
    Описывает физиологические параметры питомца. Предоставляет методы для управления параметрами.
    """
    def __init__(self,
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int):
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst


class Mind:
    """
    Описывает эмоциональные параметры питомца.
    """
    patterns = {}

    def __init__(self,
                 anxiety: int,
                 joy: int,
                 anger: int):
        self.joy = joy
        self.anxiety = anxiety
        self.anger = anger

    @property
    def get_pattern(self):
        return self.anger

    @get_pattern.setter
    def set_pattern(self, new_value):
        self.anger = new_value


class Creature:
    """
    Описывает питомца. Предоставляет универсальные методы для взаимодействия с питомцем.
    """
    def __init__(self,
                 name: str,
                 birthdate: dt,
                 body_obj: Body,
                 mind_obj: Mind,
                 kind: constants.Kind = None):
        self.name = name
        self.birthdate = birthdate
        self.body = body_obj
        self.mind = mind_obj
        self.kind = kind
        self._actions = [CreatureActions.be_a_naughty_cat(),
                         CreatureActions.be_a_cat(),
                         CreatureActions.seek_for_honey()]

    def __eq__(self, other):
        if not isinstance(other, Creature):
            raise TypeError('TypeError')

        return self.kind == other.kind and self.name == other.name and self.birthdate == other.birthdate and \
               self.body == other.body and \
               self.mind == other.mind

    @property
    def age(self) -> int:
        return (dt.now() - self.birthdate).days

    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""
        return {self.body.hunger + rr(-10, 10),
                self.body.stamina + rr(-10, 10),
                self.body.thirst + rr(-10, 10),
                self.body.health + rr(-10, 10),
                self.mind.anger + rr(-10, 10),
                self.mind.anxiety + rr(-10, 10),
                self.mind.joy + rr(-10, 10)}


    # КОММЕНТАРИЙ: можно, кстати, добавить отдельную ветку классов видов пищи, которые по-разному влияют на разных существ...)) так или иначе, какие-то виды пищи всё равно нужны, иначе как тогда понимать, какие значения должны передаваться в этот метод

    def feed(self) -> tuple:
        self.body.hunger = rr(10, 18)
        self.mind.anger = rr(5, 12)
        return self.body.hunger, self.mind.anger

    # В ближайшее свободное время исправлю реализации других соседствующих методов :)
    def play(self) -> tuple:
        self.body.stamina = rr(4, 15)
        self.mind.joy = rr(5, 14)
        self.mind.anger = rr(3, 11)
        return self.body.stamina, self.mind.joy, self.mind.anger

    def talk(self) -> tuple:
        # КОММЕНТАРИЙ: я бы ещё сказал, что разговор уменьшает тревожность — впрочем, это зависит от вида питомца, от его возраста — вполне вероятно я бы сказал, что такие значения необходимо учитывать в параметрической модели (и, соответственно, в KindParameters) — но можно обойтись и константами
        self.mind.anger = rr(1, 7)
        self.mind.joy = rr(0, 5)
        self.mind.anxiety = rr(3, 11)
        return self.mind.anger, self.mind.joy, self.mind.anxiety

    def clean(self) -> tuple:
        self.mind.anger = rr(1, 8)
        return self.mind.anger

    def action(self):
        """"""
        random_action = choice(self._actions)
        return random_action


class CreatureActions(Creature):
    """Класс-контейнер для функций-активностей зверька"""
    def __init__(self, name, birthdate,
                 body_obj, mind_obj,
                 kind_actions: constants.KindActions):
        super().__init__(name, birthdate, body_obj, mind_obj)
        self.kind_actions = kind_actions

    @staticmethod
    def seek_for_honey() -> str:
        return "Ваш питомец ищет вкусняшку =^_^="

    @staticmethod
    def be_a_cat() -> str:
        return "Ваша кошка делает 'тыгыдык' 0_o"

    @staticmethod
    def be_a_naughty_cat() -> str:
        return "Ваша кошка сдирает диван >:X"


if __name__ == '__main__':
    ''''''
    # cr2 = Creature('', '', '', '')
    # print(cr == cr2)
    # print(cr.age)
    # print(cr.__dict__['_Creature__birthdate'])
    # print(type(dt.now().day))
