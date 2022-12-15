# импорт из стандартной библиотеки
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

    # КОММЕНТАРИЙ: как раз потому что нет ясного представления "кто мы, и куда мы идём" — а за это представление отвечает модель =Ъ
    # Пока не знаю как реализовать этот метод. :`(
    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""
        # УДАЛИТЬ: чего здесь точно не должно быть, так это чтения из файла — мы читаем из файла один раз в экземпляр StatesManager, затем с его помощью создаём экземпляры Body, Mind и Creature
        health = getattr(data.PersistenceManager.read_states().mind_last, 'health')
        stamina = getattr(data.PersistenceManager.read_states().mind_last, 'stamina')
        hunger = getattr(data.PersistenceManager.read_states().mind_last, 'hunger')
        thirst = getattr(data.PersistenceManager.read_states().mind_last, 'thirst')
        delta = dt.today()
        # Условно говоря, по прошествию 15 минут...
        delta = delta+td(minutes=15)
        # КОММЕНТАРИЙ: только вот нам в этом словаре как раз сами изменения и нужны, а для этого надо сравнить текущее мгновенное значение каждого атрибута с соответствующим диапазоном в соответствующем возрасте — а диапазоны у нас где? правильно, в Creature. значит, что нужно с этим методом сделать? правильно, перенести в Creature, изменив модель
        # ... происходят следующие изменения
        return {'health': health - 1,
                'stamina': stamina - 1,
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
        # УДАЛИТЬ: вычисления времени должны происходить не в сущности питомца, а в той(-ех) сущности(-ях), которая(-ые) управляет(-ют) питомцем
        delta = dt.today()
        # Условно говоря, по прошествию 15 минут...
        delta = delta + td(minutes=15)
        # ... происходят следующие изменения
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
    # ИСПРАВИТЬ: нам здесь не нужен timedelta объект, верните сразу количество дней
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

    # КОММЕНТАРИЙ: можно, кстати, добавить отдельную ветку классов видов пищи, которые по-разному влияют на разных существ...)) так или иначе, какие-то виды пищи всё равно нужны, иначе как тогда понимать, какие значения должны передаваться в этот метод

    def feed(self, food_amount: int) -> None:
        self.body.hunger -= food_amount
        self.mind.anger -= food_amount

    def play(self, enjoy_amount: int) -> None:
        self.body.stamina -= enjoy_amount
        self.mind.joy += enjoy_amount
        self.mind.anger -= enjoy_amount

    def talk(self, conver_amount) -> None:
        # КОММЕНТАРИЙ: я бы ещё сказал, что разговор уменьшает тревожность — впрочем, это зависит от вида питомца, от его возраста — вполне вероятно я бы сказал, что такие значения необходимо учитывать в параметрической модели (и, соответственно, в KindParameters) — но можно обойтись и константами
        self.mind.anger -= conver_amount
        self.mind.joy += conver_amount

    def clean(self, clean_amount) -> None:
        self.mind.anger -= clean_amount


class CreatureActions(Creature):
    """Класс-контейнер для функций-активностей для зверька"""
    def __init__(self, name, birthdate,
                 body_obj, mind_obj,
                 kind_actions: constants.KindActions):
        super().__init__(name, birthdate, body_obj, mind_obj)
        self.kind_actions = kind_actions

    def seek_for_honey(self) -> str:
        return "Ваш питомец ищет вкусняшку =^_^="

    def be_a_cat(self) -> str:
        return "Ваша кошка делает 'тыгыдык' 0_o"

    def be_a_naughty_cat(self) -> str:
        return "Ваша кошка сдирает диван >:X"


if __name__ == '__main__':
    md = Mind('', '', '')
    print(md.tick_changes())
