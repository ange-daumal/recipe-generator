import random

# sprinkled spices
garnishes = ["nutmeg", "cinnamon", "grated chocolate",
             "half an orange wheel", "lemon twist",
             "pineapple slice", "cherry", "sage",
             'mint leaves', 'coffee bean', 'cherries',
             'orange slice', 'basil leaf', 'olive',
             "orange west",
             ]

temperatures = ["neat", "over ice"]

# leaves, roots and wood
bitters = ["aromatic bitter", 'tabasco', ]

herbs = ["sage"]

fruits = ["blackberries"]

steep_fruits = ["oranges zest"]
steep_liquids = ["honey"]

alcohols = ["vodka", "red wine", "rum", "cognac", "dry curacao", "triple sec",
            "prosecco", 'gin', 'coffee liqueur', 'irish cream liqueur',
            'schnapps', 'pink gin', 'spiced rum', 'dark rum', 'light rum',
            'vermouth', 'curaçao', 'cachaça', 'whiskey', 'passoa',
            'Grand Marnier', 'hazelnut liqueur',
            ]
thinners_common = ["simple syrup", "honey syrup", "sparkling water", ]
thinners_rare = ["milk", "lime juice", "lemon juice", "grapefruit lime",
                 "rhubarb infusion", "sage infusion", 'brewed coffee',
                 'melted dark chocolate', 'cranberry juice',
                 'chamomile infusion', 'tomato juice', 'worcestershire sauce',
                 'tea infusion', 'orange juice',
                 'cola',
                 ]


# RATIO
# alcohol thinners(cmn,rr) garnishes bitter
# 2 1,0 2 0
# 1 1,1 1 0
# 1 1,2 2 1
# 2 0,2 1 0
# 2 1,1 1 0
# 0 1,1


def get_ingredients(max_ingredient=3,
                    bitter_probability=0.1,
                    common_thinner_probability=0.6):
    sample = []

    nb_alcohol = random.randint(1, 2)
    nb_thinners = random.randint(max_ingredient - 1,
                                 max_ingredient) - nb_alcohol
    if nb_thinners < 0:
        nb_thinners = 0

    print(nb_thinners)

    nb_bitters = 1 if random.random() < bitter_probability else 0
    nb_garnishes = random.randint(1, 2)

    thinners_list = thinners_common + thinners_rare
    thinners_weights = [common_thinner_probability] * len(thinners_common) + \
                       [1 - common_thinner_probability] * len(thinners_rare)

    # alcohol
    sample.append(random.sample(alcohols, k=nb_alcohol))
    # thinners
    sample.append(random.choices(thinners_list,
                                 thinners_weights,
                                 k=nb_thinners))
    # bitters
    sample.append(random.sample(bitters, k=nb_bitters))

    # garnishes
    sample.append(random.sample(garnishes, k=nb_garnishes))

    return sample


sentences_step1 = [
    f"Build all ingredients.",
    f"Combine all ingredients.",
]

sentences_step2 = [
    f"Garnish with",
    f"Top with",
    f"Top off with",
    f"Serve with",
]

sentences_bonuses = [
    "Shake vigorously.",
    "Strain into a glass.",
    "Pour into a glass",
    ""
]


def generate_sentence(sample):
    ingredients = sample[0] + sample[1] + sample[2]
    garnish_list = sample[3]

    full_text = "Ingredients:\n"
    for ingredient in ingredients:
        full_text += f"* {ingredient.capitalize()}\n"

    full_text += "\n"
    full_text += f"1. {random.choice(sentences_step1)}\n"
    if garnish_list:
        full_text += f"2. {random.choice(sentences_step2)} " \
            f"{' and '.join(garnish_list)}.\n"

    return full_text


if __name__ == '__main__':
    print(get_ingredients())
    sample = get_ingredients()
    print(sample)
    sentence = generate_sentence(sample)
    print(sentence)
