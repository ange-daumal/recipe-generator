from flask import request, jsonify, Response
from api import flaskApp
from core.recipe_ingredients import Ingredients

ingredients = Ingredients()


@flaskApp.route("/", methods=["GET"])
def api_hello():
    return jsonify({'hello': 'world'})


@flaskApp.route("/ingredients", methods=["GET"])
def api_get_ingredients():
    return jsonify(ingredients.get_stats())


@flaskApp.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def api_get_ingredient(ingredient_id):
    return jsonify(ingredients.get_stats_by_ingredient_id(ingredient_id))


if __name__ == "__main__":
    flaskApp.run(debug=True, port=8046)
