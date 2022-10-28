from models.user import UserModel
from flask_restful import Resource, reqparse

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