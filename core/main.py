import random

from core import image_generation, parse_ingredients, cocktail_ingredients
from drivers import fb_driver, unsplash_driver
from utils import io_ops

recipe_rawpic_file = "data/recipe_raw.jpg"
recipe_newpic_file = "data/recipe_new.jpg"

cocktail_rawpic_file = "data/cocktail_raw.jpg"
cocktail_newpic_file = "data/cocktail_new.jpg"

ingredients_list = parse_ingredients.get_ingredients_list()

ordinal = lambda n: "%d%s" % (
    n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

page_id = io_ops.get_env_var("recipe_page_id")
recipe_access_token = io_ops.get_env_var("recipe_access_token")

cocktail_id = io_ops.get_env_var("cocktail_page_id")
cocktail_access_token = io_ops.get_env_var("cocktail_access_token")


def get_recipe_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    return samples


def post_recipe_sample(k=3):
    samples = random.sample(ingredients_list, k=k)
    message = ""
    for i in range(k):
        message += f"{ordinal(i + 1)} ingredient: {samples[i]}\n"

    keywords = " ".join(samples)
    success, picture_text = unsplash_driver.get_picture_by_keywords(keywords,
                                                                    recipe_rawpic_file)

    post_text = f"{message}\n{picture_text}"
    print(post_text)

    if success:
        image_generation.label(recipe_rawpic_file, samples, recipe_newpic_file)
        return fb_driver.post_picture(recipe_access_token, post_text,
                                      recipe_newpic_file)
    else:
        return fb_driver.post_text(page_id, recipe_access_token, post_text)


def post_cocktail_sample():
    flatten = lambda l: [item for sublist in l for item in sublist]

    sample = cocktail_ingredients.get_ingredients()
    message = cocktail_ingredients.generate_sentence(sample)

    keywords = ' '.join(flatten(sample))
    success, picture_text = unsplash_driver.get_picture_by_keywords(keywords,
                                                                    cocktail_rawpic_file)
    post_text = f"{message}\n{picture_text}"
    print(post_text)

    if success:
        image_generation.label(cocktail_rawpic_file,
                               list(map(lambda s: s.capitalize(),
                                        flatten(sample)[:3])),
                               cocktail_newpic_file)

        return fb_driver.post_picture(cocktail_access_token, post_text,
                                      cocktail_newpic_file)
    else:
        return fb_driver.post_text(page_id, cocktail_access_token, post_text)


if __name__ == '__main__':
    samples = get_recipe_sample(k=40)
    print(samples)
    #print(post_cocktail_sample())
