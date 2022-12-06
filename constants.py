# импорт из стандартной библиотеки
from enum import Enum
from pathlib import Path
from sys import path
from typing import Union, Tuple


class Kind(Enum):
    CAT = 'cat'
    DOG = 'dog'
    FOX = 'fox'
    BEAR = 'bear'
    SNAKE = 'snake'
    LIZARD = 'lizard'
    TURTLE = 'turtle'
    # ...


BASE_DIR = Path(path[0])


# переменные типов для аннотации
pathlike = Union[str, Path]
ParamRanges = Tuple[Tuple[int, int], ...]
