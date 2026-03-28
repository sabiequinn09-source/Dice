#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 11:24:04 2026

@author: quinneibas

"""
from flask import Flask, render_template, request

import random as r

app = Flask(__name__)

def parse_and_roll(roll):
    roll=roll.replace(' ','')
    list1 = roll.split('d')
    list3 = []
    list4= []
    list5=[]
    total=0
    while True:
        list3=list1.copy()
        for i in range(len(list1)):
            try:
                list1[i]=int(list1[i])
            except ValueError:
                list2=list1[i].split('+')
                if len(list2)!=1:
                    list1[i]=list2[0]
                    for j in range(1,len(list2)):
                        list1.append(list2[j])
                    for k in range(len(list1)-1,i+1,-1):
                        list1[k],list1[k-1]=list1[k-1],list1[k]
                else:
                    list2=list1[i].split('-')
                    for j in range(len(list2)):
                        if j%2==0:
                            list2[j]=int(list2[j])
                        else:
                            list2[j]=-int(list2[j])
                    list1[i]=list2[0]
                    for j in range(1,len(list2)):
                        list1.append(list2[j])
                    for k in range(len(list1)-1,i+1,-1):
                        list1[k],list1[k-1]=list1[k-1],list1[k]
        if list3==list1:
            break
    for i in range(0,len(list1)-1,2):
        if list1[i] > 0:
            for k in range(list1[i]):
                x=r.randint(1,list1[i+1])
                list5.append(list1[i+1])
                total+=x
                list4.append(x)
        else:
            for k in range(0,list1[i],-1):
                x=(-1) * r.randint(1,list1[i+1])
                list5.append(list1[i+1])
                total+=x
                list4.append(x)
    if len(list1)%2 != 0:
        total += list1[-1]
    return total, list4, list5

def reroll_ones(total, list4, list5):
    for i in range(len(list4)):
        if list4[i]==1:
            total-=1
            x=r.randint(1,list5[i])
            total+=x
            list4[i]=x
    return total, list4, list5
            
       
@app.route('/', methods=['GET', 'POST'])
def index1():
    result = None
    rolls_list = []
    dice_list = []
    roll_query = ''

    if request.method == 'POST':
        action = request.form.get('action')
        roll_query = request.form.get('roll')

        if action == 'roll' and roll_query:
            try:
                result, rolls_list, dice_list = parse_and_roll(roll_query)
            except:
                result = 'Invalid Format!'
        
        elif action == 'reroll':
            # 1. Get the data currently on the screen
            # Flask reads these from the hidden inputs we'll add to the HTML
            current_total = int(request.form.get('current_total', 0))
            # Convert strings back into lists of integers
            current_rolls = [int(x) for x in request.form.getlist('current_rolls')]
            current_dice = [int(x) for x in request.form.getlist('current_dice')]
            
            # 2. Run your new function
            result, rolls_list, dice_list = reroll_ones(current_total, current_rolls, current_dice)

    return render_template('index1.html', 
                           result=result, 
                           rolls_list=rolls_list, 
                           dice_list=dice_list, 
                           roll_query=roll_query)
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
    app.run(host='0.0.0.0', debug=True, port=5001, use_reloader=False)