import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

def list_all_categories():
    response = requests.get(f"{BASE_URL}categories.php")
    return response.json()

def get_meals_by_category(category_name):
    response = requests.get(f"{BASE_URL}filter.php?c={category_name}")
    return response.json()

def get_meal_details(meal_id):
    response = requests.get(f"{BASE_URL}lookup.php?i={meal_id}")
    return response.json()