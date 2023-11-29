from werkzeug.security import generate_password_hash, check_password_hash

#from databaseKark import DataBase
from databaseHeroku import DataBase


class User:
    def __init__(self, user_id, e_mail, passwordHash, firstname, lastname, rolle, uuid, verified, active):
        self.user_id = user_id
        self.e_mail = e_mail
        self.passwordHash = passwordHash.replace("\'", "")
        self.firstname = firstname
        self.lastname = lastname
        self.rolle = rolle
        self.uuid = uuid
        self.verified = verified
        self.active = active
        self.is_authenticated = True
        self.is_active = True
        self.name = firstname + " " + lastname


    @staticmethod
    def login(username, password):

        with DataBase() as db:
            usr = db.getUser(username)[0]
            if usr:
                user = User(*usr)
                pwd = user.passwordHash.replace("\'", "")
                if check_password_hash(pwd, password):
                    return True
            return False


    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)


    def __str__(self):
        return  f'Id: {self.user_id}\n' + \
                f'Username:{self.e_mail}\n' + \
                f'Password Hash:{self.passordHash}\n' + \
                f'Uuid:{self.uuid}'


    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated


    def get(self, id):
        with DataBase() as db:
            user = User(*db.getUserById(id))
            if user:
                return user
            else:
                return False
            