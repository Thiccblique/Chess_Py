import copy
import random
chips = 100
deck = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
rank = list(range(1,14))
suit = ['♠️','♥️','♣️','♦️']
def newdeck():
    fghj = []
    for ranks in rank:
      for suits in suit:
         card = (ranks,suits)
         fghj.append(card)
    fghj = copy.deepcopy(2 * fghj)
    random.shuffle(fghj)
    return fghj
newdeckk = newdeck()
def drawcard(fghj):
   return fghj.pop()
def cardname(card):
   rank,suit = card
   names = {1:'A',11:'J',12:'Q',13:'K'}
   return f"{names.get(rank,str(rank))}{suit}"
def cardvalue(cardname):
   rank,_ = cardname
   if rank == 1:
        return 11
   elif rank >= 11:
        return 10
   else:
       return rank
def hand(cardname):
    total = sum(cardvalue(cardnames) for cardnames in cardname)
    ace = sum(1 for cardnames in cardname if cardnames[0] == 1)
    while total >21 and ace:
        total-=10
        ace-=1
    return total
def showhand(hand):
    return [cardname(card)for card in hand]

while chips > 0:
    print(f"Chips = {chips}")
    while True:
        try:
            bet = int(input("Place Your Bet: "))
            if 1 <= bet <= chips:
                chips -= bet
                break
    
        except ValueError:
            pass
        print(f"Bet must be between 1 and {chips}")
    deck = newdeck()
    player = [drawcard(deck),drawcard(deck)]
    dealer = [drawcard(deck),drawcard(deck)]
    print("Dealer Hand")
    print(f"['{cardname(dealer[0])} ,  ?  ]")
    print("------------")
    print(showhand(player))
    print(f"Player Hand, Total = {hand(player)}")
    hands = []
    bets = []
    rank_zero,_ = player[0]
    rank_one,_ = player[1]
    if rank_zero == rank_one:
        choice = input("Split? (Y/N)").strip().upper()
        if choice == "Y":
            if chips >= bet:
                chips -= bet
                h1 = [player[0],drawcard(deck)]
                h2 = [player[1],drawcard(deck)]
                hands = [h1,h2]
                bets = [bet,bet]
            else: 
                print("Not enough chips")
                hands = [player]
                bets = [bet]
        else:
            hands = [player]
            bets = [bet]
    else:
        hands = [player]
        bets = [bet]
    final_totals = []
    for i, h in enumerate(hands,1):
        print(f"Playing hand #{i}:{showhand(h)},Total = {hand(h)}")
        while True:
            if hand(h) == 21:
                print("Blackjack!")
                chips += int(2.5 * bets[i-1])
                final_totals.append(None)
                break
            elif hand(h) > 21:
                print("Bust!")
                break
            else:
                print("Hit or Stand?(H/S)")
                answer = input()
                while answer != "S" and answer != "H":
                    print("H or S")
                    answer = input()
                if answer == "H":
                    hands[i-1].append(drawcard(deck))
                    print(f"Playing hand #{i}:{showhand(h)},Total = {hand(h)}")
                else:
                    break
        if hand(h) >= 21:
            continue
    print("Dealer Hand")
    print(f"['{cardname(dealer[0])},{cardname(dealer[1])}]")
    print("------------")
    for currhand in hands:
        print(showhand(currhand))
        print(f"Player Hand, Total = {hand(currhand)}")
        print(chips)
        while hand(dealer) <= 16:
            dealer.append(drawcard(deck))
            print("Dealer hits!")
        if  hand(dealer) > 21:
            print("Dealer Busts!")
            chips += int(2 * bets[i-1])
            continue
        else:
            print("Dealer Hand")
            print(showhand(dealer))
            print("------------")
            print(showhand(currhand))
            print(f"Player Hand, Total = {hand(currhand)}")
            if hand(currhand) > hand(dealer):
                print('You Won!')
                chips += int(2 * bets[i-1])
            elif hand(currhand) == hand(dealer):
                print("Draw!")
                chips += int(1 * bets[i-1])
            else:
                print("You Lost!")
                continue
        
        
    
        
                
                