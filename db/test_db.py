#!/usr/bin/env python3
"""Automated test for Issue #10 and Issue #14: Database schema and hash cracking."""
import hashlib
import sqlite3
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def test_database_structure():
    assert DB_PATH.exists(), f"Database file {DB_PATH} not found!"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    assert "users" in tables, "Table 'users' is missing!"
    assert "snippets" in tables, "Table 'snippets' is missing!"

    # Verify users
    cursor.execute("SELECT username, password_hash, role FROM users WHERE username='martin'")
    martin = cursor.fetchone()
    assert martin is not None, "User 'martin' not found in users table!"
    username, pass_hash, role = martin
    assert pass_hash == "5badcaf789d3d1d09794d8f021f40f0e", f"Unexpected hash for martin: {pass_hash}"
    assert hashlib.md5(b"starwars").hexdigest() == pass_hash, "Hash does not match MD5('starwars')!"

    # Verify snippets
    cursor.execute("SELECT COUNT(*) FROM snippets")
    count = cursor.fetchone()[0]
    assert count >= 3, f"Expected at least 3 snippets, got {count}"

    conn.close()
    print("[PASS] Database schema and preloaded data verified.")


def test_hash_cracking():
    target_hash = "5badcaf789d3d1d09794d8f021f40f0e"
    wordlist = ["admin", "123456", "password", "coderunner", "starwars", "dragon"]

    with tempfile.NamedTemporaryFile("w", delete=False) as hf, tempfile.NamedTemporaryFile("w", delete=False) as wf:
        hf.write(target_hash + "\n")
        hf.flush()
        wf.write("\n".join(wordlist) + "\n")
        wf.flush()

        # Test John the Ripper if installed
        john_proc = subprocess.run(["which", "john"], capture_output=True)
        if john_proc.returncode == 0:
            res = subprocess.run(
                ["john", "--format=raw-md5", f"--wordlist={wf.name}", hf.name],
                capture_output=True,
                text=True,
            )
            show = subprocess.run(
                ["john", "--format=raw-md5", "--show", hf.name],
                capture_output=True,
                text=True,
            )
            assert "starwars" in show.stdout, f"John failed to crack hash: {show.stdout}"
            print("[PASS] John the Ripper cracked hash successfully (password: starwars).")

    print("[PASS] Hash cracking verified.")


if __name__ == "__main__":
    test_database_structure()
    test_hash_cracking()
    print("[SUCCESS] All tests for Issue #10 and Issue #14 passed!")
