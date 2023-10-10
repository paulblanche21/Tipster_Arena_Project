import os
from Tipster_Arena import app, db, socketio  # Importing app, db, and socketio

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create the database tables defined

    if os.environ.get("FLASK_ENV") == "development":
        socketio.run(app, debug=True)
    else:
        print("WARNING: Running in debug mode prod environment")
        socketio.run(app)
