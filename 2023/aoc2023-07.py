# Timings: Part A: 10:00 / Part B: Fun Run
import os
from collections import Counter

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

def gethand(hand):
    ctr = Counter(hand)
    mc = ctr.most_common()
    if mc[0][1] == 5: return '5'
    if mc[0][1] == 4: return '4'
    if mc[0][1] == 3:
        if mc[1][1] == 2:
            return 'F'
        return '3'
    if ctr.most_common()[0][1] == 2:
        if mc[1][1] == 2:
            return 'T'
        return 'O'
    if ctr.most_common()[0][1] == 1:
        return 'H'
        
def sortcards(cardlist):
    cardorder = '23456789TJQKA'
    cardlist.sort(key=lambda t: [cardorder.index(c) for c in t[0]])
    handorder = 'HOT3F45'
    cardlist.sort(key=lambda t: handorder.index(gethand(t[0])))

def sortcardsb(cardlist):
    def gethandb(hand):
        ctr = Counter(hand)
        if 'J' not in ctr:
            return gethand(hand)
        else: # Use the Joker to make a stronger hand 
            # Replace each joker with the most common card.
            jcount = hand.count('J')
            if jcount == 5: return '5'
            del ctr['J']
            ctr[ctr.most_common(1)[0][0]] += jcount
            nhand = ''
            for e,c in ctr.items():
                nhand += ''.join([e*c])
            return gethand(nhand)

    cardorder = 'J23456789TQKA'
    cardlist.sort(key=lambda t: [cardorder.index(c) for c in t[0]])
    handorder = 'HOT3F45'
    cardlist.sort(key=lambda t: handorder.index(gethandb(t[0])))

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
