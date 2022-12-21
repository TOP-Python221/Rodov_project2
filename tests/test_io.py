# импорт из стандартной библиотеки
from pytest import mark, fixture

# импорт дополнительных модулей другого пакета
from src.constants import DATA_DIR, ACTIVE_STATE_KEYS
from src.data import PersistenceManager as PM


class TestActiveWrite:
    read_data = PM.read_states()
    print(read_data)


# def active_empty_files():
#     return (DATA_DIR / 'tests').rglob('active_empty*.json')
#
# def active_unhappy_keys_files():
#     return (DATA_DIR / 'tests').rglob('active_unhappy_keys*.json')


# @fixture
# def active_state():
#     return 'last_state'
#
# @fixture
# def active_keys(active_state):
#     return {'kind', 'name', 'birthdate', active_state}
#
# @fixture
# def active_state_keys():
#     return ACTIVE_STATE_KEYS



class TestParametersRead:
    pass

aw= TestActiveWrite()
# aw.read_data()
# class TestActiveRead:
#
#     def test_not_existing(self):
#         data = PM.read_active(DATA_DIR / 'tests/not_existing.json')
#         assert data == {}
#
#     @mark.parametrize('file_path', active_empty_files())
#     def test_empty(self, file_path):
#         data = PM.read_active(file_path)
#         assert data == {}, f'{file_path.name}'
#
#     @mark.xfail
#     @mark.parametrize('file_path', active_unhappy_keys_files())
#     def test_unhappy_keys(self, file_path, active_keys, active_state, active_state_keys):
#         PM.read_active(file_path)



