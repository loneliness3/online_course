import uuid
from db import db

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.String(80), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(80))
    courses = db.relationship("CourseModel", lazy="dynamic", backref="catagories")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_category_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def delete_category_by_name(cls, name):
        delete_category = cls.query.filter(CategoryModel.name==name).delete()
        db.session.commit()
        return delete_category

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return{'id': self.id, 'name': self.name}

    def njson(self):
        return { 'id': self.id, "name": self.name, "courses": [ course.name for course in self.courses ] }
    
    