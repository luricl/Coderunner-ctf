# Coderunner-ctf

## Repository layout

| Path           | Purpose                                                             |
| -------------- | ------------------------------------------------------------------- |
| `app/`         | Vulnerable Flask web app, Dockerfile, gunicorn + sshd, system users |
| `db/`          | SQLite schema and seed data (the credential store to be looted)     |
| `lab/`         | CTF content: flags, privesc backup script, sudoers, hardening       |
| `docs/`        | Solver walkthrough (spoilers), safety notice, provenance            |
| `compose.yaml` | Single `app` service, loopback bind, configurable ports             |

Each directory has its own `README.md` describing what belongs there and the
issues that build it.

## Run / reset

```bash
docker compose up --build -d   # start the lab
docker compose down -v         # tear down and reset
```
