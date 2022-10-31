from models.category import CategoryModel
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required

class CreateCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type = str,
        required = True,
        help = "Name cannot be blank"
    )

    @jwt_required()
    def post(self):
        data = CreateCategory.parser.parse_args()

        new_tag = CategoryModel(data["name"])

        try:
            new_tag.save_to_db()
        
        except:
            return {
                "message": "error occured while creating tag",
                "status": 500
            }, 500
        
        return{
            "message": "crated tag successfully"
        }

class DeleteCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type = str,
        required = True,
        help = 'cannot be blank'
    )

    @jwt_required()
    def post(self):
        data = DeleteCategory.parser.parse_args()

        old_category = CategoryModel.find_category_by_name(data["name"])

        if old_category is not None:
            return {"status": 404, "message": "category not found"}, 404

        try:
            CategoryModel.delete_category_by_name(data["name"])
        except:
            return { "status": 500, "message": "an error occured while deleting catagory." }, 500
        return { "status": 201, "message": "category successfully deleted." }, 201

class CategoryList(Resource):

    def get(self):
        catagories = CategoryModel.get_all_categories()
        return {
            "categories": [catagory.njson() for catagory in catagories]
        }

    

