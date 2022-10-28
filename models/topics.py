from db import db
import uuid

class TopicModel(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.String(80),  primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_topic_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def json(self):
        return {"id": self.id, "name": self.name}
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()