from hanabi_pddl_strings import problem1, problem2, domain1, domain2
from random import shuffle, randint
from time import time

class Conjunction:
    def __init__(self,part1,part2):
        self.sub = [part1,part2]
        
    def PDDL(self):
        string = "(AND "+self.sub[0].PDDL()+" "+self.sub[1].PDDL()+")"
        return string
    
    def __str__(self):
        string = "("+str(self.sub[0])+" AND "+str(self.sub[1])+")"
        return string
    
    def makecopy(self):
        return Conjunction(self.sub[0].makecopy(), self.sub[1].makecopy())
    
    def evaluate(self,game):
        a = self.sub[0].evaluate(game)
        b = self.sub[1].evaluate(game)
        return a and b

class Disjunction:
    def __init__(self,part1,part2):
        self.sub = [part1,part2]
        
    def PDDL(self):
        string = "(OR "+self.sub[0].PDDL()+" "+self.sub[1].PDDL()+")"
        return string
    
    def __str__(self):
        string = "("+str(self.sub[0])+" OR "+str(self.sub[1])+")"
        return string
    
    def makecopy(self):
        return Disjunction(self.sub[0].makecopy(), self.sub[1].makecopy())
    
    def evaluate(self,game):
        a = self.sub[0].evaluate(game)
        b = self.sub[1].evaluate(game)
        return a or b
    
class Negation:
    def __init__(self,part1):
        self.sub = [part1]
        
    def PDDL(self):
        string = "(NOT "+self.sub[0].PDDL()+")"
        return string
    
    def __str__(self):
        string = "NOT "+str(self.sub[0])
        return string
    
    def makecopy(self):
        return Negation(self.sub[0].makecopy())
    
    def evaluate(self,game):
        a = self.sub[0].evaluate(game)
        return not a
    
class Atomic:
    def __init__(self,part1,part2):
        self.name = part1
        self.objects = part2
        
    def PDDL(self):
        if self.objects == "":
            string = "("+self.name+")"
        else:
            string =  "("+self.name+" "+self.objects+")"
        return string
    
    def __str__(self):
        if self.objects == "":
            return self.name
        else:
            return self.name+" "+self.objects
    
    def makecopy(self):
        return Atomic(self.name+"_copy",self.objects)
    
    def evaluate(self,game):
        if self.name == "failure":
            return game.failure
        elif self.name == "isfinished":
            if game.board[self.objects] == 3:
                return True
            else:
                return False
    
    
class Card:
    def __init__(self,colour,number):
        self.colour = colour
        self.number = number
        
    
    def __str__(self):
        string = self.colour + " " + str(self.number)
        return string
    
    def PDDLstr(self):
        string = self.colour + " n" + str(self.number)
        return string
    
class Hand:
    def __init__(self,cards,agent):
        self.cards = cards
        self.agent = agent
        
    def __str__(self):
        string = "["
        for i in range(len(self.cards)):
            j = self.cards[i]
            if i == len(self.cards) - 1:
                string += str(j)+"]"
            else:
                string += str(j)+", "
        return string
            
    def makePDDLstring(self,copy):
        string = ""
        if copy == True:
            inhand = "(inhand"+str(self.agent)+"_copy "
        else:
            inhand = "(inhand"+str(self.agent)+" "
        for i in range(len(self.cards)):
            j = self.cards[i]
            string += inhand+j.PDDLstr()+" n"+str(i+1)+") "
        return string
            
class Deck:
    
    def __init__(self):
        self.cards = []
        for colour in ["red","white","yellow","green"]:
            for number in [1,2,3]:
                for k in range(5):
                    self.cards.append(Card(colour, number))
    
    def shuffledeck(self):
        shuffle(self.cards)
    
    def drawhands(self,handsize):
        self.shuffledeck()
        list1 = []
        list2 = []
        for i in range(handsize):
            list1.append(self.cards.pop())
            list2.append(self.cards.pop())
        hand1 = Hand(list1,1)
        hand2 = Hand(list2,2)
        return hand1,hand2
     
