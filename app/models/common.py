from app.models import db


class User(db.Model):
    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)