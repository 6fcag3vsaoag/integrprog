"""Модуль обработки текста."""


def remove_duplicate_letters(text: str) -> str:
    """Удалить последовательные повторяющиеся литеры из каждого слова.

    Проходит по каждому слову в тексте и удаляет последовательно
    повторяющиеся литеры, оставляя только одну.

    Args:
        text: Исходный текст для обработки

    Returns:
        Текст с удалёнными последовательными повторами литер

    Examples:
        >>> remove_duplicate_letters("hello")
        'helo'
        >>> remove_duplicate_letters("abba")
        'aba'
        >>> remove_duplicate_letters("привет миррр")
        'привет мир'
    """
    if not text:
        return ""

    result = []
    current_word = []

    for char in text:
        if char.isalnum():
            # Если текущая литера такая же как предыдущая в слове, пропускаем
            if current_word and current_word[-1] == char:
                continue
            current_word.append(char)
        else:
            # Не буквенно-цифровой символ — конец слова
            if current_word:
                result.append("".join(current_word))
                current_word = []
            result.append(char)

    # Добавляем последнее слово, если есть
    if current_word:
        result.append("".join(current_word))

    return "".join(result)
