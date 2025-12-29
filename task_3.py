import timeit

# 1. Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    m = len(pattern)
    n = len(text)
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        shift = shift_table.get(text[i + m - 1], m)
        i += shift
    return -1

# 2. Алгоритм Кнута-Морріса-Пратта (КМП)
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# 3. Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern, prime=101):
    m, n = len(pattern), len(text)
    d = 256
    p = h = 0
    t = 1
    for i in range(m - 1):
        t = (t * d) % prime
    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        h = (d * h + ord(text[i])) % prime
    for i in range(n - m + 1):
        if p == h:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            h = (d * (h - ord(text[i]) * t) + ord(text[i + m])) % prime
            if h < 0:
                h += prime
    return -1

# Приклад використання:
def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def benchmark():
    text1 = read_file('Cтаття_1.txt')
    text2 = read_file('Cтаття_2.txt')

    if text1 is None or text2 is None:
        print("Помилка: Файли 'Cтаття_1.txt' та 'Cтаття_2.txt' мають бути в одній папці з кодом.")
        return

    test_cases = [
        ("Стаття 1", text1, "алгоритми", "вигаданий_текст_123"),
        ("Стаття 2", text2, "структури даних", "вигаданий_текст_456")
    ]

    algorithms = [
        ("Боєра-Мура", boyer_moore_search),
        ("КМП", kmp_search),
        ("Рабіна-Карпа", rabin_karp_search)
    ]

    print(f"{'Текст':<10} | {'Тип':<12} | {'Алгоритм':<15} | {'Час (сек)':<10}")
    print("-" * 55)

    for text_name, text_content, exist_p, fake_p in test_cases:
        for p_type, pattern in [("Існуючий", exist_p), ("Вигаданий", fake_p)]:
            for algo_name, algo_func in algorithms:
                time_taken = timeit.timeit(lambda: algo_func(text_content, pattern), number=100)
                print(f"{text_name:<10} | {p_type:<12} | {algo_name:<15} | {time_taken:.5f}")

if __name__ == "__main__":
    benchmark()
