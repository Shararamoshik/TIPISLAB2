import random
from typing import Any, Generator

from .GenerationRules import reshuffling

def bim_generator(start_state: list) -> Generator[list, Any, Any]:
    while True:
        index_pair = random.randint(0, len(start_state)-2)
        start_state = reshuffling(start_state, index_pair)
        yield [start_state]
