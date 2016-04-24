import pymongo
import random

client = pymongo.MongoClient('localhost', 27017)

db = client.hearthstone
card_collection = db.cards


PACK_SIZE = 15

def random_pack():
	cards = list(card_collection.find())

	pack = []
	for i in range(0,PACK_SIZE):
		pack.append(random.choice(cards))

	return cards

print random_pack()


def create_pack(params):
	pass