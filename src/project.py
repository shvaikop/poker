import random
from tkinter import *
# random.seed(888)

WIDTH = 1000
HEIGHT = 600


# Cards: 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack - 11, Queen - 12, King - 13, Ace - 14
# Suits: Spades - 1, Clubs - 2, Diamonds - 3, Hearts - 4
VALS_dict = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:'J', 12:'Q', 13:'K', 14:'A'}
SUIT_dict = {1:'♠', 2:'♣', 3:'♢', 4:'♡'}
HAND_RANKS = {0: 'High Card', 1: 'Pair', 2: 'Two Pair', 3: 'Three of a Kind', 4: 'Straight',
              5: 'Flush', 6: 'Full House', 7: 'Four of a Kind', 8: 'Straight Flush', 9: 'Royal Flush'}

class Card:
    def __init__(self, value = None, suit = None):
        self.value = value
        self.suit = suit
        
    def __repr__(self):
        return f'|{VALS_dict[self.value]} {SUIT_dict[self.suit]}|'

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

# Deck class
class Deck(list):
    def __init__(self):
        super().__init__()
        suits = [1, 2, 3, 4]
        values = list(range(2, 15))
        for val in values:
            for suit in suits:
                self.append(Card(val, suit))

    # Pops one card from the deck
    def deal(self):
        return self.pop()

    def shuffle(self):
        random.shuffle(self)

class Hand(list):
    def __init__(self, ls = None):
        if ls == None:
            super().__init__()
        else:
            super().__init__(ls)

    def sort_vals(self):
        l = len(self)
        hand_nums = []
        for i in range(l):
            hand_nums.append((self[i].value, self[i].suit))
        hand_nums.sort()
        for i in range(l):
            self[i] = Card(hand_nums[i][0], hand_nums[i][1])
    
    def sort_suit(self):
        l = len(self)
        hand_nums = []
        for i in range(l):
            hand_nums.append((self[i].suit, self[i].value))
        hand_nums.sort()
        for i in range(l):
            self[i] = Card(hand_nums[i][1], hand_nums[i][0])    

    def hand_rank(self):
        # Sorting the hand by value
        self.sort_vals()
        # Creating a list of card values in reverse sorted order
        vals_sorted = []
        for i in range(len(self) - 1, -1, -1):
            vals_sorted.append(self[i].value)
        output = None

        ### Check for Royal Flush ###
        output = isRoyalFlush(self)
        if output:
            for j in range(len(output)):
                output[j] = output[j].value
            return [9, output[:5], None]
        self.sort_vals()
        
        ### Check for Straight Flush ###
        output = isStraightFlush(self)
        if output:
            for j in range(len(output)):
                output[j] = output[j].value
            return [8, output[:5], None]
        self.sort_vals()

        ### Check for Four of a kind ###
        output = isFour(self)
        if output != []:
            output = output * 4
            for i in vals_sorted:
                if i != output[0]:
                    output.append(i)
                    break
            return [7, output, None]
        output = None

        ### Check for Full House ###
        output = isFullHouse(self)
        if output:
            out = [output[0]] * 3
            out1 = [output[1]] * 2
            output = out + out1
            return [6, output, None]
        output = None

        ### Check for Flush ###
        output = isFlush(self)
        if output:
            output = list(reversed(output))
            for j in range(len(output)):
                # print(output[i])
                output[j] = output[j].value
            return [5, output[:5], None]

        ### Check for Straight ###
        self.sort_vals()
        output = isStraight(self)
        if output:
            for j in range(len(output)):
                output[j] = output[j].value
            return [4, output[:5], None]

        ### Check for Three of a kind ###
        output = isThree(self)
        if output != []:
            output = [output[0]] * 3
            for i in vals_sorted:
                if len(output) == 5:
                    break
                if i != output[0]:
                    output.append(i)
            return [3, output, None]

        ### Check for one pair/two pair ###
        output = isPair(self)
        if output != []:
            if len(output) > 1:
                out = [output[0]] * 2
                out1 = [output[1]] * 2
                output = out + out1
                for i in vals_sorted:
                    if i != output[0] and i != output[2]:
                        output.append(i)
                        break
                return [2, output, None]
            else:
                output = output * 2
                for i in vals_sorted:
                    if len(output) == 5:
                        break
                    if i != output[0]:
                        output.append(i)
                return [1, output, None]
        ### Check hand for high card ###
        
        
        return [0, vals_sorted[:5], None]


