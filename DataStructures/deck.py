import json
from card import Card

class Deck:
	def __init__(self):
		self.currentDeck = []
		self.activeDeck = {}
		self.currentHand = None
		self.previousHand = None
		self.acceptedHand = False
		self.currentTurn = 0
		self.currentHandSize = 0
		self.temp = []
		self.cardDictionary = self.get_card_map()

	#Grabs card map of all cards in the game
	def get_card_map(self):
		with open('./DataStructures/card_dictionary.json') as json_file:
			data = json.load(json_file)
			return data

	#First pass to initialize the current player's deck.  Configuring the canvas format to fit the card
	def initialize_current_deck(self, currentDeck, root, canvas):
		height = len(currentDeck) * 40 + 10
		height = str(height)
		canvas.configure(width=250, height=height, background="#292A34")
		root.geometry("250x" + height)
		yOffset = 10

		for element in currentDeck:
			newCard = Card(0, 0, 200, 30, str(element), currentDeck[element], self.cardDictionary[element][2], self.cardDictionary[element][1])
			self.activeDeck[element] = [self.cardDictionary[element][0], self.cardDictionary[element][1], self.cardDictionary[element][2], self.cardDictionary[element][3], currentDeck[element]]
			self.insert_sorted(newCard)

		for element in self.currentDeck:
			element.init_location(25, yOffset)
			element.draw_card_full(canvas)
			yOffset += 40

		self.list_to_dict()

	#Converting our deck of card objects to dictionary
	def list_to_dict(self):
		self.currentDeck = {self.currentDeck[i].code : self.currentDeck[i] for i in range(0, len(self.currentDeck))}

	#When the current hand grows we know to remove the cards from the deck
	def update_hand(self, root, canvas, gameHand, acceptHand, newTurn):
		#At the start of the game find the initial hand after mulligan (if no mulligan we still wait for the first 5 cards)
		if acceptHand == True and self.acceptedHand == False:
			self.check_initial_hand(root, canvas, gameHand)

		if self.acceptedHand == True:
			if self.currentTurn != newTurn:
				self.currentTurn = newTurn
				self.currentHand = gameHand

			self.check_running_hand(root, canvas, gameHand)

	#This looks for the first 5 cards to be in hand before we continue to update
	def check_initial_hand(self, root, canvas, gameHand):
		cardCount = 0

		for element in gameHand:
			cardCount += gameHand[element]

		if cardCount == 5:
			self.acceptedHand = True
			print(gameHand)
			self.currentHand = gameHand
			self.update_deck(root, canvas, self.currentHand)

	#Function to check changes in the hand
	#Since hovering cards removes them from the API call.  We only care when we have more
	#of said card in the current hand.  If we made the change everytime a card dissappeared
	#and reappeared we would draw from the deck when we hover a card in our hand
	#On every new turn we reset the process for the currentHand
	def check_new_card(self, root, canvas, gameHand):
		for element in gameHand:
			#print("Looking at element: ", print(element))
			#sub = str(element)
			#sub = sub[len(sub)-2:]
			#print(sub)
			#if sub == "T1" or sub == "T2":
			#	print("strange card")
			#Some cards get generated that aren't in the deck.  We ignore them when they do no exist in the main deck
			
			checkRunningHand = self.currentHand.get(element)
			checkActiveDeck = self.activeDeck.get(element)

			#New card found this means its been pulled from the main deck
			if checkRunningHand == None and checkActiveDeck != None:
				self.currentHand[element] = gameHand[element]
				self.update_deck(root, canvas, {element: self.currentHand[element]})

			#This will run when we have acquired a new card that is the same as one in our hand
			if checkRunningHand != None and checkActiveDeck != None:
				if gameHand[element] > self.currentHand[element]:
					self.currentHand[element] = gameHand[element]
					self.update_deck(root, canvas, {element: 1})

	#Function to update the running hand when new cards come into play
	def check_running_hand(self, root, canvas, gameHand):
		if self.currentHand == gameHand:
			pass
		else:
			self.check_new_card(root, canvas, gameHand)

	#Function to update our current deck elements and GUI
	def update_deck(self, root, canvas, cards):
		for element in cards:
			if element in self.activeDeck.keys():
				self.activeDeck[element][4] -= cards[element]
				if element in self.currentDeck.keys():
					self.currentDeck[element].update_number(canvas, self.activeDeck[element][4])

	#Insert card in sorted order according to their mana cost
	def insert_sorted(self, card):
		self.currentDeck.append(card)
		self.currentDeck.sort(key=lambda x: x.cost, reverse=False)

	#Handles returning correct hovered card
	def handle_mouse(self, root, tk):
		x, y = root.winfo_pointerx(), root.winfo_pointery()

		absX, absY = x - root.winfo_rootx(), y - root.winfo_rooty()
			
		for element in self.currentDeck:
			cardCode = self.currentDeck[element].get_bounds(absX, absY, root, tk)

	def cleanup(self, root, canvas):
		self.currentDeck.clear()
		self.currentDeck = []
		self.currentHand = None
		root.geometry("250x0")
		canvas.delete("all")
		canvas.configure(width=0, height=0)
		self.acceptedHand = False
		self.currentTurn = 0