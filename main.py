import sys
import _thread
import time
from PIL import Image, ImageTk
import json
import tkinter as tk

sys.path.append("API/")
from monitor import DataMonitor
sys.path.append("DataStructures/")
from card import Card
from deck import Deck
#    {CARDCODE: [CARD NAME, COST, FACTION]}

class View():
	def __init__(self, master):
		self.frame = tk.Frame(master)

class Controller():
	def __init__(self):
		self.root = tk.Tk()
		self.view = View(self.root)
		self.canvas = tk.Canvas(self.root, width=0, height=0)
		self.canvas.pack()
		self.images = []
		self.cards = []
		self.monitor = DataMonitor()
		self.deck = Deck()
		self.mainDeck = None;
		self.x = 0
		self.y = 0
		self.update()

	"""This function will need to update the information inside the GUI"""
	def update(self):
		self.deck.handle_mouse(self.root, tk)

		if(self.deck.currentDeck == [] and self.monitor.deck != None):
			print("First pass")
			self.deck.initialize_current_deck(self.monitor.deck, self.root, self.canvas)
		elif(self.deck.currentDeck != [] and self.monitor.deck == None):
			self.deck.cleanup(self.root, self.canvas)
		elif(self.deck.currentDeck != [] and self.monitor.deck != None):
			self.deck.update_hand(self.root, self.canvas, self.monitor.hand, self.monitor.acceptHand, self.monitor.newTurn)

		self.root.after(10, self.update)

	def quit(self):
		self.root.destroy()
		sys.exit()

	def run(self):
		self.root.title("Deck Tracker")
		self.root.deiconify()
		self.root.attributes("-topmost", True);
		self.root.resizable(0, 0)
		self.root.geometry("250x0")
		self.root.protocol("WM_DELETE_WINDOW", self.quit)
		
		self.root.mainloop()


if __name__ == '__main__':
	c = Controller()
	c.run()

