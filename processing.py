import csv
import random
import copy
from collections import deque

selected_foods = []
deselected_foods = []
give_stack = deque()
dishes = None
give_counter = 0


def final_choice():
    

def handle_selection(selected_name):
    name = selected_name.split["."][0]
    selected = None
    global give_counter

    #find the food selected
    for food in dishes:
        if name.equals(food["name"]):
            selected = food
            selected_foods.append(food)
            break

    #retrieve previous selections and update the selected and deselected list
    previous_feed = give_stack.pop()
    if selected is previous_feed[0]:
        selected_foods.append(previous_feed[0])
        deselected_foods.append(previous_feed[1])
    else:
        selected_foods.append(previous_feed[1])
        deselected_foods.append(previous_feed[0])
    
    #if counter reaches 5, start elimination process and make final choice
    if give_counter == 5:
        elemination()
        final_choice()
    '''    
    elif give_counter == 3:
        elemination()
    '''
    give_counter += 1
    give_two()
    
def elemination():
    cuisine_scores = {}
    is_hot_score = 0
    has_meat_score = 0
    food_type_scores = {} 
    
    #initial cuizin and food type initialization
    for food in dishes:
        if food["cuisine"] not in cuisine_scores.keys():
            cuisine_scores[food["cuisine"]] = 0
        
        if food["food_type"] not in  food_type_scores.keys():
            food_type_scores[food["food_type"]] = 0

    #update scores based on selections
    for food in selected_foods:
        if food["is_hot"].equals("TRUE"):
            is_hot_score += 1
        else:
            is_hot_score -= 1

        if food["has_meat"].equals("TRUE"):
            has_meat_score += 1
        else:
            has_meat_score -= 1

        cuisine_scores[food["cuisine"]] += 1
        food_type_scores[food["food_type"]] += 1
        
    #update scores based on deselections
    for food in deselected_foods:
        if food["is_hot"].equals("TRUE"):
            is_hot_score -= 1
        else:
            is_hot_score += 1

        if food["has_meat"].equals("TRUE"):
            has_meat_score -= 1
        else:
            has_meat_score += 1

        cuisine_scores[food["cuisine"]] -= 1
        food_type_scores[food["food_type"]] -= 1

    max_cuisine_score = 10
    for item in cuisine

def give_two():
    #gives two random selection
    first = random.randint(0, len(dishes))
    second = random.randint(0, len(dishes))
    while second == first:
        second = random.randint(0, len(dishes))
    
    give_stack.append((dishes[first], dishes[second]))
    
    return (dishes[first]["food_name"] + ".jpg", dishes[second]["food_name"] + ".jgp")

def load_csv():
    #load the csv into a dictionary
    csvfile = open("food_map.csv", "r")

    reader = csv.DictReader(csvfile, fieldnames = ["image_id", "food_name", "cuisine", "is_hot", "has_meat", "food_type"], skipinitialspace=True)
    data = list(reader)
    data.pop(0)
    return data

def fake_user():
    pick = random.randint(0, 2)
    return give_stack[pick]["name"] + ".jpg"

def test():
    give_two()
    while True:
        give_two()
        selected_name = fake_user()
        handle_selection(selected_name)

if __name__ == "__main__":
    dishes = load_csv()
    dup_dishes = copy.deepcopy(dishes)
    print(give_two())