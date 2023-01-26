# импорт из стандартной библиотеки
import datetime
from datetime import datetime as dt, timedelta as td, date
from random import choice
from random import randrange as rr
from pprint import pprint

# импорт дополнительных модулей текущего пакета
from src.utils import constants
from src.model import data

class Body:
    """
    Описывает физиологические параметры питомца. Предоставляет методы для управления параметрами.
    """
    def __init__(self,
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int,
                 intestine: int):
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst
        self.intestine = intestine


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
    def get_actions(self) -> list:
        return self._actions

    @property
    def age(self) -> int:
        return (dt.now() - self.birthdate).days

    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""
        changed_hunger = self.body.hunger + rr(-10, 10)
        changed_stamina = self.body.stamina + rr(-10, 10)
        changed_thirst = self.body.thirst + rr(-10, 10)
        changed_health = self.body.health + rr(-10, 10)
        changed_anger = self.mind.anger + rr(-10, 10)
        changed_anxiety = self.mind.anxiety + rr(-10, 10)
        changed_joy= self.mind.joy + rr(-10, 10)
        changed_intestine = self.body.intestine + rr(-10, 10)

        read_last_state = data.PersistenceManager.read_states()

        changed_pet = data.PersistenceManager.write_states({
            "kind": str(read_last_state.kind.value),
            "name": str(read_last_state.name.title()),
            "birthdate": str(read_last_state.birthdate),
            "mind_state": {
                "timestamp": str(read_last_state.mind_last.timestamp),
                "joy": changed_joy,
                "activity": read_last_state.mind_last.activity,
                "anger": changed_anger ,
                "anxiety": changed_anxiety
            },
            "body_state": {
                "timestamp": str(read_last_state.body_last.timestamp),
                "health": changed_health,
                "stamina": changed_stamina,
                "hunger": changed_hunger,
                "thirst": changed_thirst,
                "intestine": changed_intestine
            }
        })

        print('==============Параметры питомца обновлены==============')
        return changed_pet
        # return {'hunger': self.body.hunger + rr(-10, 10),
        #         'stamina': self.body.stamina + rr(-10, 10),
        #         'thirst': self.body.thirst + rr(-10, 10),
        #         'health': self.body.health + rr(-10, 10),
        #         'anger': self.mind.anger + rr(-10, 10),
        #         'anxiety': self.mind.anxiety + rr(-10, 10),
        #         'joy': self.mind.joy + rr(-10, 10)}


    @staticmethod
    def apply_tick_changes():
        active_pet = data.PersistenceManager.read_states()
        cr = Creature(active_pet.name,
                                         active_pet.birthdate,
                                         active_pet.body_last,
                                         active_pet.mind_last,
                                         active_pet.kind.value)
        apply = cr.tick_changes()
        return apply

    @staticmethod
    def feed() -> tuple:
        return rr(10, 18), rr(5, 12), rr(9, 17)

    @staticmethod
    def play() -> tuple:
        return rr(4, 15), rr(5, 14), rr(3, 11)

    @staticmethod
    def talk() -> tuple:
        return rr(1, 7), rr(0, 5), rr(3, 11)

    @staticmethod
    def clean() -> int:
        return rr(1, 8)

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
