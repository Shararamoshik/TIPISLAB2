def _forward_swap(state: list, index_pair: int) -> list:
    new_state = list(state)
    first_element = new_state.pop(index_pair)
    second_element = new_state.pop(index_pair)
    new_state.insert(0, first_element)
    new_state.append(second_element)
    return new_state

def _revers_swap(state: list, index_pair: int) -> list:
    new_state = list(state)
    first_element = new_state.pop(index_pair)
    second_element = new_state.pop(index_pair)
    new_state.insert(0, second_element)
    new_state.append(first_element)
    return new_state

def reshuffling(state: list, index_pair: int) -> list:
    if len(state) % 2 == 0:
        return _revers_swap(state, index_pair)
    else:
        return _forward_swap(state, index_pair)