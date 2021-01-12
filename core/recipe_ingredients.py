import json
import re
import sys
import unicodedata

import nltk
from utils import io_ops
from collections import Counter

# Get recipes from multiple sources ;
# AllRecipes.com, Epicurious.com, Foodnetwork.com

ingredients_files = [f"data/recipe-box/recipes_raw_nosource_{src}.json"
                     for src in ["ar", "epi", "fn"]]

output_file = f"data/ingredients_list.pickle"
output_file_test = f"data/ingredients_list_test.pickle"

nltk.download('stopwords')

trademarks = ["®", "hellmann", "sargento", "soy vay", "bertolli", "bacardi",
              "heinz", "gold medal", "spam", "wish bone", 'sugarcraft']

not_vegan = ["fillets", "chicken", "boar", "salmon", "beef", "fish",
             "scallops", "pork", "squid", "tamales", "salami",
             "calamari", "turkey", "mutton", "loin", "steak",
             "calf", "duck", "lamb", "tuna", "branzino",
             "snail", "bone", "shrimp", "goat", "veal",
             'curd',  # <- lait caillé
             'lobster', 'mentaiko', 'lard', 'buttermilk',
             'halibut', 'casing', 'casings', 'crab', 'crabmeat',
             'egg', 'cheese', 'black angus', 'shells',
             # cheeses
             'cresenza', 'clams',
             # charcuteries
             'cotechino',
             ]

not_an_ingredient = ["hand", "xuxu", "coloring", "baton", 'water',
                     'erythritol', 'equipment', 'available',
                     'x sheets', 'ice', 'oxtail', 'garnish', 'ingredient',
                     'canning', 'fruitcake', 'slotted spoon',

                     # wtf words
                     'ready', 'use',
                     # recipe, not ingredient
                     'cilantro mint chutney',
                     'dressing'
                     ]

measures = [
    'cup', 'can', 'teaspoon', 'tsp', 'tablespoon', 'tbsp', 'pound', 'lb', 'jar',
    'bottle', 'stick', 'about', 'pounds', 'cups', 'pinch', 'appx', 'half',
    'optional', 'milliter', 'micro', 'ounce', 'small', 'large', 'medium',
    'envelope', 'ear', 'piece', 'drops', 'oz', 'bunch', 'slice', 'spoonful',
    'advertisement', 'clove', 'pinches', 'inch', 'dash', 'gallon',
    'bag', 'cheesecloth', 'pint', 'couple', 'dashe',
    'ml', 'cl', 'g', 'kg', 'gram', 'strip', 'pod', 'double',
    'decoration', 'tb', 'accompaniment', 'ring', 'shot',
    'quarter', 'chunk', 'cube', 'deciliter', 'preserve', 'inche',
    'head',

]

