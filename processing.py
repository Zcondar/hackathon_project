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
give_counter = -1
done = 0
final_pic = ""
roundNum = 0

def final_choice():
    random_num = random.randint(0, len(dishes)-1)
    global done
    done = 1
    global final_pic
    for row in dishes:
        print(row)

    final_pic = dishes[random_num]["food_name"] + ".jpg"
    print(final_pic)

def handle_selection(selected_name):
    global selected_foods
    global deselected_foods
    global give_stack
    
    print(selected_name)
    name = selected_name.split(".")[0]
    selected = None
    global give_counter
    print("checkpoint 1")

    #find the food selectedclear

    for food in dishes:
        if name == food["food_name"]:
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
    
    print("counter is " + str(give_counter))
    #if counter reaches 4, start elimination process and make final choice
    if give_counter == 4:
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
        temp.append(pair[0])

    return temp

def get_existing_types(food_type_scores):
    temp = []
    for pair in food_type_scores:
        temp.append(pair[0])
    
    return temp

def elemination():

    cuisine_scores = []
    is_hot_score = 0
    has_meat_score = 0
    food_type_scores = [] 
    asian = 0
    #initial cuisine and food type initialization
    for food in dishes:
        if food["cuisine"] not in get_existing_names(cuisine_scores):
            cuisine_scores.append([food["cuisine"], 0])
        
        if food["food_type"] not in  get_existing_types(cuisine_scores):
            cuisine_scores.append([food["food_type"], 0])

    #update scores based on selections
    for food in selected_foods:
        if food["is_hot"] == "TRUE":
            is_hot_score += 1
        else:
            is_hot_score -= 1

        if food["has_meat"] == "TRUE":
            has_meat_score += 1
        else:
            has_meat_score -= 1

        if food["continent"] == "Asian":
            asian += 1

        for pair in cuisine_scores:
            if pair[0] == food["cuisine"]:
                pair[1] += 1
        
        for pair in food_type_scores:
            if pair[0] == food["food_type"]:
                pair[1] += 1
        
    #update scores based on deselections
    for food in deselected_foods:
        if food["is_hot"] == "TRUE":
            is_hot_score -= 1
        else:
            is_hot_score += 1

        if food["has_meat"] == "TRUE":
            has_meat_score -= 1
        else:
            has_meat_score += 1

        for pair in cuisine_scores:
            if pair[0] == food["cuisine"]:
                pair[1] -= 1
        
        for pair in food_type_scores:
            if pair[0] == food["food_type"]:
                pair[1] -= 1


    #calculate the highest scores
    max_is_hot_score = is_hot_score
    max_has_meat_score = has_meat_score
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

    if asian >= 3:
        dump_others("continent", "Asian")
    else:
        dump_other("continent","Western")

    if max_is_hot_score >= 4:
        i = 0
        while i < len(dishes):
            if dishes[i]["is_hot"] == "FALSE":
                dishes.pop(i)
            i += 1
    elif max_is_hot_score <= -4:
        i = 0
        while i < len(dishes):
            if dishes[i]["is_hot"] == "TRUE":
                dishes.pop(i)
            i += 1

    if max_has_meat_score >= 4:
        i = 0
        while i < len(dishes):
            if dishes[i]["has_meat"] == "FALSE":
                dishes.pop(i)
            i += 1
    elif max_has_meat_score <= -4:
        i = 0
        while i < len(dishes):
            if dishes["has_meat"] == "TRUE":
                dishes.pop(i)
            i += 1

def dump_others(attribute, value):
    i = 0
    while i < len(dishes):
        if dishes[i][attribute] != value:
            dishes.pop(i)
            
        i += 1

def give_two():

    #gives two random selection
    first = random.randint(0, len(dishes)-1)
    second = random.randint(0, len(dishes)-1)
    while second == first:
        second = random.randint(0, len(dishes))
    
    give_stack.append((dishes[first], dishes[second]))
    
    return (dishes[first]["food_name"] + ".jpg", dishes[second]["food_name"] + ".jpg")

def load_csv():
    #load the csv into a dictionary
    csvfile = open("food_map.csv", "r")
    global dishes
    reader = csv.DictReader(csvfile, fieldnames = ["image_id", "food_name", "cuisine", "continent", "is_hot", "has_meat", "food_type"], skipinitialspace=True)
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
    choice = give_two()
    a = choice[0]
    b = choice[1]
    an = a.split(".")[0]
    an.replace("_"," ",9)

    bn = b.split(".")[0]
    bn.replace("_"," ",9)
    # return render_template('apage_style.html',a=a,b=b,r = roundNum,an=an,bn=bn)
    return render_template('apage_style_1st_page_real.html',a=a,b=b,r = roundNum,an=an,bn=bn)


@app.route('/pickoriginal', methods=['post'])
def apage():
    global roundNum
    global done
    global final_pic
    result = request.form['button']
    handle_selection(result)
    # print(result)
    choices = give_two()
    a = choices[0]
    b = choices[1]
    roundNum += 1

    an = a.split(".")[0]
    an.replace("_"," ",9)

    bn = b.split(".")[0]
    bn.replace("_"," ",9)

    if done == 1:
        global selected_foods
        global deselected_foods
        global give_stack
        global dishes
        global give_counter

        selected_foods = []
        deselected_foods = []
        give_stack = deque()
        dishes = []
        give_counter = -1
        done = 0
        roundNum = 0
        load_csv()
        n = final_pic.split(".")[0]
        give_two()
        return render_template("apage_style_1st_page.html", a = final_pic, n=n)
    else:
        return render_template('apage_style.html',a=a,b=b,r=roundNum,an=an,bn=bn)

if __name__ == "__main__":
    load_csv()
    # print(give_two())
    app.run(debug=False)
