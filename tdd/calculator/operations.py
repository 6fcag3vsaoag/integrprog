"""Модуль операций калькулятора."""


def add(a: float, b: float) -> float:
    """Сложить два числа.

    Args:
        a: Первое число
        b: Второе число

    Returns:
        Сумма чисел a и b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Вычесть второе число из первого.

    Args:
        a: Первое число (уменьшаемое)
        b: Второе число (вычитаемое)

    Returns:
        Разность чисел a и b
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Умножить два числа.

    Args:
        a: Первое число
        b: Второе число

    Returns:
        Произведение чисел a и b
    """
    return a * b


def percentage(value: float, percent: float) -> float:
    """Вычислить процент от числа.

    Args:
        value: Базовое значение
        percent: Процент для вычисления

    Returns:
        Вычисленный процент от значения
    """
    return value * percent / 100
