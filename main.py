from datetime import datetime as dt
import datetime
from abc import ABC, abstractmethod


class Creature:
    def __init__(self, name: str,
                 birthdate: dt,
                 body: 'Body',
                 mind: 'Mind'):
        self.name = name
        self.__birthdate = birthdate
        self.body = body
        self.mind = mind

    @property
    def age(self) -> datetime.timedelta:
        return (dt.now() - self.__birthdate)

    def feed(self):
        pass

    def play(self):
        pass

    def talk(self):
        pass


class Body:
    def __init__(self,
                 health: int,
                 stamina: int,
                 hunger: int,
                 thirst: int):
        self.health = health
        self.stamina = stamina
        self.hunger = hunger
        self.thirst = thirst

    # @staticmethod # Статический только для тестов
    def tired(self):
        """Описывает физическое состояние питомца: устал/не устал"""
        if dt.today().strftime('%H') > '11': # Это, скорее, для тестов сделано, чтобы посмотреть как работает функции
            # модуля datetime
            return 'Ваш питомец устал'
        return 'Ваш питомец, как огурчик ;D'

    def sleep(self):
        pass


class Mind:
    pass

# тесты:
if __name__ == '__main__':
    animal = Creature('Ivan', datetime.datetime(2007, 6, 19), '', '')
    print(f'{animal.age.days // 365} лет')
