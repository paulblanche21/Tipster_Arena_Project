from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
from TipsterArena.app import app as flask_app
from TipsterArena.extensions import db as _db
from TipsterArena.config import DevelopmentConfig


@pytest.fixture(scope='module')
def app():
    """Instance of Main flask app"""
    flask_app.config.from_object(DevelopmentConfig)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with flask_app.app_context():
        yield flask_app


@pytest.fixture(scope='module')
def db(app: Flask):
    """
    Creates a new database for the test duration.
    """
    _db.app = app
    _db.create_all()

    yield _db  # this is where the testing happens!

    _db.drop_all()


@pytest.fixture(scope='function')
def session(db: SQLAlchemy):
    """
    Creates a new database session for a test duration.
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
