from core import parse_recipes, parse_ingredients
import random
import numpy as np

class Ingredients:

    def __init__(self):
        self.ingredients = parse_ingredients.get_ingredients_list()
        df = parse_recipes.get_ingredients_df()
        df = parse_recipes.apply_log(df)
        print(df.columns)
        self.df = df

    def get_combination_for(self, first_ing, threshold=0):
        combinable_ingredients = self.df[first_ing][
            self.df[first_ing] > threshold]
        combinable_ingredients = combinable_ingredients.reset_index()
        combinable_ingredients = combinable_ingredients['index'].apply(
            lambda x: self.ingredients[x])
        return combinable_ingredients.to_list()

    def get_random_versus_combination(self, set_length=2):
        first_ing = self.ingredients[random.randint(0, len(self.ingredients))]
        combinable_ingredients = self.get_combination_for(first_ing)
        other_ings = random.sample(combinable_ingredients, set_length - 1)
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


if __name__ == '__main__':
    from pprint import pprint
    ingredients = Ingredients()
    #x = ingredients.get_random_versus_combination(set_length=3)
    x = ingredients.get_best_combinations()
    pprint(x)
