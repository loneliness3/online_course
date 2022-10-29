from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_bcrypt import check_password_hash

class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        help="username cannot be empty.",
        required=  True
    )
    parser.add_argument(
        'password',
        type=str,
        help="username cannot be empty.",
        required = True
    )
    parser.add_argument(
        'user_type',
        type=str,
        help="user type cannot be empty",
        required = True
    )
   

    def post(self):
        data = CreateUser.parser.parse_args()

        old_user = UserModel.find_user_by_username(data["username"])
        if old_user:
            return {
                "status": 409,
                "message": "usename already exists."
            }

        new_user = UserModel(data["username"], data["password"], data["user_type"])

        try:
            new_user.save_to_db()
        except:
            return {
                "status": 500,
                "message": "an error occured while creating user."
            }, 500
        return {
            "status": 201,
            "message": "user created successfully."
        }, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="username cannot be empty."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="username cannot be empty."
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_user_by_username(data["username"])
       
        if user is None:
            return { "status": 401, "message": "Invalid Credential."}
        match_password = check_password_hash(user.password, data["password"])
        if not match_password:
            return { "status": 401, "message": "Invalid Credential."}
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {
            "status": 200,
            "access_token": access_token,
            "refresh_token": refresh_token
        }



   


class StudentEnrollCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "student_id",
        type=str,
        required=True,
        help="student id cannot be blank"
    )

    def post(self):
        data = StudentEnrollCourse.parser.parse_args()

        student = UserModel.find_user_by_user_id(data["student_id"])
        if student is None:
            return { "message": "student not found."}, 404
        return {
            "enrolled coures": [c.json() for c in student.courses]
        }