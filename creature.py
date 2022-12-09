# импорт из стандартной библиотеки
from datetime import datetime as dt, timedelta as td
from typing import Dict

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

    # Решил пока отложить реализацию метода
    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""
        health = getattr(data.PersistenceManager.read_states().mind_last, 'health')
        print(health)
        # print(data.PersistenceManager.read_states().mind_last.__dict__)

class Mind:
    """
    Описывает эмоциональные параметры питомца.
    """
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


class Creature:
    """
    Описывает питомца. Предоставляет универсальные методы для взаимодействия с питомцем.
    """
    def __init__(self,
                 name: str,
                 birthdate: dt,
                 body_obj: Body,
                 mind_obj: Mind):
        self.name = name
        self.__birthdate = birthdate
        self.body = body_obj
        self.mind = mind_obj

    @property
    def age(self) -> td:
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
        self.mind.anger -= conver_amount
        self.mind.joy += conver_amount

    def clean(self, clean_amount):
        self.mind.anger -= clean_amount


class CreatureActions(Creature):
    def __init__(self, name, birthdate,
                 body_obj, mind_obj,
                 kind_actions = Dict[constants.Kind, 'Sequence[Callable]']):
        super().__init__(name, birthdate, body_obj, mind_obj)
        self.kind_actions = kind_actions

    def seek_for_honey(self):
        return "Ваш питомец ищет вкусняшку =^_^="

    def be_a_cat(self):
        return "Ваша кошка делает 'тыгыдык' 0_o"

    def be_a_naughty_cat(self):
        return "Ваша кошка сдирает диван >:X"

if __name__ == '__main__':
    bd = Body('','','','')
    bd.tick_changes()
