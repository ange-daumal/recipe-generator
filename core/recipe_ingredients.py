from parse import parse_recipes, parse_ingredients
import random
import numpy as np
import pandas as pd
from utils import filepaths, io_ops, emojis
import datetime

from drivers.fb_driver import FbDriver


class Ingredients:

    def __init__(self):
        self.ingredients_list = parse_ingredients.get_ingredients_list()
        self.ingredients_index = dict(zip(self.ingredients_list,
                                          np.arange(
                                              len(self.ingredients_list))))
        try:
            matrix_df = pd.read_csv(filepaths.ingredients_matrix)
            matrix_df = parse_recipes.rm_unnamed(matrix_df)
        except FileNotFoundError:
            # Create ingredients_list matrix
            matrix_df = parse_recipes.get_ingredients_df()
            matrix_df = parse_recipes.apply_log(matrix_df)
            matrix_df.to_csv(filepaths.ingredients_matrix, index=False)
        self.matrix_df = matrix_df
        self.access_token = io_ops.get_env_var("recipe_access_token")
        self.fb_reacts = ["NONE", "LIKE", "LOVE", "WOW", "HAHA", "SORRY",
                          "ANGRY"]

    def get_combination_for(self, first_ing, threshold: float = 0):
        combinable_ingredients = self.matrix_df[first_ing][
            self.matrix_df[first_ing] > threshold]
        combinable_ingredients = combinable_ingredients.reset_index()
        combinable_ingredients = combinable_ingredients['index'].apply(
            lambda x: self.ingredients_list[x])
        return combinable_ingredients.to_list()

    def get_random_versus_combination(self, set_length=2):
        first_ing = self.ingredients_list[
            random.randint(0, len(self.ingredients_list)) // 4]
        combinable_ingredients = self.get_combination_for(first_ing,
                                                          threshold=0.3)
        other_ings = random.sample(combinable_ingredients, set_length)
        return [first_ing, *other_ings]

    def get_good_combinations(self, n=10, set_length=3, n_best=50):
        first_ings = random.sample(self.ingredients_list, n)
        combinations = []

        for first_ing in first_ings:
            current = [first_ing]
            best_others_index = np.argsort(-self.matrix_df[first_ing])[:n_best]
            for i in random.sample(list(best_others_index), set_length - 1):
                current.append(self.ingredients_list[i])

            combinations.append(current)
        return combinations

    @staticmethod
    def add_to_pending(post_id, *ingredients):
        try:
            df = pd.read_csv(filepaths.versus_pending)
            df = parse_recipes.rm_unnamed(df)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["post_id", "first_ing", "second_ing",
                                       "third_ing", "post_timestamp"])

        row_dict = dict(zip(df.columns,
                            [post_id, *ingredients,
                             pd.to_datetime('now').replace(microsecond=0)]))

        df = df.append(row_dict, ignore_index=True)
        df.to_csv(filepaths.versus_pending, index=False)

    def update_score(self, ing1, ing2, score, verbose):
        ing1_index = self.ingredients_index[ing1]
        ing2_index = self.ingredients_index[ing2]

        previous = self.matrix_df[ing1][ing2_index]
        new = previous + score

        self.matrix_df[ing1][ing2_index] = new
        self.matrix_df[ing2][ing1_index] = new

        if verbose:
            print(f"({ing1}, {ing2}): {previous} => {new}")

    def compute_score(self, expired, reactions_count, verbose):
        love = reactions_count['LOVE']
        wow = reactions_count['WOW']
        haha = reactions_count['HAHA']
        total_points = love + wow + haha

        comment = "This versus has ended!\r\n"
        if total_points > 0:
            second_ing_score = love / total_points
            third_ing_score = wow / total_points

            if round(second_ing_score, 1) == round(third_ing_score, 1):
                comment = "It was tight: both foods had the same popularity!" \
                          f"\r\nCongratulations to " \
                    f"{expired[2]} and {expired[3]}!"

            elif second_ing_score > third_ing_score:
                comment = f"The favourite duo was " \
                    f"{expired[1]} and {expired[2]}! " \
                    f"Congratulations {emojis.emojis_pycode.orange_heart}"

            else:
                comment = f"The favourite duo was " \
                    f"{expired[1]} and {expired[3]} " \
                    f"{emojis.emojis_pycode.open_mouth} Congratulations!"
        else:
            second_ing_score = -0.2
            third_ing_score = -0.2
            comment = "None of the duest have been chosen. Too bad, they will" \
                      "have their chance with other foods!"

        self.update_score(expired[1], expired[2], second_ing_score, verbose)
        self.update_score(expired[1], expired[3], third_ing_score, verbose)

        return comment

    def _get_history(self):
        try:
            history = pd.read_csv(filepaths.versus_history)
        except FileNotFoundError:
            columns = ["post_id", "first_ing", "second_ing", "third_ing",
                       "post_timestamp"] + self.fb_reacts
            history = pd.DataFrame(columns=columns)
        return history

    def handle_pending(self, hours_threshold=48, verbose=True,
                       save_modifications=True):
        """
        # Facebook Reactions
        Facebook Reacts are of type enum {NONE, LIKE, LOVE, WOW, HAHA, SORRY, ANGRY}
        Care reactions are counted as Like reactions (ref https://developers.facebook.com/docs/graph-api/reference/v9.0/object/reactions)

        :param hours_threshold:
        :return:
        """
        try:
            df = pd.read_csv(filepaths.versus_pending)
        except FileNotFoundError:
            return True

        history = self._get_history()

        expired_versus = pd.to_datetime('now') - \
                         pd.to_datetime(df['post_timestamp']) > \
                         datetime.timedelta(hours=hours_threshold)

        fb = FbDriver()
        for expired in df[expired_versus].values:
            if verbose:
                print(expired)

            post_id = expired[0]
            reactions_count = dict.fromkeys(self.fb_reacts, 0)
            response = fb.get_post_reactions(post_id)

            if 'code' in response.keys() and response['code'] == 100:
                # Deleted post
                continue

            for react in response['data']:
                reactions_count[react['type']] += 1

            if verbose:
                print(response)
                print(reactions_count)

            # Update history
            history_content = dict(zip(df.columns, expired))
            history_content.update(reactions_count)
            history = history.append([history_content], ignore_index=True)

            # Update matrix
            comment = self.compute_score(expired, reactions_count, verbose)

            if save_modifications:
                history.to_csv(filepaths.versus_history, index=False)
                self.matrix_df.to_csv(filepaths.ingredients_matrix, index=False)
                fb.post_comment(post_id, comment)

        if save_modifications:
            # Delete computed versus
            df = df[~expired_versus]
            df.to_csv(filepaths.versus_pending, index=False)

        return True


if __name__ == '__main__':
    ingredients = Ingredients()
    # x = ingredients_list.get_random_versus_combination(set_length=3)
    # x = ingredients_list.get_good_combinations()
    # pprint(x)
    ingredients.handle_pending(hours_threshold=0,
                               save_modifications=not True)
