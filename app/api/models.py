from .extension import db


#### USER MODEL ########
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)

    def _repr_(self):
        return (
            f"User(name = {self.name}, email = {self.email}, password={self.password})"
        )
###########