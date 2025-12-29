def binary_search_upper_bound(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])

        elif arr[mid] > target:
            upper_bound = arr[mid]
            high = mid - 1

        else:
            low = mid + 1

    if upper_bound is None and low < len(arr):
        upper_bound = arr[low]

    return (iterations, upper_bound)

# Приклад використання:
sorted_array = [0.1, 0.5, 1.2, 2.8, 3.5, 5.9, 7.1]
target_value = 2.5

result = binary_search_upper_bound(sorted_array, target_value)
print(f"Результат (ітерації, верхня межа): {result}")
