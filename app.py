from flask import Flask, render_template, request
import random as r

app = Flask(__name__)

def parse(dice):
    dice = dice.replace(' ', '')
    list1 = dice.split('d')
    list5 = []
    while True:
        list3 = list1.copy()
        for i in range(len(list1)):
            try:
                list1[i] = int(list1[i])
            except ValueError:
                list2 = list1[i].split('+')
                if len(list2) != 1:
                    list1[i] = list2[0]
                    for j in range(1, len(list2)):
                        list1.append(list2[j])
                    for k in range(len(list1) - 1, i + 1, -1):
                        list1[k], list1[k-1] = list1[k-1], list1[k]
                else:
                    list2 = list1[i].split('-')
                    for j in range(len(list2)):
                        if j % 2 == 0:
                            list2[j] = int(list2[j])
                        else:
                            list2[j] = -int(list2[j])
                    list1[i] = list2[0]
                    for j in range(1, len(list2)):
                        list1.append(list2[j])
                    for k in range(len(list1) - 1, i + 1, -1):
                        list1[k], list1[k-1] = list1[k-1], list1[k]
        if list3 == list1:
            break
    for i in range(0, len(list1) - 1, 2):
        for j in range(list1[i]):
            list5.append(list1[i+1])
    return list1, list5

def roll(list1, list5):
    list4 = []
    list6 = [i for i in range(len(list5))]
    total = 0
    for i in range(0, len(list1) - 1, 2):
        if list1[i] > 0:
            for k in range(list1[i]):
                x = r.randint(1, list1[i+1])
                total += x
                list4.append(x)
        else:
            for k in range(0, list1[i], -1):
                x = (-1) * r.randint(1, list1[i+1])
                total += x
                list4.append(x)
    if len(list1) % 2 != 0:
        total += list1[-1]
    return total, list4, list6

def reroll_ones(total, list4, list5):
    list6=[]
    for i in range(len(list4)):
        if list4[i] == 1:
            list6.append(i)
            total -= 1
            x = r.randint(1, list5[i])
            total += x
            list4[i] = x
    return total, list4, list5, list6

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    rolls_list = []
    dice_list = [] # The HTML needs this to be NOT empty to show the button
    roll_query = ''
    rerolled_indices=[]

    if request.method == 'POST':
        action = request.form.get('action')
        roll_query = request.form.get('roll')

        if action == 'roll' and roll_query:
            try:
                # 1. Parse the string (e.g., '1d6')
                info_list, d_list = parse(roll_query)
                # 2. Perform the roll
                res, r_list, rerolled_indices = roll(info_list, d_list)
                
                # 3. Explicitly assign them to the variables 
                # that the render_template function uses
                result = res
                rolls_list = r_list
                dice_list = d_list 

            except Exception as e:
                print(f"Logic Error: {e}")
                result = 'Invalid Format!'
        
        elif action == 'reroll':
            try:
                # Ensure we are getting integers from the hidden form fields
                current_total = int(request.form.get('current_total', 0))
                
                # Convert the string lists back into integer lists
                current_rolls = [int(x) for x in request.form.getlist('current_rolls')]
                current_dice = [int(x) for x in request.form.getlist('current_dice')]
                
                # Perform the reroll logic
                result, rolls_list, dice_list, rerolled_indices = reroll_ones(current_total, current_rolls, current_dice)
                
                # Keep the original query so the input box stays filled
                roll_query = request.form.get('roll')
            except Exception as e:
                print(f"Reroll Error: {e}")
                result = "Error during reroll"
    return render_template('index.html', 
                            result=result, 
                            rolls_list=rolls_list, 
                            dice_list=dice_list, 
                            roll_query=roll_query,
                            rerolled_indices=rerolled_indices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001, use_reloader=False)