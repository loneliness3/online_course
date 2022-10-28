from models.user import UserModel
from flask_bcrypt import check_password_hash

def authenticate(username, password):
    user = UserModel.find_user_by_username(username)    
    if user:
        match_password = check_password_hash(user.password, password)
        if match_password:
            return user
    
def identity(payload):
    user_id = str(payload["identity"])
    return UserModel.find_user_by_user_id(user_id)
 