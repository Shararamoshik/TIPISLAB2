import random
from itertools import permutations

def intersections(size_a, size_b) -> dict:
    list_a = []
    for i in range(size_a):
        list_a.append(i+1)

    list_b = []
    for i in range(size_b):
        list_b.append(i+1)

    all_permutations = list(permutations(list_b))
    result = {}
    for i in all_permutations:
        result[i] = random.choice(list_a)

    return result
