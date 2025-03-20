def is_odd(n: int) -> bool:
    try:
        return n % 2 != 0
    except TypeError:
        print("Expected an integer value.")

def is_even(n: int) -> bool:
    try:
        return n % 2 == 0
    except TypeError:
        print("Expected an integer value.")

def state(n: int) -> str:
    try:
        if is_odd(n):
            return "odd"
        elif is_even(n):
            return "even"
    except TypeError:
        print("Expected an integer value.")

if __name__ == "__main__":
    # This code will only execute when the module is run as a standalone script.
    print("Executing module as a standalone script")
    number = int(input("Enter a number: "))
    print(f"{number} is ", state(number))
