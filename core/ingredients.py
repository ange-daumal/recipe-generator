import json
import string
import random

ingredients_file = "data/train.json"


def has_trademarks(ingredient):
    return "®" in ingredient \
           or "hellmann" in ingredient \
           or "sargento" in ingredient \
           or "soy Vay" in ingredient \
           or "bertolli" in ingredient \
           or "bacardi" in ingredient


ingredients = set()
with open(ingredients_file) as f:
    rid_list = json.load(f)

    for rid in rid_list:
        ingredients.update([string.capwords(ing) for ing in rid['ingredients'] if not has_trademarks(ing)])

ingredients_list = list(ingredients)

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
def get_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    message = ""
    for i in range(k):
        message += f"{ordinal(i + 1)} ingredient: {samples[i]}\n"
    return message


if __name__ == '__main__':
    print(get_sample())
