# импорт из стандартной библиотеки
from json import load as jload, dump as jdump
from fractions import Fraction as frac
from datetime import datetime as dt
from random import randrange as rr

# импорт дополнительных модулей текущего пакета
from src.model import creature
from src.utils import constants


# Перенёс всё содержимое файла states в data.py, тк не смог по-нормальному
# избавиться от закольцованного импорта :(


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
    """Руководит всеми атрибутами, состояниями зверька"""

    def to_dict(self) -> dict:
        return {'kind': self.kind,
                'name': self.name,
                'birthdate': self.birthdate,
                'body_last': self.body_last.to_dict(),
                'mind_last': self.mind_last.to_dict()}


class StateCalculator:
    """Рассчитывает состояние зверька"""
    def __init__(self):
        self.last = PersistenceManager.read_states()

    def create_new_creature(self) -> 'Creature':
        """Создаёт нового зверька"""
        # Так как питомец новый - интереса ради рандом распределит параметры для зверька
        self.body = creature.Body(rr(1, 6), rr(-1, 4), rr(-3, 5), rr(-3, 5))

        self.mind = creature.Mind(rr(-4, 4), rr(-3, 4), rr(0, 5))

        # self.kind = input('Введите один из доступных видов питомца(cat - кот, dog - собака, '
                          # , fox - лиса, bear - медведь, snake - змея, lizard - ящерица) >>> ').lower()
        self.kind = 'cat'

        # self.name = input('Введите имя питомца >>> ').lower()
        self.name = 'кот'

        # self.birhdate = input('Дата рождения Вашего питомца(Год-Месяц-День) >>> ')
        self.birhdate = '2020-12-12'
        PersistenceManager.write_states({
            "kind": self.kind,
            "name": self.name,
            "birthdate": self.birhdate + ' 00:00:00',
            "mind_state": {
                "timestamp": "2022-11-26 17:30:00",
                "joy": self.mind.joy,
                "activity": '',
                "anger": self.mind.anger,
                "anxiety": self.mind.anxiety
            },
            "body_state": {
                "timestamp": "2022-11-26 17:30:00",
                "health": self.body.health,
                "stamina": self.body.stamina,
                "hunger": self.body.hunger,
                "thirst": self.body.thirst,
                "intestine": ''
            }
        })
        return creature.Creature(self.name, self.birhdate,
                                 self.body, self.mind,
                                 self.kind)

    def __revive_body(self) -> 'Body':
        """Вычисляет мгновенные значения параметров Body после загрузки данных из файлов состояний"""
        return creature.Body(self.last.body_last.health,
                             self.last.body_last.stamina,
                             self.last.body_last.hunger,
                             self.last.body_last.thirst)

    def __revive_mind(self) -> 'Mind':
        """Вычисляет мгновенные значения параметров Mind после загрузки данных из файлов состояний"""
        return creature.Mind(self.last.mind_last.anxiety,
                             self.last.mind_last.joy,
                             self.last.mind_last.anger)

    def revive_creature(self) -> 'Creature':
        """Считывает последние состояния Mind, Body зверька и возвращает новые значения"""
        return creature.Creature(self.last.name,
                                 self.last.birthdate,
                                 self.last.body_last,
                                 self.last.mind_last,
                                 self.last.kind)


class PersistenceManager:
    """
    Предоставляет пути по умолчанию и методы для работы с файлами данных.
    """
    default_parameters_path = constants.BASE_DIR / 'data/tests/parameters.json'
    default_states_path = constants.BASE_DIR / 'data/tests/states.json'
    @classmethod
    def read_parameters(cls, kind: constants.Kind, parameters_path: constants.pathlike = None) -> 'KindParameters':
        """"""

        if not parameters_path:
            parameters_path = cls.default_parameters_path

        with open(parameters_path, encoding='utf-8') as filein:
            data = jload(filein)[kind.value]

        for matureness, attrs in data['ranges'].items():
            for param, infls in attrs.items():
                if not infls:
                    continue
                if isinstance(infls, str):
                    if match := constants.separated_floats_pattern.fullmatch(infls):
                        data['ranges'][matureness][param] = tuple(
                            float(n)
                            for n in infls.split(match.group('sep'))
                        )
                    else:
                        data['ranges'][matureness][param] = float(infls)
                elif isinstance(infls, dict):
                    for range, values in infls.copy().items():
                        key = tuple(int(n) for n in range.split(','))
                        val = {
                            k: float(frac(v))
                            for k, v in values.items()
                        }
                        data['ranges'][matureness][param][key] = val
                        del data['ranges'][matureness][param][range]

        return KindParameters(
            data['title'],
            data['maturation'],
            **data['ranges']
        )

    @classmethod
    def read_states(cls, states_path: constants.pathlike = None) -> 'StatesManager':
        """Загружает из JSON файла последнее сохранённое состояние питомца в экземпляр StatesManager и возвращает его."""
        if not states_path:
            states_path = cls.default_states_path
        with open(states_path, encoding='utf-8') as filein:
            data = jload(filein)

        data['mind_state']['timestamp'] = dt.strptime(data['mind_state']['timestamp'], '%Y-%m-%d %H:%M:%S')
        data['body_state']['timestamp'] = dt.strptime(str(data['body_state']['timestamp']), '%Y-%m-%d %H:%M:%S')

        return StatesManager(
            constants.Kind(data['kind']),
            data['name'],
            dt.strptime(data['birthdate'], '%Y-%m-%d %H:%M:%S'),
            BodyState(**data['body_state']),
            MindState(**data['mind_state'])
        )

    @classmethod
    def write_states(cls, data: dict, states_path: constants.pathlike = None):
        if not states_path:
            states_path = cls.default_states_path
        with open(states_path, 'w', encoding='utf-8') as open_file:
            jdump(data, open_file)


# тесты
if __name__ == '__main__':
    st = StateCalculator()
    print(st.create_new_creature().play())
