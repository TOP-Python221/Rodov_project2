# импорт из стандартной библиотеки
from pytest import mark, fixture

# импорт дополнительных модулей другого пакета
from src.model.data import PersistenceManager as PM
from src.for_tests import foo
from src.utils import constants
from src.model import states


# К сожалению, это пока что всё, что я смог из себя выдавить за один день :)
# Так особо и не допёр, как сравнить экземпляры класса. Не мог на русском языке найти подробное описание работы
# метода __eq__ и его параметров. Сейчас попробую этим заняться.
# В общем, как Вы уже поняли, я пытался симулировать передачу лишнего параметра питомца (new_pet = [
# 'some_unexpected_arg', 'title', 'maturity', ....)

# Тут был старый и неправильный тест >>>
# ...
# ...
# ...


def get_init_param() -> list:
  """Берёт полный список атрибутов экземпляра класса и возвращает список переданных в конструктор значений"""
  init_param = []
  active_pet = PM()
  saved_pet = active_pet.read_parameters(constants.Kind.CAT).__dir__()

  for val in saved_pet:
    if not val.startswith('__'):
      init_param.append(val)

  return init_param

# @fixture()
def take_empty_dict():
    return {}

# @fixture()
def take_empty_list():
    return []

# @fixture()
def take_empty_str():
    return ''

# @fixture()
def take_int():
    return 1

# @fixture()
def take_unex_params():
    return ['unex_param', 'title', 'maturity', 'cub', 'young', 'adult', 'elder', 'Ranges', 'age_ranges']

# @fixture()
def take_less_params():
    return ['maturity', 'cub', 'elder', 'Ranges', 'age_ranges']


class TestActiveParameters:
  @staticmethod
  @mark.xfail
  @mark.parametrize('arg, exp_res', [(take_empty_dict(), get_init_param()),
                                     (take_empty_list(), get_init_param()),
                                     (take_empty_str(), get_init_param()),
                                     (take_int(), get_init_param()),
                                     (take_unex_params(), get_init_param()),
                                     (take_less_params(), get_init_param())])
  def test_unhappy_keys(arg, exp_res):
    assert arg == exp_res

  @staticmethod
  def test_happy_keys():
    assert ['title', 'maturity', 'cub', 'young', 'adult', 'elder', 'Ranges', 'age_ranges'] == get_init_param()


# def get_init_param():
#     params = []
#     pet = states.StateCalculator()
#     for val in pet.create_new_creature().__dir__():
#         if not val.startswith('__'):
#             params.append(val)
#
#     return params
#
# @mark.xfail
# @mark.parametrize('arg, exp_res', [([], get_init_param()),
#                                    ({}, get_init_param()),
#                                    (['kind', 'name', '_Creature__birthdate', 'body', 'mind', 'age', 'tick_changes', 'feed', 'play',],
#                                     get_init_param()),
#                                    (1, get_init_param()),
#                                    ('str', get_init_param()),
#                                    (['unex_arg1', 'unex_arg2', 'kind', 'name', '_Creature__birthdate', 'body',
#                                       'mind', 'age',
#                                         'tick_changes', 'feed', 'play', 'talk', 'clean', 'action'], get_init_param())])
# class TestCreature:
#     @staticmethod
#     def test_unhappy_creat_creature(arg, exp_res):
#         assert arg == exp_res
#
#
# def test_happy_creat_creature():
#     assert ['kind', 'name', '_Creature__birthdate', 'body', 'mind', 'age', 'tick_changes', 'feed', 'play', 'talk', 'clean', 'action'] == get_init_param()
