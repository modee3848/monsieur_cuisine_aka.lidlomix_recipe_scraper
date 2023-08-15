import requests
import time
import json

RETRY_DELAY = 60  # seconds
REQUEST_TIMEOUT = 20  # seconds
BASE_URL = "https://mc-api.tecpal.com/api/v2/recipes/"
HEADERS = {
    "Accept-Language": "pl-PL"        #Language code for customization
}

def save_to_file(data, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    #Fetch the recipe by its ID from the API.
def get_recipe_by_id(recipe_id):

 try:
    response = requests.get(BASE_URL + str(recipe_id), headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error request for recipe id {recipe_id}:{response.status_code}: {response.text}")
        return None
 except requests.Timeout:
        print(f"Request for recipe ID {recipe_id} timed out. Waiting for {RETRY_DELAY} seconds before retrying...")
        time.sleep(RETRY_DELAY)
        return get_recipe_by_id(recipe_id)  # Try again after timeout

 except requests.RequestException as e:
        print(f"Error while fetching recipe ID {recipe_id}: {e}")

 return None

    

def main():
    success_counter = 0

    for recipe_id in range(100000, 300001):
        recipe_data = get_recipe_by_id(recipe_id)

        if recipe_data:
            success_counter += 1
            print(f"Successfully fetched recipe {recipe_id}. Total count: {success_counter}")

            if 100000 <= recipe_id <= 200000:
                save_to_file(recipe_data, "all_recipes_part1.json")
            elif 200001 <= recipe_id <= 300000:
                save_to_file(recipe_data, "all_recipes_part2.json")

        # Add delay to not overwhelm the server
        time.sleep(0.2)

if __name__ == "__main__":
    main()
