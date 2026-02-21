"""Тесты для операций калькулятора."""

import pytest
from calculator import add, subtract, multiply, percentage


class TestAdd:
    """Тесты для функции сложения."""

    def test_add_positive_numbers(self):
        """Тест сложения двух положительных чисел."""
        # Arrange (Подготовка)
        a = 2
        b = 3
        expected = 5

        # Act (Действие)
        result = add(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_add_negative_numbers(self):
        """Тест сложения двух отрицательных чисел."""
        # Arrange (Подготовка)
        a = -2
        b = -3
        expected = -5

        # Act (Действие)
        result = add(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_add_with_zero(self):
        """Тест сложения с нулём."""
        # Arrange (Подготовка)
        a = 5
        b = 0
        expected = 5

        # Act (Действие)
        result = add(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_add_positive_and_negative(self):
        """Тест сложения положительного и отрицательного чисел."""
        # Arrange (Подготовка)
        a = 10
        b = -3
        expected = 7

        # Act (Действие)
        result = add(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_add_floats(self):
        """Тест сложения чисел с плавающей точкой."""
        # Arrange (Подготовка)
        a = 2.5
        b = 3.5
        expected = 6.0

        # Act (Действие)
        result = add(a, b)

        # Assert (Проверка)
        assert result == expected


class TestSubtract:
    """Тесты для функции вычитания."""

    def test_subtract_positive_numbers(self):
        """Тест вычитания двух положительных чисел."""
        # Arrange (Подготовка)
        a = 5
        b = 3
        expected = 2

        # Act (Действие)
        result = subtract(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_subtract_negative_result(self):
        """Тест вычитания с отрицательным результатом."""
        # Arrange (Подготовка)
        a = 3
        b = 5
        expected = -2

        # Act (Действие)
        result = subtract(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_subtract_with_zero(self):
        """Тест вычитания с нулём."""
        # Arrange (Подготовка)
        a = 5
        b = 0
        expected = 5

        # Act (Действие)
        result = subtract(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_subtract_negative_numbers(self):
        """Тест вычитания отрицательных чисел."""
        # Arrange (Подготовка)
        a = -5
        b = -3
        expected = -2

        # Act (Действие)
        result = subtract(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_subtract_floats(self):
        """Тест вычитания чисел с плавающей точкой."""
        # Arrange (Подготовка)
        a = 5.5
        b = 2.5
        expected = 3.0

        # Act (Действие)
        result = subtract(a, b)

        # Assert (Проверка)
        assert result == expected


class TestMultiply:
    """Тесты для функции умножения."""

    def test_multiply_positive_numbers(self):
        """Тест умножения двух положительных чисел."""
        # Arrange (Подготовка)
        a = 4
        b = 3
        expected = 12

        # Act (Действие)
        result = multiply(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_multiply_by_zero(self):
        """Тест умножения на ноль."""
        # Arrange (Подготовка)
        a = 5
        b = 0
        expected = 0

        # Act (Действие)
        result = multiply(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_multiply_negative_numbers(self):
        """Тест умножения отрицательного числа на положительное."""
        # Arrange (Подготовка)
        a = -4
        b = 3
        expected = -12

        # Act (Действие)
        result = multiply(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_multiply_two_negatives(self):
        """Тест умножения двух отрицательных чисел."""
        # Arrange (Подготовка)
        a = -4
        b = -3
        expected = 12

        # Act (Действие)
        result = multiply(a, b)

        # Assert (Проверка)
        assert result == expected

    def test_multiply_floats(self):
        """Тест умножения чисел с плавающей точкой."""
        # Arrange (Подготовка)
        a = 2.5
        b = 4
        expected = 10.0

        # Act (Действие)
        result = multiply(a, b)

        # Assert (Проверка)
        assert result == expected


class TestPercentage:
    """Тесты для функции вычисления процента."""

    def test_percentage_basic(self):
        """Тест базового вычисления процента."""
        # Arrange (Подготовка)
        value = 200
        percent = 10
        expected = 20.0

        # Act (Действие)
        result = percentage(value, percent)

        # Assert (Проверка)
        assert result == expected

    def test_percentage_zero(self):
        """Тест вычисления нулевого процента."""
        # Arrange (Подготовка)
        value = 100
        percent = 0
        expected = 0.0

        # Act (Действие)
        result = percentage(value, percent)

        # Assert (Проверка)
        assert result == expected

    def test_percentage_hundred(self):
        """Тест вычисления 100 процентов."""
        # Arrange (Подготовка)
        value = 50
        percent = 100
        expected = 50.0

        # Act (Действие)
        result = percentage(value, percent)

        # Assert (Проверка)
        assert result == expected

    def test_percentage_decimal(self):
        """Тест вычисления дробного процента."""
        # Arrange (Подготовка)
        value = 100
        percent = 15.5
        expected = 15.5

        # Act (Действие)
        result = percentage(value, percent)

        # Assert (Проверка)
        assert result == expected

    def test_percentage_of_negative(self):
        """Тест вычисления процента от отрицательного числа."""
        # Arrange (Подготовка)
        value = -200
        percent = 10
        expected = -20.0

        # Act (Действие)
        result = percentage(value, percent)

        # Assert (Проверка)
        assert result == expected
