import os
from flask import Flask
from flask_restful import Api
from flask_uuid import FlaskUUID
from db import db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import datetime

# from security import authenticate, identity
from resources.user import CreateUser
from resources.course import CreateCourse, CourseLists, GetCourseByInstructorId, UpdateCourse, DeleteCourse, GetCourseByTopic, EnrollCourse
from resources.category import CreateCategory, DeleteCategory

load_dotenv()


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.debug = True

app.secret_key=os.getenv("SERECT_KEY")
app.config["JWT_EXPIRATION_DELTA"]= datetime.timedelta(minutes=120)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
try:
    prodURI = os.getenv('DB_URL')
    prodURI = prodURI.replace("postgresql://loneliness:ohdude@localhost:5432/online_db")
    app.config['SQLALCHEMY_DATABASE_URI'] = prodURI

except:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://loneliness:ohdude@localhost:5432/online_db"
app.config["SQLALCHEMY_MODIFICATION"] = False

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)

api = Api(app)

jwt = JWTManager(app)

@app.route('/')
def home():
    return {"Hey!": "Welcome"}
# @app.before_first_request
# def create_table():
#     db.create_all()

#endpoints for users
api.add_resource(CreateUser, "/users/create")

#endpoints for courses
api.add_resource(CreateCourse, "/courses/create")

#endpoints for tags
api.add_resource(CreateCategory, "/categories/create")

#endpoint for course update
api.add_resource(UpdateCourse, "/courses/update")

#endpoint for course delete
api.add_resource(DeleteCourse, "/courses/delete")

#endpoint for instructer viewing
api.add_resource(GetCourseByInstructorId, "/courses/getByInstructorId")

#endpoint for topic viewing
api.add_resource(GetCourseByTopic, "/courses/getByTopic")

#endpoint for enrolling a course
api.add_resource(EnrollCourse, "/courses/enroll")

#get all course endpoint
api.add_resource(CourseLists, "/courses/all")

#delete category
api.add_resource(DeleteCategory, "/categories/delete")

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug= True)