<<<<<<< HEAD
from flask_login import UserMixin
from flask_login import login_manager  # You should also adjust this import
from .import db, bcrypt  # Adjust this import as well
=======
from app import db, bcrypt  # Adjust the import according to your project structure
from flask_login import UserMixin
from flask_login import login_manager  # You should also adjust this import
from app import app  # Adjust this import as well
>>>>>>> 84f6b4b (Give me back my life)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