def test():
    h = Hand([Card(5,1), Card(3,2), Card(10,3), Card(11,3), Card(12,3), Card(13,3), Card(14,3)])
    print(h.hand_rank())    # Royal Flush

    h = Hand([Card(5,1), Card(3,3), Card(4,3), Card(5,3), Card(6,3), Card(7,3), Card(14,3)])
    print(h.hand_rank())    # Straight Flush

    h = Hand([Card(5,1), Card(3,2), Card(5,3), Card(11,3), Card(5,2), Card(13,3), Card(5,4)])
    print(h.hand_rank())    # Four of a Kind

    h = Hand([Card(5,1), Card(3,2), Card(5,3), Card(11,3), Card(11,2), Card(13,3), Card(5,4)])
    print(h.hand_rank())    # Full House

    h = Hand([Card(5,1), Card(3,1), Card(4,1), Card(11,3), Card(5,1), Card(13,1), Card(5,4)])
    print(h.hand_rank())    # Flush

    h = Hand([Card(5,1), Card(3,2), Card(5,3), Card(4,3), Card(6,2), Card(7,3), Card(5,4)])
    print(h.hand_rank())    # Straight

    h = Hand([Card(5,1), Card(3,2), Card(6,3), Card(11,3), Card(5,2), Card(13,3), Card(5,4)])
    print(h.hand_rank())    # Three of a Kind

    h = Hand([Card(5,1), Card(3,2), Card(5,3), Card(11,3), Card(13,2), Card(13,3), Card(8,4)])
    print(h.hand_rank())    # Two pair

    h = Hand([Card(5,1), Card(3,2), Card(6,3), Card(11,3), Card(5,2), Card(13,3), Card(7,4)])
    print(h.hand_rank())    # Pair

    h = Hand([Card(5,1), Card(3,2), Card(4,3), Card(7,3), Card(9,2), Card(13,3), Card(14,4)])
    print(h.hand_rank())    # High card


# Fuction that checks if a {player} has a flush
# Returns None if there is no flush
# Otherwise returns a list of cards in the flush
def isFlush(hand_cards): # Input: hand of cards sorted by suit
    # hand_cards = Hand([Card(14,2), Card(10,2), Card(11,2), Card(13,2), Card(12,2), Card(13,3), Card(14,3)])
    # print(hand_cards)
    hand_cards.sort_suit()
    # print(hand_cards)
    counter = 1
    output = []
    output.append(hand_cards[-1])
    for i in range(len(hand_cards) - 1, 0, -1):
        
        # print(f'i = {i} counter = {counter}')
        if hand_cards[i - 1].suit == hand_cards[i].suit:
            output.append(hand_cards[i - 1])
            counter += 1
        # print(i, counter)
        if hand_cards[i - 1].suit != hand_cards[i].suit or i == 1:
            if counter >= 5:
                # print(output)
                # for j in range(len(output)):
                #     # print(output[i])
                #     output[j] = output[j].value
                output = Hand(output)
                output.sort_vals()
                return output
            else:
                output = []
                output.append(hand_cards[i - 1])
                counter = 1

# Function that checks if a {player} has a straight
# Return None if no straigt
# Returns a list of cards part of the straight sequence, not known if ascending or descending
# Card with highest value might be in the middle of the list
def isStraight(hand_cards):
    hand_cards = Hand(hand_cards)
    # Go through the hand, detect duplicates, add duplicates to a list
    i_to_delete = []    # List that holds indices in the hand list that should be deleted
    duplicates = []     # List that holds 'dupl's
    dupl = []   # List that holds single value duplicates
    for i in range(len(hand_cards) - 1):
        if hand_cards[i].value == hand_cards[i + 1].value:
            i_to_delete.append(i + 1)
            if dupl == []:
                dupl.append(hand_cards[i])
                dupl.append(hand_cards[i + 1])
            else:
                dupl.append(hand_cards[i + 1])
        if hand_cards[i].value != hand_cards[i + 1].value or i == len(hand_cards) - 2:
            if dupl != []:
                duplicates.append(dupl)
                dupl = []

    # Reverse i_to_delete list to delete from the end
    # Delete duplicates from hand_cards
    i_to_delete = list(reversed(i_to_delete))
    # print(i_to_delete)
    for i in i_to_delete:
        del hand_cards[i]

    # If length of hand without duplicates is less than 5
    # return None straight away
    if len(hand_cards) < 5:
        return None

    # Check for straight
    straight = []
    straight.append(hand_cards[-1])
    l = len(hand_cards)
    for i in range(l - 1, -1, -1):
        if hand_cards[i].value - hand_cards[(i - 1) % l].value == 1:
            straight.append(hand_cards[(i - 1) % l])
        elif hand_cards[i].value == 2 and hand_cards[(i - 1) % l].value == 14:
            straight.append(hand_cards[(i - 1) % l])
        else:
            if len(straight) >= 5:
                break
            else:
                straight = []
                straight.append(hand_cards[(i - 1) % l])
    if len(straight) < 5:
        return None
    else:
        return straight
    
