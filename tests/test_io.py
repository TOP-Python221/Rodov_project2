# импорт из стандартной библиотеки
from pytest import mark, fixture

# импорт дополнительных модулей другого пакета
from src.constants import DATA_DIR, ACTIVE_STATE_KEYS
from src.data import PersistenceManager as PM
from src.for_tests import foo
from src import constants

# class TestActiveWrite:
#     def test_wrond_value(self):
#         eqs = PM.


# class TestAct:
#     def test_act_foo(self):
#         assert foo(10, 2) == 5

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


# def active_empty_files():
#   return DATA_DIR / 'tests'

# К сожалению, это пока что всё, что я смог из себя выдавить за один день :)
# Так особо и не допёр, как сравнить экземпляры класса. Не мог на русском языке найти подробное описание работы
# метода __eq__ и его параметров. Сейчас попробую этим заняться.
# В общем, как Вы уже поняли, я пытался симулировать передачу лишнего параметра питомца (new_pet = [
# 'some_unexpected_arg', 'title', 'maturity', ....)
@mark.xfail
class TestParametersRead:
  def test_unhappy_arg(self):
    active_pet = PM()
    saved_pet = active_pet.read_parameters(constants.Kind.CAT).__dir__()
    new_pet = ['some_unexpected_arg', 'title', 'maturity', 'cub', 'young', 'adult', 'elder', '__module__', '__doc__',
               'Ranges', '__init__', '__eq__', 'age_ranges', '__dict__', '__weakref__', '__hash__', '__new__', '__repr__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__ne__', '__gt__', '__ge__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
    assert saved_pet == new_pet


# aw= TestActiveWrite()
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



