
import os
import sys
from pathlib import Path

from TipsterArena.app import create_app, db, socketio

sys.path.append(str(Path(__file__).resolve().parent.parent))

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    if os.environ.get("FLASK_ENV") == "development":
        socketio.run(app, debug=True)
    else:
        print("WARNING: Running in debug mode in a"
              + "non-development environment")
        socketio.run(app)