class Game:
    
    def __init__(self,hand1,hand2):
        self.hand1 = hand1
        self.hand2 = hand2
        
    def reset(self):
        self.board = {"red":0,"white":0,"yellow":0,"green":0}
        self.failure = False
        self.tokens1 = 1
        self.tokens2 = 1
        
    def play(self,move1,move2,index):
        if move1 == "discard":
            self.tokens1 += 1
        else:
            if self.tokens1 > 0:
                self.tokens1 -= 1
                card = self.hand1.cards[index]
                if card.number == self.board[card.colour] + 1:
                    self.board[card.colour] +=1
                elif card.number != 3 or self.board[card.colour] != 3:
                    self.failure = True
        if move2 == "discard":
            self.tokens2 += 1
        else:
            if self.tokens2 > 0:
                self.tokens2 -= 1
                card = self.hand2.cards[index]
                if card.number == self.board[card.colour] + 1:
                    self.board[card.colour] +=1
                elif card.number != 3 or self.board[card.colour] != 3:
                    self.failure = True
        
    def playgame(self,plan1,plan2):
        self.reset()
        for i in range(len(plan1)):
            self.play(plan1[i],plan2[i],i)
            
def find_passive_ant(agent,hand1,hand2,planlength,goal):
    plan = ["play"]*planlength
    responsible = False
    finished = False
    while responsible == False and finished == False:
        responsible = passive_ant_game(plan,agent,hand1,hand2,goal)
        if responsible == False:
            plan,finished = getnextplan(plan)
    return plan,responsible

def find_not_passive_ant(agent,hand1,hand2,planlength,goal):
    plan = ["play"]*planlength
    responsible = True
    finished = False
    while responsible == True and finished == False:
        responsible = passive_ant_game(plan,agent,hand1,hand2,goal)
        if responsible == True:
            plan,finished = getnextplan(plan)
    return plan,responsible
            
def passive_ant_game(plan,agent,hand1,hand2,goal):
    plana = plan
    planb = ["play"]*len(plan)
    responsible = False
    finished = False
    while responsible == False and finished == False:
        game = Game(hand1, hand2)
        if agent == 1:
            game.playgame(plana, planb)
        else:
            game.playgame(planb, plana)
        if goal.evaluate(game) == True:
            exists = winning_plan_exists(planb,agent,hand1,hand2,goal)
            if exists == True:
                responsible = True
            else:
                planb,finished = getnextplan(planb)
        else:
            planb,finished = getnextplan(planb)
    return responsible
            
def winning_plan_exists(planb,agent,hand1,hand2,goal):
    plana = ["play"]*len(planb)
    exists = False
    finished = False
    while exists == False and finished == False:
        game = Game(hand1, hand2)
        if agent == 1:
            game.playgame(plana, planb)
        else:
            game.playgame(planb, plana)
        if goal.evaluate(game) == False:
            exists = True
        else:
            plana,finished = getnextplan(plana)
    return exists

def getnextplan(plan):
    index = len(plan)-1
    done = False
    finished = False
    while not done:
        if index == -1:
            plan = ["discard"]*len(plan)
            done = True
            finished = True
        elif plan[index] == "play":
            plan[index] = "discard"
            done = True
        else:
            plan[index] = "play"
            index -= 1
    return plan,finished
                    
def randomplan(planlength):
    plan = []
    for i in range(planlength):
        choice = randint(1, 2)
        if choice == 1:
            plan.append("play")
        else:
            plan.append("discard")
    return plan
     
def stringtoformula(string):
    if string[0] == "N":
        return Negation(stringtoformula(string[4:]))
    elif string[0] == "(":
        left = 0
        right = 0
        index = 1
        while not (left == right and string[index] in ["A","O"] and not
                   string[index+1] == "T"):
            if string[index] == "(":
                left += 1
            elif string[index] == ")":
                right += 1
            index += 1
        if string[index] == "A":
            part1 = stringtoformula(string[1:index - 1])
            part2 = stringtoformula(string[index+4:-1])
            return Conjunction(part1, part2)
        else:
            part1 = stringtoformula(string[1:index - 1])
            part2 = stringtoformula(string[index+3:-1])
            return Disjunction(part1, part2)
    else:
        if " " not in string:
            return Atomic(string,"")
        else:
            index = 0
            while string[index] != " ":
                index += 1
            return Atomic(string[0:index],string[index+1:])
    
