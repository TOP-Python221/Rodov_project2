# импорт из стандартной библиотеки
from enum import Enum
from pathlib import Path
from sys import path
from typing import Union, Tuple, Dict
from re import compile as reg_pattern_compile


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


BASE_DIR = Path(path[0])


# переменные типов для аннотации
pathlike = Union[str, Path]
ParamRanges = Tuple[Tuple[int, int], ...]
KindActions = Dict[Kind, 'Sequence[Callable]']

separated_floats_pattern = reg_pattern_compile(
    r'^((?P<float>\d+\.\d+)(?P<sep>[,; ])?){2,}$'
)