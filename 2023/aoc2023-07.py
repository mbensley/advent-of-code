# Timings: Part A: 10:00 / Part B: Fun Run
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

def sortcards(cardlist):
    def gethand(hand):
        hset = list(set(hand))
        if len(hset) == 5:
            return 'H'
        if len(hset) == 4:
            return 'O'
        if len(hset) == 1:
            return '5'
        if len(hset) == 3: #2 pair, 3 of a kind
            # count each card
            if hand.count(hset[0]) == 3 or hand.count(hset[1]) == 3 or hand.count(hset[2]) == 3:
                return '3'
            return 'T'
        if len(hset) == 2: #4 of a kind of FullHouse
            if hand.count(hset[0]) == 4 or hand.count(hset[1]) == 4:
                return '4'
            return 'F'

    cardorder = '23456789TJQKA'
    cardlist.sort(key=lambda t: [cardorder.index(c) for c in t[0]])
    handorder = 'HOT3F45'
    cardlist.sort(key=lambda t: handorder.index(gethand(t[0])))

def sortcardsb(cardlist):
    def gethand(hand):
        hset = list(set(hand))
        if 'J' not in hset:
            if len(hset) == 5:
                return 'H'
            if len(hset) == 4:
                return 'O'
            if len(hset) == 1:
                return '5'
            if len(hset) == 3: #2 pair, 3 of a kind
                # count each card
                if hand.count(hset[0]) == 3 or hand.count(hset[1]) == 3 or hand.count(hset[2]) == 3:
                    return '3'
                return 'T'
            if len(hset) == 2: #4 of a kind of FullHouse
                if hand.count(hset[0]) == 4 or hand.count(hset[1]) == 4:
                    return '4'
                return 'F'
        else: # Use the Joker to make a stronger hand 
            jcount = hand.count('J')
            hset.remove('J')
            print(len(hset), jcount, hset)
            if len(hset) == 1 or len(hset) == 0:
                return '5'
            if jcount == 3:
                return '4'
            if jcount == 2:
                #hset is 3 or 2
                if len(hset) == 3:
                    return '3'
                return '4'
            if jcount == 1:
                #hset is 4, 3, or 2
                if len(hset) == 4:
                    return 'O'
                if len(hset) == 3:
                    return '3'
                # otherwise it's a 2-2 or 3-1 card split
                if hand.count(hset[0]) == 2:
                    return 'F'
                return '4'


    cardorder = 'J23456789TQKA'
    cardlist.sort(key=lambda t: [cardorder.index(c) for c in t[0]])
    handorder = 'HOT3F45'
    cardlist.sort(key=lambda t: handorder.index(gethand(t[0])))

with open(inputfile()) as f:
    input = getinput(f)
    cardlist = [line.split() for line in input]
    sortcards(cardlist)
    totala = 0
    for idx, (hand,bid) in enumerate(cardlist):
        totala += (idx+1) * int(bid)

    # Part B
    cardlist = [line.split() for line in input]
    sortcardsb(cardlist)
    totalb = 0
    for idx, (hand,bid) in enumerate(cardlist):
        totalb += (idx+1) * int(bid)

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
