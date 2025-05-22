from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

db = SQLAlchemy()


class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Text, unique=True, nullable=False)
    time_free = db.Column(db.Date)
    iks = db.Column(db.Integer)
    age = db.Column(db.Integer)
    is_org = db.Column(db.Text)
    bet = db.Column(db.Text)
    links_expired = db.Column(db.Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Domain {self.domain}>'
