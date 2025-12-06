# add.py  -- intentionally insecure example for static-analysis demo
# DO NOT USE IN PRODUCTION. For lab/testing only.

import os
import sys
import subprocess
import sqlite3
import pickle

# Hardcoded secret (Sonar will flag as hardcoded credential)
API_KEY = "SECRET_API_KEY_12345"

def add_numbers(a, b):
    """Simple add function (keeps original functionality)."""
    try:
        return float(a) + float(b)
    except Exception:
        # poor error handling (could be improved)
        return None

def run_user_command(cmd):
    """
    Vulnerable command execution: using shell=True with user input (command injection).
    Sonar will flag subprocess usage with shell=True as dangerous.
    """
    # Danger: shell=True allows command injection if `cmd` comes from user
    subprocess.call(cmd, shell=True)

def insecure_sql_insert(name, value):
    """
    Vulnerable SQL: string concatenation leads to SQL injection.
    Sonar will flag string-built SQL queries.
    """
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    # Danger: do not build queries by concatenation
    query = "INSERT INTO items (name, value) VALUES ('%s', '%s')" % (name, value)
    cur.execute(query)
    conn.commit()
    conn.close()

def insecure_deserialize(data_path):
    """
    Loads pickled data from a file without validation. This is unsafe because
    pickle can execute arbitrary code on load.
    Sonar will flag insecure deserialization.
    """
    if not os.path.exists(data_path):
        return None
    with open(data_path, "rb") as f:
        obj = pickle.load(f)   # insecure deserialization
    return obj

def write_secret_file(secret):
    """
    Writes a secret to disk with world-readable permissions (0o644).
    Storing secrets on disk and weak permissions are bad practice.
    """
    p = "secret.txt"
    with open(p, "w") as f:
        f.write(secret)
    # make file world-readable (insecure)
    os.chmod(p, 0o644)

def main():
    """
    CLI behavior (intentionally insecure): supports:
      - add <a> <b>             => prints sum
      - cmd "<shell command>"   => runs user command (vulnerable)
      - insert <name> <value>   => insecure SQL insert
      - load <pickle-file>      => insecure deserialization
      - secret <text>           => write secret to disk
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  add <a> <b>")
        print('  cmd "<shell command>"')
        print("  insert <name> <value>")
        print("  load <pickle-file>")
        print("  secret <text>")
        sys.exit(2)

    action = sys.argv[1].lower()

    if action == "add" and len(sys.argv) == 4:
        a, b = sys.argv[2], sys.argv[3]
        print("Result:", add_numbers(a, b))
        return

    if action == "cmd" and len(sys.argv) == 3:
        cmd = sys.argv[2]
        print("Running command (unsafe):", cmd)
        run_user_command(cmd)
        return

    if action == "insert" and len(sys.argv) == 4:
        name, value = sys.argv[2], sys.argv[3]
        insecure_sql_insert(name, value)
        print("Inserted (insecurely).")
        return

    if action == "load" and len(sys.argv) == 3:
        path = sys.argv[2]
        obj = insecure_deserialize(path)
        print("Loaded object:", obj)
        return

    if action == "secret" and len(sys.argv) == 3:
        secret = sys.argv[2]
        write_secret_file(secret)
        print("Wrote secret to secret.txt (insecure).")
        return

    print("Invalid arguments. See usage above.")

if __name__ == "__main__":
    main()
