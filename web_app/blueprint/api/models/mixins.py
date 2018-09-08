from ...extension import db
from sqlalchemy.sql import func

class BasicMixin():

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp(), 
        onupdate=func.current_timestamp())

    def save(self):
        if self.id is None:
            db.session.add(self)
        db.session.commit()