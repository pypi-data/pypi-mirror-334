import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from pltstat import singlefeat as sf
from pltstat import twofeats as tf
from pltstat import multfeats as mf
from pltstat import circle as crl



import numpy as np
from scipy.stats import fisher_exact

def fisher_test(obs, alpha=0.05):
    obs = obs.values
    # p_value = _stats_r.fisher_test(obs, conf_int=True, conf_level=alpha)[0][0]

    obs = np.asarray(obs)

    # Если таблица 2x2, используем scipy
    if obs.shape == (2, 2):
        _, p_value = fisher_exact(obs, alternative='two-sided')
        return p_value

    # Если таблица до 5x5 или force_monte_carlo False, используем библиотеку fisher
    if obs.shape[0] <= 5 and obs.shape[1] <= 5 and not force_monte_carlo:
        p_value = fisher.pvalue(obs).two_tail
        return p_value

    return None, p_value
from scipy.special import comb


def hypergeom_prob(obs):
    """
    Вычисление гипергеометрической вероятности для наблюдаемой таблицы.
    """
    # Маргинальные суммы
    row_sums = obs.sum(axis=1)
    col_sums = obs.sum(axis=0)
    total_sum = obs.sum(axis=0).sum(axis=0)

    # Гипергеометрическое распределение
    prob = 1.0
    for i in range(len(row_sums)):
        prob *= comb(row_sums[i], obs[i, 0]) * comb(total_sum - row_sums[i], col_sums[0] - obs[i, 0])

    # Нормируем на общее количество вариантов
    prob /= comb(total_sum, col_sums[0])

    return prob


def monte_carlo_simulation(obs, num_samples=10000):
    """
    Вычисление p-value с использованием метода Монте-Карло.
    """
    observed_prob = hypergeom_prob(obs)
    more_extreme_count = 0

    # Генерация случайных таблиц с фиксированными маргинальными суммами
    for _ in range(num_samples):
        rand_table = np.zeros_like(obs, dtype=int)
        for i, row_sum in enumerate(np.sum(obs, axis=1)):
            rand_table[i, :] = np.random.multinomial(row_sum, np.sum(obs, axis=0) / np.sum(obs))

        if hypergeom_prob(rand_table) <= observed_prob:
            more_extreme_count += 1

    return more_extreme_count / num_samples


def monte_carlo_simulation(obs, num_samples=10000):
    """
    Вычисление p-value с использованием метода Монте-Карло.
    Векторизация генерации случайных таблиц.
    """
    observed_prob = hypergeom_prob(obs)
    row_sums = np.sum(obs, axis=1)
    col_sums = np.sum(obs, axis=0)
    total_sum = np.sum(obs)

    # Генерация всех случайных таблиц за один шаг
    rand_tables = np.array([np.random.multinomial(row_sum, col_sums / total_sum) for row_sum in row_sums])

    # Преобразование в векторизованный формат для подсчета гипергеометрической вероятности
    probs = np.apply_along_axis(hypergeom_prob, 1, rand_tables)

    # Подсчитываем количество случайных таблиц с более экстремальными вероятностями
    return np.mean(probs <= observed_prob)


def fisher_exact_custom(obs, monte_carlo_samples=10000):
    """
    Тест Фишера для наблюдаемой таблицы.

    :param obs: Наблюдаемая таблица сопряженности (например, 2x2)
    :param monte_carlo_samples: Количество симуляций для Монте-Карло
    :return: p-value
    """
    # Если таблица 2x2, используем scipy
    if obs.shape == (2, 2):
        _, p_value = fisher_exact(obs)
        return p_value

    # Для всех остальных случаев используем Монте-Карло
    return monte_carlo_simulation(obs, num_samples=monte_carlo_samples)



# Пример использования
obs_2x2 = np.array([[10, 20], [20, 30]])  # Таблица 2x2
obs_3x2 = np.array([[10, 20], [20, 30], [30, 40]])  # Таблица 3x2

# Пример с таблицей 2x2
p_value_2x2 = fisher_exact_custom(obs_2x2)
print(f"P-value для 2x2: {p_value_2x2}")

# Пример с таблицей 3x2 (используется Монте-Карло)
p_value_3x2 = fisher_exact_custom(obs_3x2)
print(f"P-value для 3x2: {p_value_3x2}")
