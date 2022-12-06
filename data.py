# импорт из стандартной библиотеки
from json import load as jload, dump as jdump
from datetime import datetime as dt

# импорт дополнительных модулей
import states
import constants


class PersistenceManager:
    """
    Предоставляет пути по умолчанию и методы для работы с файлами данных.
    """
    default_parameters_path = constants.BASE_DIR / 'parameters.json'
    default_states_path = constants.BASE_DIR / 'states.json'

    @classmethod
    def read_parameters(cls, kind: constants.Kind, parameters_path: constants.pathlike = None) -> states.KindParameters:
        """Загружает из JSON файла параметры вида в экземпляр KindParameters и возвращает его."""

    @classmethod
    def read_states(cls, states_path: constants.pathlike = None) -> states.StatesManager:
        """Загружает из JSON файла последнее сохранённое состояние питомца в экземпляр StatesManager и возвращает его."""
        if not states_path:
            states_path = cls.default_states_path
        with open(states_path, encoding='utf-8') as filein:
            data = jload(filein)

        data['body_state']['timestamp'] = dt.strptime(data['body_state']['timestamp'], '%Y-%m-%d %H:%M:%S')
        data['mind_state']['timestamp'] = dt.strptime(data['mind_state']['timestamp'], '%Y-%m-%d %H:%M:%S')

        return states.StatesManager(
            constants.Kind(data['kind']),
            data['name'],
            dt.strptime(data['birthdate'], '%Y-%m-%d %H:%M:%S'),
            states.BodyState(**data['body_state']),
            states.MindState(**data['mind_state'])
        )

    @classmethod
    def write_states(cls, state, states_path: constants.pathlike = None):
        """"""


# тесты
if __name__ == '__main__':
    sm = PersistenceManager.read_states()
    print(sm.__dict__, end='\n\n')
    print(sm.body_last.__dict__, end='\n\n')
    print(sm.mind_last.__dict__, end='\n\n')
