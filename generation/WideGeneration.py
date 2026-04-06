from typing import Any, Generator


def wide_generator(start_state: list[int]) -> Generator[list[int], Any, Any]:
    """
    Бесконечный генератор обхода в ширину графа перестановок.
    После полного обхода всех уникальных состояний начинает заново.
    """
    start_tuple = tuple(start_state)
    visited = {start_tuple}
    levels = []  # сохраняем все уровни для повторного воспроизведения
    current_level = [start_state]
    levels.append(current_level)
    yield current_level

    length = len(start_state) - 1

    while True:
        next_level = []
        for state in current_level:
            for i in range(length):
                new_state = state[:]
                new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
                new_tuple = tuple(new_state)
                if new_tuple not in visited:
                    visited.add(new_tuple)
                    next_level.append(new_state)
        if not next_level:
            break
        current_level = next_level
        levels.append(current_level)
        yield current_level

    while True:
        for level in levels:
            yield level
