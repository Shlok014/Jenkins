# add.py
"""Small add utility with a reusable function and a tiny CLI."""

from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    return a + b

if __name__ == "__main__":
    # Simple CLI: python add.py 2 3
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add.py <num1> <num2>")
        sys.exit(2)
    try:
        # allow ints and floats
        a = float(sys.argv[1])
        b = float(sys.argv[2])
    except ValueError:
        print("Both arguments must be numbers.")
        sys.exit(2)

    result = add(a, b)
    # print as integer when both were integer-valued
    if result.is_integer():
        print(int(result))
    else:
        print(result)