prep_details = [
    'diced', 'stewed', 'chopped', 'crumbled', 'peeled', 'minced', 'fresh',
    'divided', 'cooked', 'washed', 'softened', 'sliced', 'deveined', 'shaken',
    'fine', 'seasoned', 'rest', 'cold', 'mashed', 'overripe', 'hot',
    'cubed', 'uncooked', 'bottled', 'quartered', 'whole', 'wheat', 'packed',
    'taste', 'semi', 'sweet', 'semisweet', 'unsweetened',
    'assorted', 'pitted', 'plus', 'purpose', 'kosher', 'canned',
    'finely', 'toasted', 'frozen', 'mixed', 'cut', 'squeezed', 'cracked',
    'halved', 'roasted', 'grilled', 'dried', 'freshly', 'ground', 'coarse',
    'beaten', 'blend', 'blended', 'seeded', 'grated', 'chilled', 'garnish',
    'discarded', 'powdered', 'cooled', 'sifted', 'drained', 'granulated',
    'skinned', 'sprinkles', 'ripe', 'extra', 'virgin', 'brewed', 'unsalted',
    'bittersweet', 'good', 'quality', 'coursely', 'french', 'italian', 'recipe',
    'brine', 'currants', 'icing', 'royal', 'shortening', 'corarsely',
    'quart', 'spiced', 'prepared', 'dollop', 'neely', 'allspice',
    'one', 'two', 'three', 'four', 'crystallized', 'puree', 'sized',
    'israeli', 'sprigs', 'snipped', 'thickly', 'frosting', 'style',
    'confectioners', 'cooking', 'spray', 'thinly', 'vegan',
    'stilton', 'dry', 'crusty', 'pickled', 'grained', 'unfiltered',
    'little', 'strong', 'sizes', 'nonstick', 'flaky', 'blanched', 'silvered',
    'crushed', 'idiazábal', 'pibkcling', 'pimm', 'sweetened', 'drizzling',
    'condensed', 'grain', 'coarsely', 'unsprayed', 'reduced',
    'china', 'halves', 'distilled', 'purchased', 'soft', 'desired',
    'slivered', 'hulled', 'shredded', 'melted', 'rolled', 'evaporated',
    'salted', 'nonfat', 'pickling', 'delicata', 'unflavored',
    'low', 'lowfat',
    'natural', 'plain', 'light', 'miniature', 'lengthwise', 'drippings',
    'clarified', 'topping', 'stuffed', 'filling', 'non', 'fat', 'spent',
    'vital', 'warm', 'hard', 'boiled', 'shelled', 'sauteed', 'sharp',
    'package', 'packaged', 'master', 'mixture', 'precooked', 'rounded',
    'paste', 'heaping', 'cheap', 'burmese', 'bran', 'hardening', 'splash',
    'flax', 'glucose', 'wild', 'spread', 'dried', 'decorating',
    'reserved', 'six', 'seven', 'eight', 'nine', 'ten', 'premium',
    'cube', 'mix', 'container', 'baby', 'bunches',
    'aged', 'new', 'roughly', 'reduction', 'hickory', 'jarred', 'sour',
    'dayold', 'brush', 'extralarge', 'extra', 'large', 'rinsed',
    'gratedfresh', 'imported', 'several', 'fillings', 'organic',
    'candies', 'matchsticks', 'together', 'slab', 'smokehouse',
    'loosely', 'fronds', 'cleaned', 'grade', 'grape', 'herbed',
    'lightened', 'crustless', 'sourdough', 'peel', 'traditional',
    'preserved', 'candy', 'brunoised', 'disk', 'best',
    'process', 'food', 'candied', 'packages', 'long', 'browned',
    # type of foods
    'heavy', 'long', 'gluten', 'free', 'fully', 'smoked',
    # countrys
    'english', 'asian', 'bulgarian', 'spanish',
    # brands
    'myers', 'aarti',

]

translator = dict()
for i in range(sys.maxunicode):
    if unicodedata.category(chr(i)).startswith('P'):
        translator.update({i: " "})


def has_trademarks(ingredient) -> bool:
    return any(x in ingredient for x in trademarks)


def is_not_vegan(ingredient) -> bool:
    return any(x in ingredient for x in not_vegan)


def is_not_an_ingredient(ingredient) -> bool:
    return any(x in ingredient for x in not_an_ingredient)


def should_be_removed(ingredient):
    if len(ingredient.split(" ")) > 2:
        return True
    ingredient = ingredient.lower()
    return is_not_an_ingredient(ingredient) or has_trademarks(
        ingredient) or is_not_vegan(ingredient)


def filter_ingredient(ingredient, stop_ingredient_words, test=False):
    """
    From sentence '2 pounds red potatoes, diced with peel ADVERTISEMENT'
    to 'red potatoes'
    :param ingredient:
    :return:
    """
    ing = ingredient.lower()

    if is_not_an_ingredient(ing) \
            or has_trademarks(ing) \
            or is_not_vegan(ing):
        return ""

    if test:
        print(ing)

    ing = ing.split(",")[0]  # remove what is after ,
    ing = ing.split("(")[0]  # remove what is after (
    ing = ing.split(" or ")[0]  # remove what is after ' or '

    ing = ing.translate(translator)  # remove punctuation
    ing = re.sub(r'[\d]', ' ', ing)  # remove digits

    final_ing = ""
    nb_words = 0
    for i in ing.split(' '):
        i = i.strip()
        if i and len(i) > 1 and i not in stop_ingredient_words:
            final_ing += f" {i}"
            nb_words += 1

    return final_ing.strip() if nb_words < 4 else ""


def process_recipe_box_ingredients():
    stop_ingredient_words = measures + \
                            [f"{m}s" for m in measures] + \
                            prep_details + \
                            list(nltk.corpus.stopwords.words('english'))
    ingredients = Counter()
    for ingredients_file in ingredients_files:
        with open(ingredients_file) as f:
            recipes = json.load(f)

            for recipe in recipes.values():

                if not recipe:
                    continue

                for recipe_ing in recipe['ingredients']:
                    ing = filter_ingredient(recipe_ing,
                                            stop_ingredient_words)
                    if ing:
                        ingredients.update([ing])

    ingredients_list = [x[0] for x in ingredients.most_common(950)]

    io_ops.save_obj(ingredients_list, output_file)

    return ingredients_list


def get_ingredients_list():
    return io_ops.load_obj(output_file) or process_recipe_box_ingredients()


if __name__ == '__main__':
    test = not True
    l = process_recipe_box_ingredients()
    print(get_ingredients_list()[:10])
