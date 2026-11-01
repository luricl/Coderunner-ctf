# Placeholder WSGI entrypoint for gunicorn.
#
# The real Coderunner app (editor UI, execution backend, DB-backed snippets)
# is built out in issues #4, #5, #6, #7, #8. This stub exists only so the
# Dockerfile built for issue #2 has something real to install and serve.
import os
from flask import Flask
from models import db

app = Flask(__name__)

db_path = os.environ.get(
    "CODERUNNER_DB_PATH",
    os.path.join(app.instance_path, "database.db")
)
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.get("/")
def index():
    return "Coderunner placeholder - app UI not wired up yet.", 200


if __name__ == "__main__":
    app.run()
