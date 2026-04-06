import matplotlib.pyplot as plt


def plot_relative_displacement_by_radius_averaged(histories_data, radii, generators, window=5):
    """
    Для каждого радиуса строит график среднего приращения центров,
    усреднённого по блокам из `window` последовательных итераций.
    """
    for radius in radii:
        plt.figure(figsize=(10, 6))

        for gen_name in generators.keys():
            key = (gen_name, radius)
            hist = histories_data.get(key)
            if not hist or len(hist) < 2:
                print(f"Нет данных для {gen_name}, радиус {radius} (нужно минимум 2 шага)")
                continue

            # Вычисляем приращения для всех последовательных шагов
            increments = []
            for step_idx in range(1, len(hist)):
                prev_mean = sum(hist[step_idx - 1]) / len(hist[step_idx - 1])
                curr_mean = sum(hist[step_idx]) / len(hist[step_idx])
                increments.append(abs(curr_mean - prev_mean))

            # Разбиваем на блоки по window и усредняем
            averaged = []
            block_starts = []
            for i in range(0, len(increments), window):
                block = increments[i:i + window]
                averaged.append(sum(block) / len(block))
                block_starts.append(i + 1)  # номер первой итерации в блоке (для подписи)

            # Ось X – номер блока (или можно середину блока)
            block_numbers = list(range(1, len(averaged) + 1))
            # Либо можно показать начало блока: block_starts
            plt.plot(block_numbers, averaged, label=gen_name, marker='o', linewidth=2, markersize=6)

        plt.title(
            f"Скорость насыщения (среднее приращение центров)\nРадиус = {radius}, усреднение по {window} итерациям")
        plt.xlabel("Номер блока итераций (каждый блок = 5 шагов)")
        plt.ylabel("Среднее смещение в блоке")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"relative_displacement_avg_r{radius}_w{window}.png", dpi=150)
        plt.show()

def plot_relative_displacement(histories_data, Generators):
    """
    Строит график среднего приращения центров между последовательными итерациями.
    Это показывает «скорость» смещения системы на каждом шаге.
    """
    plt.figure(figsize=(12, 6))

    for gen_name in Generators.keys():
        # Собираем все истории для этого генератора (по всем радиусам)
        all_histories = []
        for (name, radius), hist in histories_data.items():
            if name == gen_name and hist and len(hist) > 1:
                all_histories.append(hist)
        if not all_histories:
            continue

        # Определяем минимальную длину истории среди всех радиусов для этого генератора
        min_len = min(len(h) for h in all_histories)

        # Для каждого шага вычисляем среднее приращение (по всем радиусам и классам)
        avg_increments = []
        for step_idx in range(1, min_len):
            increments = []
            for hist in all_histories:
                # Для одного эксперимента: среднее положение центров на этом шаге
                prev_mean = sum(hist[step_idx -1]) / len(hist[step_idx -1])
                curr_mean = sum(hist[step_idx]) / len(hist[step_idx])
                increments.append(abs(curr_mean - prev_mean))
            avg_increments.append(sum(increments) / len(increments))

        steps_axis = list(range(1, len(avg_increments) + 1))
        plt.plot(steps_axis, avg_increments, label=gen_name, marker='o', linewidth=2)

    plt.title("Среднее смещение центров между последовательными итерациями\n(скорость насыщения)")
    plt.xlabel("Итерации поиска")
    plt.ylabel("Смещение (абсолютное приращение среднего положения)")
    plt.legend()
    plt.grid(True)
    plt.xticks(range(1, max(2, len(steps_axis)) + 1))  # чтобы были целые метки как на примере
    plt.tight_layout()
    plt.savefig("relative_displacement.png", dpi=150)
    plt.show()