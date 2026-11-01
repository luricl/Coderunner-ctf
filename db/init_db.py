#!/usr/bin/env python3
"""Build the static SQLite database using Flask-SQLAlchemy (Active Record pattern)."""
import sys
from pathlib import Path

# Add app directory to sys.path to import models
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
APP_DIR = ROOT_DIR / "app"
sys.path.insert(0, str(APP_DIR))

from flask import Flask
from models import db, User, Snippet

DB_PATH = BASE_DIR / "database.db"


def init_database():
    """Generates the static SQLite database artifact with predefined seed data."""
    if DB_PATH.exists():
        DB_PATH.unlink()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        # Create schema
        db.create_all()

        # Seed users (Active Record style)
        # Passwords stored as unsalted MD5:
        # admin: !Admin_Super_Sec2026!#$ (noise)
        # martin: starwars (target for lateral movement via SSH)
        # clara: c1@r4_k3y_unbr34k4bl3_x99 (noise)
        admin = User(
            id=1,
            username="admin",
            password_hash="b81c35e0cb8bdf19c669e5ecc2adbbe7",
            email="admin@coderunner.local",
            role="admin",
        )
        martin = User(
            id=2,
            username="martin",
            password_hash="5badcaf789d3d1d09794d8f021f40f0e",
            email="martin@coderunner.local",
            role="developer",
        )
        clara = User(
            id=3,
            username="clara",
            password_hash="f96d2ec4a85175c0bec2afbf4dd00f52",
            email="clara@coderunner.local",
            role="developer",
        )

        db.session.add_all([admin, martin, clara])
        db.session.commit()

        # Seed snippets (associated with users via relationship)
        s1 = Snippet(
            id=1,
            title="Healthcheck",
            code='import sys\nprint(f"System running Python {sys.version.split()[0]}")',
            author=admin,
        )
        s2 = Snippet(
            id=2,
            title="Fibonacci Memoized",
            code=(
                "def fib(n, memo={}):\n"
                "    if n in memo: return memo[n]\n"
                "    if n <= 1: return n\n"
                "    memo[n] = fib(n-1, memo) + fib(n-2, memo)\n"
                "    return memo[n]\n\n"
                "print([fib(i) for i in range(10)])"
            ),
            author=martin,
        )
        s3 = Snippet(
            id=3,
            title="Quick Sort",
            code=(
                "def quicksort(arr):\n"
                "    if len(arr) <= 1: return arr\n"
                "    pivot = arr[len(arr) // 2]\n"
                "    left = [x for x in arr if x < pivot]\n"
                "    middle = [x for x in arr if x == pivot]\n"
                "    right = [x for x in arr if x > pivot]\n"
                "    return quicksort(left) + middle + quicksort(right)\n\n"
                "print(quicksort([3, 6, 8, 10, 1, 2, 1]))"
            ),
            author=clara,
        )

        db.session.add_all([s1, s2, s3])
        db.session.commit()

    print(f"[+] Static database built successfully at {DB_PATH} using Flask-SQLAlchemy")


if __name__ == "__main__":
    init_database()
