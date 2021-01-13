# Input data
ingredients_files = [f"data/recipe-box/recipes_raw_nosource_{src}.json"
                     for src in ["ar", "epi", "fn"]]

reacts_fp = ["data/storage/heart_react.png", "data/storage/wow_react.png"]
options_reacts_fp = ["data/storage/like_react.png",
                     "data/storage/haha_react.png"]

# Cleaned input data
output_ingredients_file = f"data/storage/ingredients_list.pickle"
output_recipes_file = f"data/storage/recipes_list.json"

# Computed ingredients score
ingredients_combinations_csv = "data/storage/ingredients_combinations.csv"
ingredients_matrix = "data/storage/ingredients_matrix.csv"

# Handling of versus polls
versus_pending = "data/storage/versus_pending.csv"
versus_history = "data/storage/versus_history.csv"

# Computed images
recipe_rawpic_file = "data/tmp/recipe_raw.jpg"
recipe_newpic_file = "data/tmp/recipe_new.jpg"
cocktail_rawpic_file = "data/tmp/cocktail_raw.jpg"
cocktail_newpic_file = "data/tmp/cocktail_new.jpg"
versus1_img = "data/tmp/versus1_raw.jpg"
versus2_img = "data/tmp/versus2_raw.jpg"

