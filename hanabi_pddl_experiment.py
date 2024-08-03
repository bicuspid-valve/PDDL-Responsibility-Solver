# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 16:46:12 2024

@author: tparker
"""

import os

from hanabi_pddl_main import Deck, randomplan, passive_ant_game, passive_ant_PDDL, stringtoformula, domain2
from hanabi_pddl_main import getresp2
from time import time

def getPDDLresp(planlength,resp):
    ready = False
    while not ready:
        deck1 = Deck()
        hand1, hand2 = deck1.drawhands(planlength)
        plan = randomplan(planlength)
        b = passive_ant_game(plan,1,hand1,hand2,goal)
        if b == resp:
            ready = True
    x=passive_ant_PDDL(goalstring,hand1,hand2,plan,1)
    file2 = open("problem.pddl", 'w+')
    file2.write(x)
    file2.close()
    stream = os.popen('/home/tim/fast-downward.sif --alias lama-first --search-time-limit 120s  domain.pddl problem.pddl')
    output = stream.read()
    stream.close()
    list1 = [0,0,0]
    if resp == True:
        for i in range(len(output)):
                if output[i:i+11] == "Total time:":
                    x = 12
                    while output[i+x] != "s":
                        x += 1
                    list1[1] = (output[i+12:i+x]) 
                if output[i:i+12] == "Search time:":
                    x = 13
                    while output[i+x] != "s":
                        x += 1
                    list1[0] = (output[i+13:i+x])
                if output[i:i+13] == "Planner time:":
                    x = 14
                    while output[i+x] != "s":
                        x += 1
                    list1[2] = (output[i+14:i+x])
    else:
        for i in range(len(output)):
                if output[i:i+11] == "Total time:":
                    x = 12
                    while output[i+x] != "s":
                        x += 1
                    list1[1] = (output[i+12:i+x]) 
                if output[i:i+12] == "Search time:":
                    x = 13
                    while output[i+x] != "s":
                        x += 1
                    list1[0] = (output[i+13:i+x])
                if output[i:i+13] == "Planner time:":
                    x = 14
                    while output[i+x] != "s":
                        x += 1
                    list1[2] = (output[i+14:i+x])
    return list1

def getPDDLresp2(planlength,resp):
    ready = False
    while not ready:
        deck1 = Deck()
        hand1, hand2 = deck1.drawhands(planlength)
        plan = randomplan(planlength)
        x=passive_ant_PDDL(goalstring,hand1,hand2,plan,1)
        file2 = open("problem.pddl", 'w+')
        file2.write(x)
        file2.close()
        stream = os.popen('/home/tim/fast-downward.sif --alias lama-first --search-time-limit 300s  domain.pddl problem.pddl')
        output = stream.read()
        stream.close()
        if ("Solution found!" in output) == resp:
            ready = True
    list1 = [0,0,0]
    if resp == True:
        for i in range(len(output)):
                if output[i:i+11] == "Total time:":
                    x = 12
                    while output[i+x] != "s":
                        x += 1
                    list1[1] = (output[i+12:i+x]) 
                if output[i:i+12] == "Search time:":
                    x = 13
                    while output[i+x] != "s":
                        x += 1
                    list1[0] = (output[i+13:i+x])
                if output[i:i+13] == "Planner time:":
                    x = 14
                    while output[i+x] != "s":
                        x += 1
                    list1[2] = (output[i+14:i+x])
    else:
        for i in range(len(output)):
                if output[i:i+11] == "Total time:":
                    x = 12
                    while output[i+x] != "s":
                        x += 1
                    list1[1] = (output[i+12:i+x]) 
                if output[i:i+12] == "Search time:":
                    x = 13
                    while output[i+x] != "s":
                        x += 1
                    list1[0] = (output[i+13:i+x])
                if output[i:i+13] == "Planner time:":
                    x = 14
                    while output[i+x] != "s":
                        x += 1
                    list1[2] = (output[i+14:i+x])
    return list1



# open the file using open() function
file = open("domain.pddl", 'w+')
# Overwrite the file
file.write(domain2())
file.close()


goalstring = "(NOT isfinished red AND NOT isfinished white)"
goal = stringtoformula(goalstring)

for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
    count = 0
    print(str(i)+" cards")
    file1 = open(str(i)+" Python Results.txt","w+")
    while count != 50:
        hand1,hand2,plan = getresp2(i, False)
        k = 1
        finaltime = 0
        while finaltime == 0 and k < 100000:
            start = time()
            for j in range(k):
                b = passive_ant_game(plan,1,hand1,hand2,goal)
            end = time()
            finaltime = (end-start)/k
            k = k*10
        file1.write(str(finaltime)+"\n")
        count += 1
        print(str(count*2)+"% done")
    file1.close()
        
    

# for i in [15]:
#     print(i)
#     file1 = open(str(i)+" Cards Results.txt","w+")
#     truelist = [[],[],[]]
#     falselist = [[],[],[]]
#     for j in range(50):
#         print(str((j)*2)+"% complete")
# #        list1 = getPDDLresp2(i,True)
#         list2 = getPDDLresp2(i,False)
#         for k in range(len(list2)):
# #            truelist[k].append(list1[k])
#             falselist[k].append(list2[k])
#     file1.write("\n")
#     file1.write(str(i)+" Cards\n")
#     file1.write("\n")
#     file1.write("Responsible = True\n")
#     file1.write("Search Time\n")
#     file1.write("\n")
#     for l in truelist[0]:
#         file1.write(l+"\n")
#     file1.write("\n")
#     file1.write("Total Time\n")
#     file1.write("\n")
#     for l in truelist[1]:
#         file1.write(l+"\n")
#     file1.write("\n")
#     file1.write("Planning Time\n")
#     file1.write("\n")
#     for l in truelist[2]:
#         file1.write(l+"\n")
#     file1.write("\n")
#     file1.write("Responsible = False\n")
#     file1.write("Search Times\n")
#     file1.write("\n")
#     for l in falselist[0]:
#         file1.write(l+"\n")
#     file1.write("\n")
#     file1.write("Total Time\n")
#     file1.write("\n")
#     for l in falselist[1]:
#         file1.write(l+"\n")
#     file1.write("\n")
#     file1.write("Planning Time\n")
#     file1.write("\n")
#     for l in falselist[2]:
#         file1.write(l+"\n")
#     file1.close()
