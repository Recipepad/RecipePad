from app import db


class UserAccount(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    uid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"username: {self.username}, password: {self.password}"


class Recipe(db.Model):
    rid = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(45))
    cover_imgid = db.Column(db.Integer)
    description = db.Column(db.String(300))
    ingredients = db.Column(db.JSON)
    steps = db.Column(db.JSON)
    tags = db.Column(db.JSON)

    def __repr__(self):
        return f"rid: {self.rid}, title: {self.title}, cover_imgid: {self.cover_imgid}, " \
               f"description: {self.description}, ingredients: {self.ingredients}, steps: {self.steps}, " \
               f"tags: {self.tags}"