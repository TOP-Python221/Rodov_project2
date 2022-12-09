# импорт из стандартной библиотеки
import datetime
from datetime import datetime as dt, timedelta as td
from typing import Dict
from time import perf_counter as pc

# импорт дополнительных модулей
import constants
import data


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

    # Пока не знаю как реализовать этот метод. :`(
    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""
        health = getattr(data.PersistenceManager.read_states().mind_last, 'health')
        stamina = getattr(data.PersistenceManager.read_states().mind_last, 'stamina')
        hunger = getattr(data.PersistenceManager.read_states().mind_last, 'hunger')
        thirst = getattr(data.PersistenceManager.read_states().mind_last, 'thirst')
        delta = datetime.datetime.today()
        # Условно говоря, по прошествию 15 минут...
        delta = delta+datetime.timedelta(minutes=15)
        #... происходят следующие изменения
        return {'health': health - 1,
                'stamina': stamina -1,
                'hunger': hunger + 3,
                'thirst': thirst + 4}


class Mind:
    """
    Описывает эмоциональные параметры питомца.
    """
    patterns = {}

    def __init__(self,
                 joy: int,
                 anger: int):
        self.joy = joy
        self.anger = anger

    @property
    def pattern(self):
        pass

    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""
        joy = getattr(data.PersistenceManager.read_states().body_last, 'joy')
        activity = getattr(data.PersistenceManager.read_states().body_last, 'activity')
        anger = getattr(data.PersistenceManager.read_states().body_last, 'anger')
        anxiety = getattr(data.PersistenceManager.read_states().body_last, 'anxiety')
        delta = datetime.datetime.today()
        # Условно говоря, по прошествию 15 минут...
        delta = delta+datetime.timedelta(minutes=15)
        #... происходят следующие изменения
        return {'joy': joy - 3,
                'activity': activity - 1,
                'anger': anger + 2,
                'anxiety': anxiety + 4}


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
        self.kind = kind
        self.name = name
        self.__birthdate = birthdate
        self.body = body_obj
        self.mind = mind_obj

    @property
    def age(self) -> td:
        return dt.now() - self.__birthdate

    def apply_changes(self) -> None:
        """Принимает значения атрибутов от функции tick_changes"""
        for state in (self.mind, self.body):
            for attr, delta in state.tick_changes().items():
                new_value = getattr(self.mind, attr) + delta
                setattr(self.mind, attr, new_value)
            for attr, delta in state.tick_changes().items():
                new_value = getattr(self.body, attr) + delta
                setattr(self.body, attr, new_value)

    def feed(self, food_amount: int) -> None:
        self.body.hunger -= food_amount
        self.mind.anger -= food_amount

    def play(self, enjoy_amount: int) -> None:
        self.body.stamina -= enjoy_amount
        self.mind.joy += enjoy_amount
        self.mind.anger -= enjoy_amount

    def talk(self, conver_amount) -> None:
        self.mind.anger -= conver_amount
        self.mind.joy += conver_amount

    def clean(self, clean_amount) -> None:
        self.mind.anger -= clean_amount


class CreatureActions(Creature):
    """Класс-контейнер для функций-активностей для зверька"""
    def __init__(self, name, birthdate,
                 body_obj, mind_obj,
                 kind_actions = Dict[constants.Kind, 'Sequence[Callable]']):
        super().__init__(name, birthdate, body_obj, mind_obj)
        self.kind_actions = kind_actions

    def seek_for_honey(self) -> str:
        return "Ваш питомец ищет вкусняшку =^_^="

    def be_a_cat(self) -> str:
        return "Ваша кошка делает 'тыгыдык' 0_o"

    def be_a_naughty_cat(self) -> str:
        return "Ваша кошка сдирает диван >:X"

if __name__ == '__main__':
    md = Mind('','','')
    print(md.tick_changes())
