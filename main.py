import JSONModule
import Graph


from Centroid import Centroid
from IntersectionsGeneration import intersections
from generation.BimGeneration import bim_generator
from generation.DepthGeneration import depth_generator
from generation.WideGeneration import wide_generator

SIZE_A = 100               # числа от 1 до 100
SIZE_B = 9                 # длина перестановки
START_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 9]
INITIAL_CENTERS = [10, 30, 50, 70, 90]   # начальные центры 5 классов
RADII = [3, 5, 7]                         # три цикла
STABILITY_WINDOW = 40    # сколько последних шагов центры не меняются для остановки
MAX_STEPS = 20000         # защита от бесконечности
INVOICE_STEP = 5           # запись каждого шага (можно увеличить для ускорения)
FILE_PATH = "my_data.json"

GENERATORS = {
    "Луч": bim_generator,
    "Глубина": depth_generator,
    "Ширина": wide_generator
}


def load_or_generate_intersections():
    if input("Выберите режим 1 - загрузить (медленно), 2 - генерировать (быстро): ") == "1":
        return JSONModule.load_dict_from_json(FILE_PATH)
    else:
        return intersections(SIZE_A, SIZE_B)

def run_experiment(generator_name, generator_func, radius, intersections_dict):
    """
    Запускает эксперимент для одного типа генерации и одного радиуса.
    Возвращает: (steps, centers_history, stable_reached)
        steps – число шагов до стабилизации (или MAX_STEPS)
        centers_history – список состояний центров на каждом шаге (INVOICE_STEP)
        stable_reached – достигнута ли стабилизация
    """
    centroids = [Centroid(init_center, radius) for init_center in INITIAL_CENTERS]
    gen = generator_func(START_STATE)   # генератор выдаёт списки перестановок

    step = 0
    centers_history = []

    while step < MAX_STEPS:
        step += 1

        states = next(gen)   # states – список перестановок

        # Обрабатываем каждую перестановку из сгенерированного на этом шаге списка
        for perm in states:
            value = intersections_dict[tuple(perm)]
            # Определяем, в какие классы попадает число
            for centroid in centroids:
                if centroid.position - radius <= value <= centroid.position + radius:
                    centroid.add_new_dots(value)

        # Обновляем центры (удаляем выпавшие точки и пересчитываем среднее)
        current_centers = []
        for centroid in centroids:
            centroid.delete_dots()
            centroid.calculate_position()
            current_centers.append(centroid.position)

        if step % INVOICE_STEP == 0:
            centers_history.append(current_centers)

        # Проверка стабилизации: последние STABILITY_WINDOW состояний центров одинаковы
        if len(centers_history) >= STABILITY_WINDOW:
            last_states = centers_history[-STABILITY_WINDOW:]
            if all(s == last_states[0] for s in last_states):
                print(f"Стабилизация достигнута на шаге {step}")
                return step, centers_history, True

    print(f"Превышен лимит шагов {MAX_STEPS}, стабилизация не достигнута")
    return MAX_STEPS, centers_history, False

def main():
    intersections_dict = load_or_generate_intersections()

    results = {}       # (gen, radius) -> steps
    histories = {}     # (gen, radius) -> list of center states

    for radius in RADII:
        print(f"\n====== ЦИКЛ ЭКСПЕРИМЕНТОВ С РАДИУСОМ {radius} ======")
        for gen_name, gen_func in GENERATORS.items():
            # Подменяем wide_generator на исправленный, если нужно
            if gen_name == "Ширина" and gen_func == wide_generator:
                gen_func = wide_generator
            print(f"\n--- Запуск: {gen_name}, радиус {radius} ---")
            steps, hist, stable = run_experiment(gen_name, gen_func, radius, intersections_dict)
            results[(gen_name, radius)] = steps
            histories[(gen_name, radius)] = hist

    Graph.plot_relative_displacement(histories, GENERATORS)
    Graph.plot_relative_displacement_by_radius_averaged(histories, RADII, GENERATORS)


if __name__ == "__main__":
    main()