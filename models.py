from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect to database."""

    db.app = app
    db.init_app(app)

class User(db.model):

    __tablename__ = 'users'
    id = db.column(db.Integer, primary_key=True, Autoincrement=True)

    username = db.column(db.Text, nullable=False, unique=True)

    password = db.column(db.Text, nullable=False)

    # @classmethod
    # def register(cls, username, pwd):
    #     """register user with hashed password & return user."""

    #     hashed = bcrypt.        generate_password_hash(pwd)
    #     hashed_utf8 = hashed.decode
    #     ("utf8")

    #     #return instance of user w/username and hashed pwd
    #     return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False