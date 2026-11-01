#!/usr/bin/env python3
"""Build the static SQLite database using Flask-SQLAlchemy and Faker (Active Record pattern).

Uses a fixed random seed (1337) to guarantee 100% deterministic reproducibility across runs,
while populating realistic developer accounts, diverse snippets, and subtle CTF lore.
"""
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add app directory to sys.path to import models
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
APP_DIR = ROOT_DIR / "app"
sys.path.insert(0, str(APP_DIR))

from faker import Faker
from flask import Flask
from models import Snippet, User, db

DB_PATH = BASE_DIR / "database.db"

# Sample realistic Python snippets for the platform
REALISTIC_SNIPPETS = [
    {
        "title": "JWT Token Validator",
        "code": (
            "import hmac\nimport hashlib\nimport base64\n\n"
            "def verify_signature(header_b64, payload_b64, signature, secret):\n"
            "    data = f'{header_b64}.{payload_b64}'.encode()\n"
            "    expected = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()\n"
            "    return hmac.compare_digest(signature, expected)\n"
        ),
    },
    {
        "title": "LRU Memory Cache Decorator",
        "code": (
            "from collections import OrderedDict\nfrom functools import wraps\n\n"
            "def simple_lru(maxsize=128):\n"
            "    def decorator(func):\n"
            "        cache = OrderedDict()\n"
            "        @wraps(func)\n"
            "        def wrapper(*args):\n"
            "            if args in cache:\n"
            "                cache.move_to_end(args)\n"
            "                return cache[args]\n"
            "            result = func(*args)\n"
            "            cache[args] = result\n"
            "            if len(cache) > maxsize:\n"
            "                cache.popitem(last=False)\n"
            "            return result\n"
            "        return wrapper\n"
            "    return decorator\n"
        ),
    },
    {
        "title": "CSV Stream Parser",
        "code": (
            "import csv\nfrom io import StringIO\n\n"
            "def parse_user_export(stream_data):\n"
            "    f = StringIO(stream_data)\n"
            "    reader = csv.DictReader(f)\n"
            "    return [row for row in reader if row.get('active') == 'true']\n"
        ),
    },
    {
        "title": "Rate Limiter Leaky Bucket",
        "code": (
            "import time\n\n"
            "class LeakyBucket:\n"
            "    def __init__(self, capacity, leak_rate):\n"
            "        self.capacity = capacity\n"
            "        self.leak_rate = leak_rate\n"
            "        self.water = 0\n"
            "        self.last_check = time.time()\n\n"
            "    def add_drop(self):\n"
            "        now = time.time()\n"
            "        leaked = (now - self.last_check) * self.leak_rate\n"
            "        self.water = max(0, self.water - leaked)\n"
            "        self.last_check = now\n"
            "        if self.water < self.capacity:\n"
            "            self.water += 1\n"
            "            return True\n"
            "        return False\n"
        ),
    },
]


def init_database():
    """Generates the static SQLite database artifact with Faker seed data."""
    if DB_PATH.exists():
        DB_PATH.unlink()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Initialize Faker with fixed seed for deterministic reproducibility
    fake = Faker()
    Faker.seed(1337)

    with app.app_context():
        # Create schema
        db.create_all()

        # 1. CTF Key Users:
        # Admin (noise with high entropy password)
        admin = User(
            id=1,
            username="admin",
            password_hash="b81c35e0cb8bdf19c669e5ecc2adbbe7",
            email="admin@coderunner.local",
            role="admin",
            created_at=datetime(2026, 1, 10, 8, 30, tzinfo=timezone.utc),
        )

        # Martin: Target user for lateral movement via SSH (Issue #10, #12, #14)
        # Password: starwars -> MD5: 5badcaf789d3d1d09794d8f021f40f0e
        martin = User(
            id=2,
            username="martin",
            password_hash="5badcaf789d3d1d09794d8f021f40f0e",
            email="martin@coderunner.local",
            role="developer",
            created_at=datetime(2026, 1, 15, 9, 45, tzinfo=timezone.utc),
        )

        users_list = [admin, martin]

        # 2. Faker Noise Developers (Realistic team members)
        noise_usernames = ["clara", "elena", "lucas", "diego", "sarah"]
        for i, username in enumerate(noise_usernames, start=3):
            # Complex, uncrackable random hash for noise users
            random_pw = fake.password(length=32, special_chars=True)
            pass_hash = hashlib.md5(random_pw.encode()).hexdigest()
            created = fake.date_time_between(
                start_date="-180d", end_date="-10d", tzinfo=timezone.utc
            )
            user = User(
                id=i,
                username=username,
                password_hash=pass_hash,
                email=f"{username}@coderunner.local",
                role="developer",
                created_at=created,
            )
            users_list.append(user)

        db.session.add_all(users_list)
        db.session.commit()

        # 3. Snippets - including CTF lore hints by Martin!
        snippets_list = []

        # Snippet 1: Martin's backup automation draft (lore clue pointing to backy.sh)
        s_martin_lore = Snippet(
            id=1,
            title="Backup Automation Helper (Draft)",
            code=(
                "# Martin's dev notes:\n"
                "# Testing directory bundling before handing tasks over to backy.sh\n"
                "# Remember: /usr/local/bin/backy.sh runs as root with sudo privileges.\n\n"
                "import os, glob\n\n"
                "def list_project_sources(base_dir='/opt/app'):\n"
                "    return glob.glob(f'{base_dir}/**/*.py', recursive=True)\n\n"
                "if __name__ == '__main__':\n"
                "    print(f'Found {len(list_project_sources())} source files.')\n"
            ),
            author=martin,
            created_at=datetime(2026, 2, 1, 14, 20, tzinfo=timezone.utc),
        )
        snippets_list.append(s_martin_lore)

        # Snippet 2: Admin System Diagnostics
        s_admin = Snippet(
            id=2,
            title="System Environment Diagnostics",
            code=(
                "import sys\nimport platform\n\n"
                "print(f'Python Version: {platform.python_version()}')\n"
                "print(f'Platform: {platform.system()} {platform.release()}')\n"
            ),
            author=admin,
            created_at=datetime(2026, 1, 11, 10, 0, tzinfo=timezone.utc),
        )
        snippets_list.append(s_admin)

        # Snippets 3+: Distributed among Faker developers
        for idx, snip_data in enumerate(REALISTIC_SNIPPETS, start=3):
            author_user = users_list[idx % len(users_list)]
            s = Snippet(
                id=idx,
                title=snip_data["title"],
                code=snip_data["code"],
                author=author_user,
                created_at=fake.date_time_between(
                    start_date="-90d", end_date="-5d", tzinfo=timezone.utc
                ),
            )
            snippets_list.append(s)

        db.session.add_all(snippets_list)
        db.session.commit()

    print(
        f"[+] Static database generated at {DB_PATH} ({len(users_list)} users, {len(snippets_list)} snippets)"
    )


if __name__ == "__main__":
    init_database()
