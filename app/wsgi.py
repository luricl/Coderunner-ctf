# Placeholder WSGI entrypoint for gunicorn.
#
# The real Coderunner app (editor UI, execution backend, DB-backed snippets)
# is built out in issues #4, #5, #6, #7, #8. This stub exists only so the
# Dockerfile built for issue #2 has something real to install and serve.
from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "Coderunner placeholder - app UI not wired up yet.", 200


if __name__ == "__main__":
    app.run()
