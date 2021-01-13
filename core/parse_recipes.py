import pandas as pd
import numpy as np
from core import parse_ingredients
import json
import itertools
from tqdm import tqdm

output_csv = "data/ingredients_combinations.csv"


def _get_ingredients_in_dict(ingredients, ingredients_index):
    ingredients_in_dict = []
    for ingredient in ingredients:
        try:
            _ = ingredients_index[ingredient]
            ingredients_in_dict.append(ingredient)
        except KeyError:
            continue
    return ingredients_in_dict


def _rm_unnamed(df):
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    return df


def apply_log(df):
    df = df.apply(np.log2)
    for col in df.columns:
        df[col][df[col] == -np.inf] = 0
    df = _rm_unnamed(df)
    return df


def parse_recipes(ingredients_list):
    df = pd.DataFrame(0, index=np.arange(len(ingredients_list)),
                         columns=ingredients_list)
    ingredients_index = dict(
        zip(ingredients_list, np.arange(len(ingredients_list))))

    recipes_file = parse_ingredients.output_recipes_file
    with open(recipes_file, 'r') as recipes_fp:
        recipes = json.load(recipes_fp)

    for recipe in tqdm(recipes):
        ingredients_in_dict = _get_ingredients_in_dict(recipe['ingredients'],
                                                       ingredients_index)

        combinations = itertools.combinations(ingredients_in_dict, 2)
        for ing1, ing2 in combinations:
            index_ing1 = ingredients_index[ing1]
            index_ing2 = ingredients_index[ing2]
            df[ing1][index_ing2] += 1
            df[ing2][index_ing1] += 1

    df.to_csv(output_csv)
    return df


def get_ingredients_df():
    try:
        df = pd.read_csv(output_csv)
        df = _rm_unnamed(df)
        return df
    except FileNotFoundError:
        all_ingredients = parse_ingredients.get_ingredients_list()
        return parse_recipes(all_ingredients)


if __name__ == '__main__':
    df = get_ingredients_df()
    df = apply_log(df)
    print(df)
