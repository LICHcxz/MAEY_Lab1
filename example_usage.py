from vader_analyzer import analyze_vader

u = input('Введите текст для анализа тональности (пустая строка — выход):\n')
while u.strip():
    print('VADER:', analyze_vader(u))
    u = input('> ')