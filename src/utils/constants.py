# импорт из стандартной библиотеки
from collections.abc import Sequence, Callable
from enum import Enum
from pathlib import Path
from re import compile as reg_pattern_compile
from sys import path
from typing import Union, Tuple, Dict


class Kind(Enum):
    CAT = 'cat'
    DOG = 'dog'
    FOX = 'fox'
    BEAR = 'bear'
    SNAKE = 'snake'
    LIZARD = 'lizard'
    TURTLE = 'turtle'
    # ...


class Matureness(str, Enum):
    CUB = 'cub'
    YOUNG = 'young'
    ADULT = 'adult'
    ELDER = 'elder'


BASE_DIR = Path(path[1])
DATA_DIR = BASE_DIR / 'src/model/data'
print(BASE_DIR)


# переменные типов для аннотации
pathlike = Union[str, Path]
ParamRanges = Tuple[Tuple[int, int], ...]
KindActions = Dict[Kind, 'Sequence[Callable]']
Actions = Sequence[Callable]

separated_floats_pattern = reg_pattern_compile(
    r'^((?P<float>\d+\.\d+)(?P<sep>[,; ])?){2,}$'
)

ACTIVE_STATE_KEYS = {'timestamp', 'health', 'stamina', 'hunger', 'thirst', 'intestine', 'joy', 'activity', 'anger', 'anxiety'}

HELP = ['Выйти из приложения: q/quit/выход\n',
        'Посмотреть чем занимается питомец: w/watch/посмотреть\n',]
