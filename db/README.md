# Database (`db/`)

This directory houses the static database artifacts for the Coderunner CTF challenge (addresses issue #10 and supports #8).

## Files

| File | Description |
| --- | --- |
| `schema.sql` | Table definitions (`users`, `snippets`). |
| `seed.sql` | Initial data containing preloaded users and code snippets. |
| `init_db.py` | Python utility to recreate `database.db` from `schema.sql` and `seed.sql`. |
| `database.db` | Static, versioned SQLite database. Distributed inside the container at `/opt/app/instance/database.db`. |

## Credential Design

- Passwords are encrypted as unsalted **MD5**.
- `martin`'s hash (`5badcaf789d3d1d09794d8f021f40f0e`) corresponds to the common dictionary password `starwars`.
- Other users (`admin`, `clara`) use complex high-entropy passwords serving as realistic noise.
