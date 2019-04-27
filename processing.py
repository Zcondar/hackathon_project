import csv
import random
import copy
from collections import deque
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

selected_foods = []
deselected_foods = []
give_stack = deque()
dishes = []
give_counter = 0

def final_choice():
    random_num = random.randint(0, len(dishes))
    return dishes[random_num]["name"] + ".jpg"
    

def handle_selection(selected_name):
    global selected_foods
    global deselected_foods
    global give_stack
    
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
    #WARNING: NOT YET POPED UNSELECTED
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
    
def get_existing_names(cuisine_scores):
    temp = []
    for pair in cuisine_scores:
        temp.append[pair[0]]

    return temp

def get_existing_types(food_type_scores):
    temp = []
    for pair in food_type_scores:
        temp.append[pair[0]]
    
    return temp

def elemination():

    cuisine_scores = []
    is_hot_score = 0
    has_meat_score = 0
    food_type_scores = [] 
    
    #initial cuisine and food type initialization
    for food in dishes:
        if food["cuisine"] not in get_existing_names(cuisine_scores):
            cuisine_scores.append((food["cuisine"], 0))
        
        if food["food_type"] not in  get_existing_types(cuisine_scores):
            cuisine_scores.append((food["food_type"], 0))

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

        for pair in cuisine_scores:
            if pair[0].equals(food["cuisine"]):
                pair[1] += 1
        
        for pair in food_type_scores:
            if pair[0].equals(food["food_type"]):
                pair[1] += 1
        
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

        for pair in cuisine_scores:
            if pair[0].equals(food["cuisine"]):
                pair[1] -= 1
        
        for pair in food_type_scores:
            if pair[0].equals(food["food_type"]):
                pair[1] -= 1


    #calculate the highest scores
    max_is_hot_score = max(is_hot_score)
    max_has_meat_score = max(has_meat_score)
    max_cuisine_score = [0, 0]

    for pair in cuisine_scores:
        if pair[1] > max_cuisine_score[1]:
            max_cuisine_score = [pair[0], pair[1]]

    max_food_type_score = [0, 0]
    for pair in food_type_scores:
        if pair[1] > max_food_type_score[1]:
            max_food_type_score = [pair[0], pair[1]]

    #start dumping others
    if max_food_type_score[1] >= 2:
        dump_others("food_type", max_food_type_score[0])
    
    if max_cuisine_score[1] >= 3:
        dump_others("cuisine", max_cuisine_score[1])
    
    if max_is_hot_score >= 4:
        i = 0
        while i < len(dishes):
            if dishes["is_hot"].equals("FALSE"):
                dishes.pop(i)
    elif max_is_hot_score <= -4:
        i = 0
        while i < len(dishes):
            if dishes["is_hot"].equals("TRUE"):
                dishes.pop(i)

    if max_has_meat_score >= 4:
        i = 0
        while i < len(dishes):
            if dishes["has_meat"].equals("FALSE"):
                dishes.pop(i)
    elif max_has_meat_score <= -4:
        i = 0
        while i < len(dishes):
            if dishes["has_meat"].equals("TRUE"):
                dishes.pop(i)

def dump_others(attribute, value):
    i = 0
    while i < len(dishes):
        if dishes[i][attribute] != value:
            dishes.pop(i)

def give_two():

    #gives two random selection
    first = random.randint(0, len(dishes))
    second = random.randint(0, len(dishes))
    while second == first:
        second = random.randint(0, len(dishes))
    
    give_stack.append((dishes[first], dishes[second]))
    
    return (dishes[first]["food_name"] + ".jpg", dishes[second]["food_name"] + ".jpg")

def load_csv():
    #load the csv into a dictionary
    csvfile = open("food_map.csv", "r")
    global dishes
    reader = csv.DictReader(csvfile, fieldnames = ["image_id", "food_name", "cuisine", "is_hot", "has_meat", "food_type"], skipinitialspace=True)
    dishes = list(reader)
    dishes.pop(0)

def fake_user():
    pick = random.randint(0, 2)
    return give_stack[pick]["name"] + ".jpg"

def test():
    give_two()
    while True:
        give_two()
        selected_name = fake_user()
        handle_selection(selected_name)

@app.route("/")
def hello():
    return render_template('pickoriginal.html',a="pizza.jpg",b="chicken_wings.jpg")

@app.route('/pickoriginal', methods=['post'])
def apage():

    result = request.form['button']
    print(result)
    load_csv()
    choices = give_two()
    a = choices[0]
    b = choices[1]

    return render_template('pickoriginal.html',a=a,b=b)

if __name__ == "__main__":
    load_csv()
    print(give_two())
    app.run(debug=True)
