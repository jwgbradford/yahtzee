'''Basic rules
1 or 2 player mode - 1 player mode to start
each rolls 5 x 6-sided dice
scoring
1 pt = highest dice wins
2 pt = any pair
3 pt = any 3 of a kind
4 pt = two pair
5 pt = full house (3 of a kind and pair)
6 pt = 4 of a kind
7 pt = low run (1, 2, 3, 4, 5)
8 pt =  high run (2, 3, 4, 5, 6)
9 pt = yahtzee (any 5 of a kind)'''

import random

class Player():
    def __init__(self):
        self.dice = []
        self.score = 0

    def starting_roll(self):
        #roll 5 times
        for i in range(0, 5):
            #add a random number between 1 and 6 each time
            self.dice.append(random.randint(1,6))

    def check_doubles(self):
        #set a temporary flag in case we find a pair
        temp_pair= False
        #pairs need to be different values (otherwise they're a three of a kind or higher)
        pair_value = 0
        #we're checking the first dice against the others, so we only need 4 loops
        #but we want to check each dice aginst the rest
        for i in range(0, 5):
            #we don't want to check the first dice against itself, so we start our inner loop from i + 1
            for j in range(i+1, 5):
                if self.dice[i] == self.dice[j]:
                    #we only count pairs, if they are different to the first pair
                    if temp_pair and self.dice[i] != pair_value:
                        #we can just exit here as you can't find 3 doubles (that would require 6 dice)
                        return True, True
                    else:
                        temp_pair = True
                        pair_value = self.dice[i]
        if temp_pair:
            return True, False
        else:
            return False, False

    def check_multiples(self):
        #keep track of if we have, 3, 4, or 5 of a kind
        three = False
        four = False 
        five = False
        dice_count = 0
        #we do need to track which dice value we're counting
        dice_value = 0
        #we're checking the first dice against the others, so we only need 4 loops
        #but we want to check each dice aginst the rest
        for i in range(0, 5):
            #we don't want to check the first dice against itself, so we start our inner loop from i + 1
            for j in range(i+1, 5):
                if self.dice[i] == self.dice[j]:
                    #this time we want all the dice to be the same value
                    if dice_count > 0 and self.dice[i] == dice_value:
                        dice_count += 1
                        #remember we started counting at zero
                        if dice_count == 4:
                            five = True
                        elif dice_count == 3:
                            four = True
                        elif dice_count == 2:
                            three = True
                    else:
                        dice_count = 1
                        dice_value = self.dice[i]
            #if we don't find a run of 3 or more, reset the count
            dice_count = 0
        return three, four, five
    
    def check_full_house(self):
        #a full house is 2 of a kind, and 3 of a kind
        pair, double_pair = self.check_doubles()
        triple, quad, five = self.check_multiples()
        if pair and triple:
            return True
        else:
            return False
        
    def check_low_run(self):
        if (1 in self.dice and
            2 in self.dice and
            3 in self.dice and
            4 in self.dice and
            5 in self.dice):
            return True
        return False

    def check_high_run(self):
        if (6 in self.dice and
            2 in self.dice and
            3 in self.dice and
            4 in self.dice and
            5 in self.dice):
            return True
        return False

    def calculate_score(self):
        #first lets see if we have any pairs
        pair, double_pair = self.check_doubles()
        #then check for 3, 4, and 5 of a kind
        triple, quad, five = self.check_multiples()
        #now we can check for full houses (pair and 3 of a kind)
        if pair and triple:
            full_house = True
        else:
            full_house = False        
        #next we can check for a low run (1, 2, 3, 4, 5)
        low_run  = self.check_low_run()
        #finally a high run (2, 3, 4, 5, 6)
        high_run = self.check_high_run()
        #now work out the scores
        if five:
            self.score = 9
        elif high_run:
            self.score = 8
        elif low_run:
            self.score = 7
        elif quad:
            self.score = 6
        elif full_house:
            self.score = 5
        elif double_pair:
            self.score = 4
        elif triple:
            self.score = 3
        elif pair:
            self.score = 2


def main_loop():
    players = [Player(), Player()]
    players[0].starting_roll()
    players[1].starting_roll()
    for go in range(1,4):
        for turn in range(0, 2):
            if turn == 0:
                print('player 1 dice :')
            else:
                print('player 2 dice:')
            print(players[turn].dice)
            reroll = input('''Enter the dice number you would like to re-roll,\nor enter 's' to stick and calculate your score\n>''').lower()
            if reroll == 's':
                pass
            elif int(reroll) > 0 and int(reroll) < 7:
                new_roll = random.randint(1, 6)
                players[turn].dice[int(reroll) - 1] = new_roll
            else:
                print('Invalid response, turn forfeit')
            print(players[turn].dice, '\n')
    players[0].calculate_score()
    players[1].calculate_score()
    print('\nPlayer 1 dice:', players[0].dice, ' scores:', players[0].score)
    print('\nPlayer 2 dice:', players[1].dice, ' scores:',players[1].score)

if __name__ == "__main__":
    main_loop()