def conjunctlist(list1):
    if len(list1) == 1:
        return list1[0]
    else:
        part1 = list1.pop(0)
        part2 = conjunctlist(list1)
        return Conjunction(part1,part2)
    
def timeformula(time):
    return Atomic("istime","n"+str(time+1))

def plantoformula(plan,agent):
    index = 1
    newlist = []
    for i in plan:
        newlist.append(Atomic("played"+str(agent),i+" n"+str(index)))
        index += 1
    return conjunctlist(newlist)

def sameplanformula(agent,length):
    newlist = []
    ag = str(agent)
    for i in range(length):
        f1 = Atomic("played"+ag,"play n"+str(i+1))
        f2 = Atomic("played"+ag+"_copy","play n"+str(i+1))
        f3 = Atomic("played"+ag,"discard n"+str(i+1))
        f4 = Atomic("played"+ag+"_copy","discard n"+str(i+1))
        f5 = Conjunction(f1, f2)
        f6 = Conjunction(f3, f4)
        f7 = Disjunction(f5, f6)
        newlist.append(f7)
    return conjunctlist(newlist)

def passive_att_PDDL(string,plan1,plan2,agent):
    other = 3 - agent
    f1 = plantoformula(plan1, agent)        
    f2 = plantoformula(plan2, other)
    goal = stringtoformula(string)
    f3 = conjunctlist([f1,f2,goal])
    stringlist = problem1()
    string1 = stringlist[0]
    string2 = f3.PDDL()
    string3 = stringlist[1]
    print("Here is the domain:")
    print(domain1())
    print("Here is the first problem")
    print(string1+string2+string3)
    f4 = Negation(goal)
    f5 = Conjunction(f2,f4)
    string4 = f5.PDDL()
    print("Here is the second problem")
    print(string1+string4+string3)
    
def active_ant_PDDL(string,plan,agent):
    goal = stringtoformula(string)
    f1 = Negation(goal)
    stringlist = problem1()
    string1 = stringlist[0]
    string2 = f1.PDDL()
    string3 = stringlist[1]
    print("Here is the domain:")
    print(domain1())
    print("Here is the first problem")
    print(string1+string2+string3)
    f2 = plantoformula(plan, agent)
    f3 = Conjunction(f1,f2)
    string4 = f3.PDDL()
    print("Here is the second problem")
    print(string1+string4+string3)
    
def passive_ant_PDDL(goalstring,hand1,hand2,plan,agent):
    stringlist = problem2()
    string1 = stringlist[0]
    string2 = hand1.makePDDLstring(False)+hand1.makePDDLstring(True)
    string2 += hand2.makePDDLstring(False)+hand2.makePDDLstring(True)
    string3 = stringlist[1]
    string5 = stringlist[2]
    otheragent = 3 - agent
    goal = stringtoformula(goalstring)
    othergoal = Negation(goal.makecopy())
    sameplan = sameplanformula(otheragent, len(plan))
    forceplan = plantoformula(plan, agent)
    timelimit = timeformula(len(plan))
    
    f1 = conjunctlist([goal,forceplan,othergoal,sameplan,timelimit,timelimit.makecopy()])
    string4 = f1.PDDL()
    print("Here is the domain:")
    print(domain2())
    print("Here is the problem")
    print(string1+string2+string3+string4+string5)

planlength = 9

planc = ["discard"]*planlength


ready = False

goalstring = "(NOT isfinished red AND NOT isfinished white)"
goal = stringtoformula(goalstring)

while not ready:
    print("i")
    deck1 = Deck()
    hand1, hand2 = deck1.drawhands(planlength)
    plan = randomplan(planlength)
    b = passive_ant_game(plan,1,hand1,hand2,goal)
    if b == True:
        ready = True

passive_ant_PDDL(goalstring,hand1,hand2,plan,1)

# count = 0
# while count != 40:
#  #   print("i")
#     deck1 = Deck()
#     hand1, hand2 = deck1.drawhands(planlength)
#     plan = randomplan(planlength)
#     b = passive_ant_game(plan,1,hand1,hand2,goal)
#     if b == True:
#         start = time()
#         for i in range(5):
#             b = passive_ant_game(plan,1,hand1,hand2,goal)
#         end = time()
#         print((end - start)/5)
#         count += 1
        
        

