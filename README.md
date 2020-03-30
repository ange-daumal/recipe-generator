# recipe-generator
An automatic recipe idea generator for the Facebook Page [Recipe Ideas Generator](facebook.com/Recipe-Ideas-Generator-113704106942055)

# Usage
## Required access 
After cloning the project, you need to put in a `.env` file at the root of this repository:
* `page_id`: the ID of the Facebook Page you want to post to.
* `user_id`: the ID of a user with permissions `manage_pages` and `publish_pages` on your Page
* `user_access_token`: the token of User Access for the specified `user_id`.

## Running instructions 
* Get pipenv using `python3 -m pip install pipenv`
* Install dependencies using `python3 -m pipenv install`
* Run `python3 -m pipenv run main.py`

Then you should see a text with "Success" followed by your new Post id.