import json
import string
import random
from drivers import fb_driver, unsplash_driver
from core import image_generation

ingredients_file = "data/train.json"
raw_picture_file = "data/tmp_raw.jpg"
new_picture_file = "data/tmp_new.jpg"

trademarks = ["®", "hellmann", "sargento", "soy vay", "bertolli", "bacardi",
              "heinz", "gold medal", "spam", "wish bone"]

not_vegan = ["fillets", "chicken", "boar", "salmon", "beef", "fish",
             "scallops", "pork", "squid", "tamales", "salami",
             "calamari", "turkey", "mutton", "loin", "steak",
             "calf", "duck", "lamb", "tuna", "branzino",
             "snail", "bone", "shrimp"]

not_an_ingredient = ["hand"]


def has_trademarks(ingredient) -> bool:
    return any(x in ingredient for x in trademarks)


def is_not_vegan(ingredient) -> bool:
    return any(x in ingredient for x in not_vegan)


def is_not_an_ingredient(ingredient) -> bool:
    return any(x in ingredient for x in not_an_ingredient)


def should_be_removed(ingredient):
    ingredient = ingredient.lower()
    return is_not_an_ingredient(ingredient) or has_trademarks(ingredient) or is_not_vegan(ingredient)


ingredients = set()
with open(ingredients_file) as f:
    rid_list = json.load(f)

    for rid in rid_list:
        ingredients.update([string.capwords(ing) for ing in rid['ingredients']
                            if not should_be_removed(ing)])

ingredients_list = list(ingredients)
print("Unique ingredients:", len(ingredients_list))

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def get_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    return samples


def post_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    message = ""
    for i in range(k):
        message += f"{ordinal(i + 1)} ingredient: {samples[i]}\n"

    keywords = " ".join(samples)
    _, picture_text = unsplash_driver.get_picture_by_keywords(keywords, raw_picture_file)

    image_generation.label(raw_picture_file, samples, new_picture_file)
    post_text = f"{message}\n{picture_text}"
    print(post_text)

    # return fb_driver.post_picture(post_text, new_picture_file)


if __name__ == '__main__':
    samples = get_sample(k=40)
    print(samples)
    # image_generation.label(raw_picture_file, samples, new_picture_file)
