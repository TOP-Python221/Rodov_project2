# импорт из стандартной библиотеки
from datetime import datetime as dt, timedelta as td

# импорт дополнительных модулей
import constants


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
        return (dt.now() - self.__birthdate).days

    def tick_changes(self) -> dict:
        """Вычисляет и возвращает словарь с изменениями параметров питомца, которые должны быть применены по прошествии очередного субъективного часа."""


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

    def action(self):
        pass


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
    cr = Creature('', '', '', '')
    print(cr.age)
    print(cr.__dict__['_Creature__birthdate'])
    print(type(dt.now().day))
