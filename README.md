# recipe-generator
An automatic recipe idea generator for two Facebook Pages:

* Food recipe [Recipe Ideas Generator](https://www.facebook.com/Recipe-Ideas-Generator-113704106942055)
* Cocktail recipe [Cocktail Idea Generator](https://www.facebook.com/Cocktail-Idea-Generator-100886964965848)

# Developers

## Required access 
After cloning the project, you need to put in a `.env` file at the root of this repository.
* `page_id`: the ID of the Facebook Page you want to post to.
* `user_id`: the ID of a user with permissions `manage_pages` and `publish_pages` on your Page
* `user_access_token`: the token of User Access for the specified `user_id`.

Another way is to directly use a Page Access Token. On this project, there is two variables:
* `recipe_access_token` for the first page,
* `cocktail_access_token` for the second one.

## Data required
* Get Ryan Lee's [Recipe Box](https://github.com/rtlee9/recipe-box) dataset
* Unzip the folder `recipe-box` in `data/` folder.

## Running instructions 
* Get pipenv using `python3 -m pip install pipenv`
* Install dependencies using `python3 -m pipenv install`
* Run `python3 -m pipenv run main.py`

Then you should see a text with "Success" followed by your new Post id.