def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    
    avg = total / len(numbers)
    return avg


data = []
result = calculate_average(data)
print("Average:", result)