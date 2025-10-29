def multiply_all(*args: int) -> int :
    result = 1
    for num in args : 
        result *= num
    return result


"""
- *args : allows any number of arguments; args becomes 
a tuple which contains all the passed arguments
"""