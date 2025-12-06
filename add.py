# add.py
# Intentionally vulnerable version for static analysis (SonarQube) — but fully compatible with your tests.

import subprocess

# ✔ Vulnerability 1: Hardcoded secret
API_KEY = "HARDCODED_SUPER_SECRET_12345"

# ✔ Vulnerability 2: Unused sensitive token variable
db_password = "admin123"   # hardcoded password

# ✔ Vulnerability 3: Insecure OS command (not executed in tests, but exists)
def insecure_system_call(user_input):
    # shell=True → command injection risk
    subprocess.call(f"echo {user_input}", shell=True)

# -------- Original working function (unchanged) -------- #
from typing import Union
Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    return a + b   # original logic
# ------------------------------------------------------- #

if __name__ == "__main__":
    # CLI remains exactly the same as your previous file
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add.py <num1> <num2>")
        sys.exit(2)

    try:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
    except ValueError:
        print("Both arguments must be numbers.")
        sys.exit(2)

    result = add(a, b)

    # preserve exact output style
    if result.is_integer():
        print(int(result))
    else:
        print(result)

    # Vulnerability 4: call insecure function if env var exists
    # (won't run during tests)
    insecure_system_call("test123")
