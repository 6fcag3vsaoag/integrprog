"""Тесты для модуля обработки текста."""

import pytest
from text_processor import remove_duplicate_letters


class TestRemoveDuplicateLetters:
    """Тесты для функции удаления повторяющихся литер."""

    def test_remove_duplicates_simple(self):
        """Тест удаления простых повторяющихся литер."""
        # Arrange (Подготовка)
        text = "hello"
        expected = "helo"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_multiple_words(self):
        """Тест обработки нескольких слов."""
        # Arrange (Подготовка)
        text = "hello world"
        expected = "helo world"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_russian(self):
        """Тест обработки русского текста."""
        # Arrange (Подготовка)
        text = "привет миррр"
        expected = "привет мир"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_no_duplicates(self):
        """Тест текста без повторяющихся литер."""
        # Arrange (Подготовка)
        text = "abc def"
        expected = "abc def"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_all_same(self):
        """Тест слова из одинаковых литер."""
        # Arrange (Подготовка)
        text = "aaaa bbbb"
        expected = "a b"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_empty_string(self):
        """Тест пустой строки."""
        # Arrange (Подготовка)
        text = ""
        expected = ""

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_preserve_case(self):
        """Тест сохранения регистра букв."""
        # Arrange (Подготовка)
        text = "HeLLo"
        expected = "HeLo"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_multiple_sentences(self):
        """Тест обработки нескольких предложений."""
        # Arrange (Подготовка)
        text = "Hello world. Good morning!"
        expected = "Helo world. God morning!"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_non_sequential(self):
        """Тест не последовательных повторов (должны сохраниться)."""
        # Arrange (Подготовка)
        text = "abba"
        expected = "aba"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected

    def test_remove_duplicates_with_numbers(self):
        """Тест текста с цифрами."""
        # Arrange (Подготовка)
        text = "aa11 bb22"
        expected = "a1 b2"

        # Act (Действие)
        result = remove_duplicate_letters(text)

        # Assert (Проверка)
        assert result == expected
