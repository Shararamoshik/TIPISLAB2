import json
import ast
from typing import Dict, List, Union, Tuple

def save_dict_to_json(data: Dict[tuple, List[str]], filepath: str) -> None:
    dict_to_save = {str(key): value for key, value in data.items()}

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dict_to_save, f, ensure_ascii=False, indent=4)


def _parse_tuple_key(key_str: str) -> Tuple[int, ...]:
    """
    Быстро преобразует строку вида '(1, 2, 3)' в кортеж целых чисел.
    Работает ~в 5-10 раз быстрее ast.literal_eval для больших данных.
    """
    # Убираем скобки и разбиваем по запятым
    content = key_str.strip()[1:-1]  # удаляем '(' и ')'
    if not content:
        return ()  # пустой кортеж
    # Разделяем по запятой, убираем пробелы и преобразуем в int
    return tuple(int(item.strip()) for item in content.split(','))


def load_dict_from_json(filepath: str) -> Dict[Tuple[int, ...], List[str]]:
    """
    Загружает словарь из JSON, восстанавливая ключи как кортежи целых чисел.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        loaded_dict = json.load(f)

    result = {}
    for key_str, value in loaded_dict.items():
        # Быстрый парсинг кортежа (без ast.literal_eval)
        key = _parse_tuple_key(key_str)
        result[key] = value
    return result