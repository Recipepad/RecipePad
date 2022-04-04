from app import db


class UserAccount(db.Model):
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"username: {self.username}, password: {self.password}"