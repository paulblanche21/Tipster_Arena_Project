import os
import os
import sys
from pathlib import Path

# Adding the path to the Tipster_Arena package to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Tipster_Arena.app import create_app, db, socketio  # Adjusted imports

app = create_app()  # Creating an app instance

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create the database tables defined

    if os.environ.get("FLASK_ENV") == "development":
        socketio.run(app, debug=True)
    else:
        print("WARNING: Running in debug mode in a"
              + "non-development environment")
        socketio.run(app)
