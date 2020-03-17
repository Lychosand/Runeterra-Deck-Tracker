import sys
import json

newMap = dict()

with open("set1-en_us.json", 'r', encoding="cp866") as json_file:
	data = json.load(json_file)
	for p in data:
		card_code = p['cardCode']
		card_name = p['name']
		card_cost = p['cost']
		card_region = p['regionRef']
		card_refs = p['associatedCardRefs']
		newMap[card_code] = [card_name, card_cost, card_region, card_refs]

newMap = json.dumps(newMap)
loadedMap = json.loads(newMap)


with open('card_dictionary.json', 'w') as json_file:
	json.dump(loadedMap, json_file, indent=4)