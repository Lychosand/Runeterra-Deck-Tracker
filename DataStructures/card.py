#Data structure for handling the specific cards in a deck
from PIL import Image, ImageTk

class Card:
	def __init__(self, x, y, w, h, code, number, faction, cost):
		self.width = w
		self.height = h
		self.top = 0
		self.left = 0
		self.right = 0
		self.bottom = 0
		self.code = code
		self.image = self.init_image("./Images/Full/" + str(self.code) + "-full.png")	
		self.cardImage = self.init_image("./Images/Cards/" + str(self.code) + ".png")
		self.totalNumber = self.init_image("./Images/Amount/" + str(number) + ".png")
		self.transparent = self.init_image("./Images/Full/transparent.png")
		self.cost = cost
		self.number = number
		self.cardCost = self.init_image("./Images/Cost/" + str(cost) + ".png")
		self.hovered = False
		self.showing = False
		self.popup = None
		self.popupCanvas = None
		self.color = self.init_color(faction)

	#Determines the faction color for the card
	def init_color(self, faction):
		if(faction == "Demacia"):
			return 'AntiqueWhite1'
		elif(faction == "Ionia"):
			return 'hot pink'
		elif(faction == 'Noxus'):
			return 'red3'
		elif(faction == 'PiltoverZaun'):
			return 'orange'
		elif(faction == 'Freljord'):
			return 'pale turquoise'
		elif(faction == 'ShadowIsles'):
			return 'aquamarine'
		else:
			return 'black'

	#Initializes the current location of the card
	def init_location(self, x, y):
		self.left = x
		self.top = y
		self.right = self.left + self.width
		self.bottom = self.top + self.height

	#Acquires the correct image to display for the card from the cardcode
	def init_image(self, string):
		image = None
		try:
			image = Image.open(string)
		except:
			image = Image.open("Images/Amount/default.png")

		image = ImageTk.PhotoImage(image)
		return image

	#Determines if a current card is being hovered
	def get_bounds(self, x, y, root, tk):
		if(x > self.left and x < self.right and y > self.top and y < self.bottom):
			self.hovered = True
		else:
			self.hovered = False
			self.showing = False

		self.create_popup(root, tk)

	#Updates the ammount of cards left in the deck to draw on the GUI
	def update_number(self, canvas, number):
		self.totalNumber = self.init_image("Images/Amount/" + str(number) + ".png")

		if(number == 0):
			self.draw_transparent(canvas)

		self.draw_number(canvas)

	#Function to draw out all elements of the card
	def draw_card_full(self, canvas):
		self.draw_rounded_border(canvas, 30, 3, self.color)
		canvas.create_image(self.left, self.top, image=self.image, anchor='nw')
		self.draw_number(canvas)
		self.draw_cost(canvas)

	#Draws a transparent black overlay for when the deck is out of the current card
	def draw_transparent(self, canvas):
		canvas.create_image(self.left, self.top, image=self.transparent, anchor='nw')

	def draw_card(self, canvas):
		self.popupCanvas.create_image(0, 0, image=self.cardImage, anchor='nw')

	def draw_number(self, canvas):
		canvas.create_image(self.right - 30, self.top + 3, image=self.totalNumber, anchor='nw')

	def draw_cost(self, canvas):
		canvas.create_image(self.left + 2, self.top + 2, image=self.cardCost, anchor='nw')

	def draw_rounded_border(self, canvas, radius, increase, color):
		points = [self.left+radius-increase, self.top-increase,
				  self.left+radius-increase, self.top-increase,
				  self.right-radius+increase, self.top-increase,
				  self.right-radius+increase, self.top-increase,
				  self.right+increase, self.top-increase,
				  self.right+increase, self.top+radius-increase,
				  self.right+increase, self.top+radius-increase,
				  self.right+increase, self.bottom-radius+increase,
				  self.right+increase, self.bottom-radius+increase,
				  self.right+increase,self.bottom+increase,
				  self.right-radius+increase, self.bottom+increase,
				  self.right-radius+increase, self.bottom+increase,
				  self.left+radius, self.bottom+increase,
				  self.left+radius, self.bottom+increase,
				  self.left-increase, self.bottom+increase,
				  self.left-increase, self.bottom-radius+increase,
				  self.left-increase, self.bottom-radius+increase,
				  self.left-increase, self.top+radius-increase,
				  self.left-increase, self.top+radius-increase,
				  self.left-increase, self.top-increase]

		canvas.create_polygon(points, fill=color, smooth=True)

	#Function creates the popup animation for when the user hover's the card
	def create_popup(self, root, tk):
		if(self.hovered == True and self.showing == False):
			self.popup = tk.Toplevel(root)

			popupLeft = root.winfo_rootx() + self.right + 20
			popupTop = root.winfo_rooty() + self.top - 135

			#Don't let cards come off screen
			if(popupTop < root.winfo_rooty()):
				popupTop = root.winfo_rooty()
			elif(popupTop + 350 > root.winfo_rooty() + root.winfo_height()):
				popupTop = root.winfo_rooty() + root.winfo_height() - 350

			self.popup.geometry('250x350+' + str(popupLeft) + '+' + str(popupTop))
			self.popupCanvas = tk.Canvas(self.popup, width=250, height=350)
			self.popupCanvas.pack(fill="both", expand=True)
			
			self.showing = True

			self.popup.overrideredirect(True)
			self.popup.lift()

			self.popup.wm_attributes("-topmost", True)
			self.popup.wm_attributes("-disabled", True)
			self.popup.wm_attributes('-transparentcolor', self.popup['bg'])

			self.draw_card(self.popupCanvas)
		elif(self.hovered == False and self.showing == False and self.popup != None):
			self.popupCanvas.configure(width=0, height=0)
			self.popup.destroy()
			self.popup = None
			
