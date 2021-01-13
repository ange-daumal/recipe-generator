from parse import parse_recipes, parse_ingredients
import random
import numpy as np
import pandas as pd
from utils import data_paths
import datetime


class Ingredients:

    def __init__(self):
        self.ingredients = parse_ingredients.get_ingredients_list()
        try:
            df = pd.read_csv(data_paths.ingredients_matrix)
            df = parse_recipes.rm_unnamed(df)
        except FileNotFoundError:
            # Create ingredients matrix
            df = parse_recipes.get_ingredients_df()
            df = parse_recipes.apply_log(df)
            df.to_csv(data_paths.ingredients_matrix, index=False)
        self.df = df

    def get_combination_for(self, first_ing, threshold=0):
        combinable_ingredients = self.df[first_ing][
            self.df[first_ing] > threshold]
        combinable_ingredients = combinable_ingredients.reset_index()
        combinable_ingredients = combinable_ingredients['index'].apply(
            lambda x: self.ingredients[x])
        return combinable_ingredients.to_list()

    def get_random_versus_combination(self, set_length=2):
        first_ing = self.ingredients[random.randint(0,
                                                    len(self.ingredients)) // 4]
        combinable_ingredients = self.get_combination_for(first_ing)
        other_ings = random.sample(combinable_ingredients, set_length)
        return [first_ing, *other_ings]

    def get_good_combinations(self, n=10, set_length=3):
        first_ings = random.sample(self.ingredients, n)
        combinations = []

        for first_ing in first_ings:
            current = [first_ing]
            n_selected = set_length * 8
            best_others_index = np.argsort(-self.df[first_ing])[:n_selected]
            for i in random.sample(list(best_others_index), set_length - 1):
                current.append(self.ingredients[i])

            combinations.append(current)
        return combinations

    @staticmethod
    def add_to_pending(post_id, *ingredients):
        try:
            df = pd.read_csv(data_paths.versus_pending)
            df = parse_recipes.rm_unnamed(df)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["post_id", "first_ing", "second_ing",
                                       "third_ing", "post_timestamp"])

        row_dict = dict(zip(df.columns,
                            [post_id, *ingredients,
                             pd.to_datetime('now').replace(microsecond=0)]))

        df = df.append(row_dict, ignore_index=True)
        df.to_csv(data_paths.versus_pending, index=False)

    def handle_pending(self, hours_threshold=48):
        try:
            df = pd.read_csv(data_paths.versus_pending)
        except FileNotFoundError:
            return True
        expired_versus = pd.to_datetime('now') - \
                         pd.to_datetime(df['post_timestamp']) > \
                         datetime.timedelta(hours=hours_threshold)

        for expired in df[expired_versus]:
            # Get FB reactions
            # Update history
            # Update matrix
            # Delete expired
            pass


if __name__ == '__main__':
    from pprint import pprint

    ingredients = Ingredients()
    # x = ingredients.get_random_versus_combination(set_length=3)
    # x = ingredients.get_good_combinations()
    # pprint(x)
    print(ingredients.df)