def isStraightFlush(sorted_hand):
    output = isFlush(sorted_hand)
    if output:
        output = isStraight(output)
        if output:
            return output

def isRoyalFlush(sorted_hand):
    output = isStraightFlush(sorted_hand)
    if output:
        if output[0].value == 14 and output[4].value == 10:
            return output

def consec_comb(sorted_hand, n):
    r_val = []
    counter = 1
    for i in range(len(sorted_hand) -1, 0, -1):
        if sorted_hand[i].value == sorted_hand[i - 1].value:
            counter += 1
        else:
            counter = 1
        if counter >= n:
            r_val.append(sorted_hand[i].value)
    return r_val

# Function checks whether a player has four of a kind
# returns None or the card value that makes up the combination
def isFour(sorted_hand):
    return consec_comb(sorted_hand, 4)

def isThree(sorted_hand):
    return consec_comb(sorted_hand, 3)

def isPair(sorted_hand):
  return consec_comb(sorted_hand, 2)

def isFullHouse(sorted_hand):
    threes = isThree(sorted_hand)
    twos = isPair(sorted_hand)
    if threes != [] and twos != []:
        for i in threes:
            for j in twos:
                if i != j:
                    return [i,j]
        return None
    return None


class Player:
    def __init__(self):
        self.name = None
        self.cash = 1000
        self.card = [None] * 2


