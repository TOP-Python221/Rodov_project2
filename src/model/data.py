# импорт из стандартной библиотеки
from json import load as jload, dump as jdump
from datetime import datetime as dt
from fractions import Fraction as frac

# импорт дополнительных модулей текущего пакета
# Среда ругалась на импорт и я переписал '.' -> src :\
from src.model import states
from src.utils import constants



class PersistenceManager:
    """
    Предоставляет пути по умолчанию и методы для работы с файлами данных.
    """
    # Вроде, исправил :)
    default_parameters_path = constants.BASE_DIR / 'data/tests/parameters.json'
    default_states_path = constants.BASE_DIR / 'data/states.json'

    @classmethod
    def read_parameters(cls, kind: constants.Kind, parameters_path: constants.pathlike = None) -> states.KindParameters:
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

        return states.KindParameters(
            data['title'],
            data['maturation'],
            **data['ranges']
        )

    @classmethod
    def read_states(cls, states_path: constants.pathlike = None) -> states.StatesManager:
        """Загружает из JSON файла последнее сохранённое состояние питомца в экземпляр StatesManager и возвращает его."""
        if not states_path:
            states_path = cls.default_states_path
        with open(states_path, encoding='utf-8') as filein:
            data = jload(filein)

        data['mind_state']['timestamp'] = dt.strptime(data['mind_state']['timestamp'], '%Y-%m-%d %H:%M:%S')
        data['body_state']['timestamp'] = dt.strptime(str(data['body_state']['timestamp']), '%Y-%m-%d %H:%M:%S')

        return states.StatesManager(
            constants.Kind(data['kind']),
            data['name'],
            dt.strptime(data['birthdate'], '%Y-%m-%d %H:%M:%S'),
            states.BodyState(**data['body_state']),
            states.MindState(**data['mind_state'])
        )

    @classmethod
    def write_states(cls, data: dict, states_path: constants.pathlike = None):
        if not states_path:
            states_path = cls.default_states_path
        with open(states_path, 'w', encoding='utf-8') as open_file:
            jdump(data, open_file)


# тесты
if __name__ == '__main__':
    d = PersistenceManager()
    print(d.read_states())
    # d = PersistenceManager.read_states()
    # print(d.mind_last.joy)
    # print(sm.__dict__, end='\n\n')
    # print(sm.body_last.__dict__, end='\n\n')
    # print(sm.mind_last.__dict__, end='\n\n')