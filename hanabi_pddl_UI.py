# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:49:15 2024

@author: tparker
"""

from hanabi_pddl_main import active_ant, passive_ant, passive_att

print("Would you like to check anticipation or attribution?")
ans1 = input("Answer: ")
ans1 = ans1.lower()
if ans1 in ["anticipation","ant"]:
    checktype = "anticipation"
else:
    checktype = "attribution"
print("Would you like to check active or passive responsibility?")
ans1 = input("Answer: ")
ans1 = ans1.lower()
if ans1 in ["passive","pass","p"]:
    resptype = "passive"
else:
    resptype = "active"
print("For which agent would you like to check?")
ans1 = input("Answer: ")
ans1 = ans1.lower()
if ans1 in ["one","1",1]:
    agent = 1
    other = 2
else:
    agent = 2
    other = 1
print("What formula would you like to evaluate responsibility for?")
string = input("Answer: ")
print("How long should the plan be?")
ans1 = input("Answer: ")
ans1 = ans1.lower()
if ans1 in ["one","1",1]:
    planlength = 1
elif ans1 in ["two","2",2]:
    planlength = 2
elif ans1 in ["three","3",3]:
    planlength = 3
elif ans1 in ["four","4",4]:
    planlength = 4
else:
    planlength = 5
plan1 = []
for i in range(planlength):
    print("Input action "+str(i+1)+" for agent "+str(agent)+".")
    plan1.append(input("Answer: ").lower())
if checktype == "attribution":
    plan2 = []
    for i in range(planlength):
        print("Input action "+str(i+1)+" for agent "+str(other)+".")
        plan2.append(input("Answer: ").lower())
    if resptype == "passive":
        passive_att(string,plan1,plan2,agent)
    else:
        active_ant(string,plan1,agent)
