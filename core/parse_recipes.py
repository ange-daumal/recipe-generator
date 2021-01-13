import pandas as pd
import numpy as np
from core import parse_ingredients
import json
import itertools
from tqdm import tqdm

output_csv = "data/ingredients_combinations.csv"
recipes_file = parse_ingredients.output_recipes_file

all_ingredients = parse_ingredients.get_ingredients_list()

df = pd.DataFrame(0, index=np.arange(len(all_ingredients)),
                  columns=all_ingredients)
ingredients_index = dict(zip(all_ingredients, np.arange(len(all_ingredients))))

with open(recipes_file, 'r') as recipes_fp:
    recipes = json.load(recipes_fp)


def get_ingredients_in_dict(ingredients):
    ingredients_in_dict = []
    for ingredient in ingredients:
        try:
            _ = ingredients_index[ingredient]
            ingredients_in_dict.append(ingredient)
        except KeyError:
            continue
    return ingredients_in_dict


def rm_unnamed(df):
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    return df


def apply_log(df):
    df = df.apply(np.log2)
    for col in df.columns:
        df[col][df[col] == -np.inf] = 0
    df = rm_unnamed(df)
    return df


def parse_recipes():
    for recipe in tqdm(recipes):
        ingredients_in_dict = get_ingredients_in_dict(recipe['ingredients'])

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
        rm_unnamed(df)
        return df
    except FileNotFoundError:
        return parse_recipes()


if __name__ == '__main__':
    df = get_ingredients_df()
    df = apply_log(df)
    print(df)