class Game():
    def __init__(self, num_of_players):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_of_players = num_of_players
        self.pot = 0
        self.won = False    # index of player that won; otherwise None
        self.player = [None] * num_of_players     # List that contains players still in the game
        for i in range(num_of_players):
            self.player[i] = Player()
        self.minBet = 50    # starting value, should reload after each betting round
        self.communityCards = []

        self.playerBets = [0] * num_of_players
        self.lastPlayer = 0     # Last player that raised, round played till him
        self.starting = 0

        self.turn = 0
        self.round = 0
        self.dealCards()
        reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet)

    def reloadGame(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.minBet = 50    # starting value, should reload after each betting round
        self.communityCards = []

        self.playerBets = [0] * self.num_of_players

        for i in range(self.num_of_players):
            self.player[i].card = [None] * 2

        self.round = 0
        self.dealCards()

        self.starting = (self.starting + 1) % self.num_of_players
        self.turn = self.starting
        while self.player[self.turn].card == None or self.player[self.turn].cash == 0:
            self.turn += 1
        self.lastPlayer = self.turn
        reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet)

    def dealCards(self):
        for i in range(self.num_of_players):
            if self.player[i].cash == 0:
                self.player[i].card = None
                continue
            for j in range(2):
                self.player[i].card[j] = self.deck.deal()

    def dealComCards(self, n):
        for i in range(n):
            self.communityCards.append(self.deck.deal())
    
    def winner(self):
        self.hands = []
        for i in range(self.num_of_players):
            if self.player[i].card != None:
                crds = list(self.communityCards)
                crds.append(self.player[i].card[0])
                crds.append(self.player[i].card[1])
                self.hands.append(Hand(crds).hand_rank()) ###
                self.hands[-1][2] = i
        self.hands.sort(reverse=True)
        print(self.hands)
        # Further check if players have equal hands if 5 out of 7 cards are compared
        winners = []
        winners.append(self.hands[0][2])
        i = 1
        while self.hands[0][0] == self.hands[i][0] and self.hands[0][1] == self.hands[i][1]:
            winners.append(self.hands[i][2])
            i += 1
            if i == len(self.hands):
                break
        
        for p in winners:
            self.player[p].cash += self.pot // len(winners)

        w = [str(x) for x in winners]
        print(f'Player/s ' + ', '.join(w) + f' won with a {HAND_RANKS[self.hands[0][0]]}')
        self.reloadGame()

    def checkOnFinishRound_call(self):
        self.turn = self.starting
        while self.player[self.turn].card == None or self.player[self.turn].cash == 0:
            self.turn += 1
            self.turn = self.turn % self.num_of_players

        self.lastPlayer = self.turn
        self.playerBets = [0] * self.num_of_players
        self.round += 1
        self.minBet = 0
        if self.round == 1:
            self.dealComCards(3)
        elif self.round == 4: # game finished
            self.winner()
        else:
            self.dealComCards(1)
        # print(f'round {self.round}')

    # Function that returns the number of players still in the game
    def playersPlaying(self):
        counter = 0
        index = None
        for i in range(self.num_of_players):
            if self.player[i].card != None:
                counter += 1
                index = i
        return (counter, index)

    def playersWithMoney(self):
        counter = 0
        for i in range(self.num_of_players):
            if self.player[i].cash != 0 and self.player[i].card != None:
                counter += 1
        return counter

    def increaseTurn(self):
        ### Check if there is 1 player in the game
        #   If yes, this player wins, gets the money
        #   New game
        num, id = self.playersPlaying()
        # print(f'num, id {num, id}')
        if num == 1:
            ### Print message this player won
            self.player[id].cash += self.pot
            print(f'Player {id + 1} WON!!!')
            # winning_message_1(id)
            self.reloadGame()
            return

        ### Check how many players still have money
        #   If only 1 then deal remaining community cards
        #   Call winner method
        num = self.playersWithMoney()
        if num < 1:
            # print(self.communityCards)
            if len(self.communityCards) < 5:
                self.dealComCards(5 - len(self.communityCards))
            # print(self.communityCards)
            self.winner()
            return
        
        self.turn += 1
        self.turn = self.turn % self.num_of_players
        if self.turn % self.num_of_players == self.lastPlayer:
            self.checkOnFinishRound_call()
            return
        
        while self.player[self.turn].card == None or self.player[self.turn].cash == 0:
            if self.turn % self.num_of_players == self.lastPlayer:
                break
            else:
                self.turn += 1
                self.turn = self.turn % self.num_of_players
        # print(self.turn)
        if self.turn % self.num_of_players == self.lastPlayer:
            self.checkOnFinishRound_call()

        

    def call(self, up):
        if self.round < 4:
            if up != None:  # player is raising
                if up > self.minBet and up < self.player[self.turn].cash:
                    self.minBet = up
                    self.lastPlayer = self.turn
                elif up > self.minBet and up >= self.player[self.turn].cash:
                    if self.player[self.turn].cash > self.minBet:
                        self.minBet = self.player[self.turn].cash
                        self.lastPlayer = self.turn
            if self.minBet == 0:
                self.lastPlayer = self.turn
                self.minBet = 50

            if self.player[self.turn].cash < self.minBet:
                self.pot += self.player[self.turn].cash
                self.player[self.turn].cash = 0
            else:
                self.player[self.turn].cash -= self.minBet - self.playerBets[self.turn]
                self.playerBets[self.turn] = self.minBet
                self.pot += self.minBet

            self.increaseTurn()
            
        # print(f'pot {self.pot}')
        # print(f'player {self.player[self.turn - 1].cash}')
        # if self.minBet == 0:
        #     reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet)
        # else:
        reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet - self.playerBets[self.turn])
        # reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet)
    
    def check(self):
        if self.minBet == 0:
            self.increaseTurn()
            reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet)

    def fold(self):
        self.player[self.turn].card = None
        self.increaseTurn()

        # if self.minBet == 0:
        #     reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet)
        # else:
        reload_view(self.player, self.turn, self.communityCards, self.pot, self.minBet - self.playerBets[self.turn])



root = Tk()
root.title('Poker')
canvas = Canvas(root, width = WIDTH, height = HEIGHT, background="#148232")
canvas.grid()

#region: Welcome window
canvas.create_text(500, 150, text = 'Welcome to Poker', font=('Helvetica', 50))
entry1 = Entry (root) 
canvas.create_window(500, 400, window=entry1, height=30, width=100)
canvas.create_text(500, 350, text='Enter the number of players: (2 - 8)', font=('Helvetica', 20))

# def winning_message_1(player_number):
#     # print('djdjdjdjd')
#     st = f'Player {player_number + 1} WON!!!'
#     print(st)
#     canvas.create_text(500, 340, text= st, fill='red', font=('Helvetica', 20))

