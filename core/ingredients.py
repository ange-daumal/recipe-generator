import json
import string

ingredients_file = "data/train.json"

trademarks = ["®", "hellmann", "sargento", "soy vay", "bertolli", "bacardi",
              "heinz", "gold medal", "spam", "wish bone"]

not_vegan = ["fillets", "chicken", "boar", "salmon", "beef", "fish",
             "scallops", "pork", "squid", "tamales", "salami",
             "calamari", "turkey", "mutton", "loin", "steak",
             "calf", "duck", "lamb", "tuna", "branzino",
             "snail", "bone", "shrimp", "goat"]

not_an_ingredient = ["hand", "xuxu"]


def has_trademarks(ingredient) -> bool:
    return any(x in ingredient for x in trademarks)


def is_not_vegan(ingredient) -> bool:
    return any(x in ingredient for x in not_vegan)


def is_not_an_ingredient(ingredient) -> bool:
    return any(x in ingredient for x in not_an_ingredient)


def should_be_removed(ingredient):
    if len(ingredient.split(" ")) > 3:
        return True
    ingredient = ingredient.lower()
    return is_not_an_ingredient(ingredient) or has_trademarks(ingredient) or is_not_vegan(ingredient)


def get_ingredients():
    ingredients = set()
    with open(ingredients_file) as f:
        rid_list = json.load(f)

        for rid in rid_list:
            ingredients.update([string.capwords(ing) for ing in rid['ingredients']
                                if not should_be_removed(ing)])

    ingredients_list = list(ingredients)
    print("Unique ingredients:", len(ingredients_list))
    return ingredients_list


