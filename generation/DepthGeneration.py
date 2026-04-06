import random
from typing import Any, Generator

from .GenerationRules import reshuffling

def depth_generator(start_state: list) -> Generator[list, Any, Any]:
    length_state = len(start_state) - 1
    while True:
        result = []
        for i in range(length_state):
            result.append(reshuffling(start_state, i))
        start_state = random.choice(result)
        yield result
