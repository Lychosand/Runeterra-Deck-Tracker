import requests
import json

URL = "http://127.0.0.1:21337";

def get_static_deck():
	response = None;
	deckMap = dict();
	try:
		response = requests.get(url = URL + "/static-decklist");
	except:
		return -1
	data = response.json()

	data = data['CardsInDeck']

	for key in data:
		deckMap[key] = data[key]

	return deckMap

def get_current_cards():
	r = requests.get(url = URL + "/positional-rectangles");
	data = r.json();
	data = data['Rectangles'];
	handMap = dict();
	for key in data:
		if(key['LocalPlayer'] and key['CardCode'] != 'face'):
			if(key['CardCode'] in handMap):
				handMap[key['CardCode']] += 1;
			else:
				handMap[key['CardCode']] = 1;

	return handMap;

def get_game_state():
	response = None
	try:
		response = requests.get(url = URL +"/positional-rectangles");
	except:
		return -1

	data = response.json();
	return data['GameState'];