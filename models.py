from app import db


class UserAccount(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    uid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"username: {self.username}, password: {self.password}, uid: {self.uid}"


"""
Examples:

ingredients = {
    "beef": "1 pound",
    "wine": "2 oz"
}

steps = [
        {
            "title": "step 1 Prepare A",
            "detail": "Put A into B",
            "imgid": "1001-step-1649429341-0"
        },
        {
            "title": "step 2 Prepare B",
            "detail": "Cut B into slices",
            "imgid": "1001-step-1649429341-1"
        },
        {
            "title": "step 2 Prepare B",
            "detail": "Cut B into slices",
            "imgid": "1001-step-1649429341-2"
        }
]

tags = {
    "tags": ["tag1", "tag2", "tag3"]
}
"""
class Recipe(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
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


class UserRecipe(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    rid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    def __repr__(self):
        return f"uid: {self.username}, rid: {self.password}"


class UserBookmark(db.Model):
    uid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    rid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    def __repr__(self):
        return f"uid: {self.uid}, rid: {self.rid}"