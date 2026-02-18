def check_fibonacci(val):
    a, b = 1, 1
    
    while b < val:
        memory = b
        b = a + b
        a = memory
        
    return b == val

# Example usage:
# print(check_fibonacci(8)) # True