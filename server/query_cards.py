import unirest
import json
import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client.hearthstone
card_collection = db.cards

def get_cards_from_api():
	response = unirest.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards?collectible=1",
  		headers={
    		"X-Mashape-Key": "Kv2act4lSmmshliZ7JasXPYR6wiop1ZKZgzjsn4OcmVrAaGvsJ"
  		}	
	)

	card_collection.drop()

	for s, cards in response.body.items():
		for card in cards:
			if card["type"] in ["Minion", "Spell", "Weapon"]:
				if not card.get("playerClass", None):
					card["playerClass"] = "Neutral"
				card_collection.insert(card)


	db.cards.create_index([('cardId', pymongo.ASCENDING)], unique=True)

get_cards_from_api()