#     buttonContinue = Button(text='Continue', command=game.reloadGame(), font=15)
#     canvas.create_window(500, 360, window=buttonContinue, width=100, height=35)
coords_x = [100, 300, 500, 700, 900, 700, 500, 300]
coords_y = [250, 50, 50, 50, 250, 500, 500, 500]

def reload_view(players, turn, com_cards, pot, to_call):    # List of players
    global coords_x, coords_y
    canvas.delete('cash')
    canvas.delete('turn')
    

    # Turn pointer
    if turn < 5: 
        canvas.create_oval(coords_x[turn] - 60, coords_y[turn] - 30, coords_x[turn] + 60, coords_y[turn] + 50, fill='#2dc90e', tags='turn', outline='')
    else:
        canvas.create_oval(coords_x[turn] - 60, coords_y[turn] - 50, coords_x[turn] + 60, coords_y[turn] + 30, fill='#2dc90e', tags='turn', outline='')

    for i in range(len(players)): 
        canvas.create_text(coords_x[i], coords_y[i], text="Player " + str(i + 1), fill='#a31ca1', font=('Helvetica', 16, 'bold'))
        if i < 5: 
            canvas.create_text(coords_x[i], coords_y[i] + 30, text='$' + str(players[i].cash), tags='cash', fill='#FFD700', font=('Helvetica', 12, 'bold'))
        else:
            canvas.create_text(coords_x[i], coords_y[i] - 25, text=str(players[i].cash), tags='cash', fill='#FFD700', font=('Helvetica', 12, 'bold'))

    s = ''
    for i in range(len(com_cards)):
        s += repr(com_cards[i]) + '  '
    canvas.create_text(500, 300, text=s, tags='cash', fill='black', font=('Helvetica', 20))
    canvas.create_text(500, 260, text= '$' + str(pot), tags='cash', fill='#FFD700', font=('Helvetica', 16))
    canvas.create_text(500, 360, text= 'To call: $' + str(to_call), tags='cash', fill='orange', font=('Helvetica', 16))

entryRaise = None
game = None
def TkCall():
    global entryRaise
    global game
    n = entryRaise.get()
    if n != '':
        n = int(n)
    else:
        n = None
    game.call(n)

def TkCheck():
    game.check()

def TkFold():
    game.fold()

def NumOfPlayers():
    global game
    global entryRaise
    
    n = entry1.get()
    if not n.isdigit():
        return
    n = int(n)
    if not 2 <= n <= 8:
        return

    canvas.delete('all')
    game = Game(n)

    buttonCall = Button(text='Bet / Call', command=TkCall, font=15)
    canvas.create_window(810, 570, window=buttonCall, width=100, height=35)

    entryRaise = Entry (root)
    canvas.create_window(920, 570, window = entryRaise, height=30, width=100)

    buttonCheck = Button(text='Check', command=TkCheck, font=15)
    canvas.create_window(650, 570, window=buttonCheck, width=100, height=35)

    buttonFold = Button(text='Fold', command=TkFold, font=15)
    canvas.create_window(100, 570, window=buttonFold, width=100, height=35)



button1 = Button(text='Enter', command=NumOfPlayers, font=15)
canvas.create_window(500, 450, window=button1, width=80, height=35)
#endregion

def clicked(event, x = 6):
    if game == None:
        return
    global coords_x, coords_y
    i = None
    for j in range(game.num_of_players):
        if (coords_x[j] - 70 < event.x < coords_x[j] + 70) and (coords_y[j] - 45 < event.y < coords_y[j] + 45):
            i = j
            break
    if i == None:
        return
        
    if i < 5: 
        if game.player[i].card != None:
            s = repr(game.player[i].card[0]) + ' ' + repr(game.player[i].card[1])
            canvas.create_text(coords_x[i], coords_y[i] + 65, text=s, tags='cards', fill='black', font=('Helvetica', 20))
    else:
        if game.player[i].card != None:
            s = repr(game.player[i].card[0]) + ' ' + repr(game.player[i].card[1])
            canvas.create_text(coords_x[i], coords_y[i] - 65, text=s, tags='cards', fill='black', font=('Helvetica', 20))

def released(event):
    canvas.delete('cards')

canvas.bind('<Button>', clicked)
canvas.bind('<ButtonRelease>', released)
root.mainloop()


