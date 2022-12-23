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
  new_atrs = []
  active_pet = PM()
  saved_pet = active_pet.read_parameters(constants.Kind.CAT).__dir__()

  for val in saved_pet:
    if not val.startswith('__'):
      new_atrs.append(val)

  return new_atrs


# Всё также на данный момент времени не разобрался с __eq__, поэтому тест, увы, такой. Как говорится: на безрыбье и
# рак рыба
# class TestActiveParameters:
#   @staticmethod
#   @mark.xfail
#   @mark.parametrize('arg, exp_res', [({}, get_init_param()),
#                                      ([], get_init_param()),
#                                      ('', get_init_param()),
#                                      (1, get_init_param()),
#                                      (['unex_param','title', 'maturity', 'cub', 'young', 'adult', 'elder', 'Ranges',
#                                        'age_ranges'], get_init_param()),
#                                      (['maturity', 'cub', 'elder', 'Ranges',
#                                        'age_ranges'], get_init_param())])
#   def test_unhappy_keys(arg, exp_res):
#     assert arg == exp_res
#
#   @staticmethod
#   def test_happy_keys():
#     assert ['title', 'maturity', 'cub', 'young', 'adult', 'elder', 'Ranges', 'age_ranges'] == get_init_param()


def unpack_def():
    pet = states.StateCalculator()
    return pet.create_new_creature().__dir__()




# @mark.parametrize('arg', 'exp_res', [(arg, unpack_def()),
#                                      (arg, unpack_def()),
#                                      (arg, unpack_def()),
#                                      (arg, unpack_def()),])
class TestCreature:
    @staticmethod
    def test_foo(arg, unpack_def):
        pass

