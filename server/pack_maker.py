import pymongo
import random

import collections
import functools

class memoized(object):
	'''Decorator. Caches a function's return value each time it is called.
	If called later with the same arguments, the cached value is returned
	(not reevaluated).
	'''
	def __init__(self, func):
		self.func = func
		self.cache = {}
	def __call__(self, *args):
		if not isinstance(args, collections.Hashable):
    		# uncacheable. a list, for instance.
      		# better to not cache than blow up.
			return self.func(*args)
		if args in self.cache:
			return self.cache[args]
		else:
			value = self.func(*args)
			self.cache[args] = value
			return value
  	def __repr__(self):
		'''Return the function's docstring.'''
		return self.func.__doc__
  	def __get__(self, obj, objtype):
		'''Support instance methods.'''
		return functools.partial(self.__call__, obj) 

client = pymongo.MongoClient('localhost', 27017)

db = client.hearthstone
card_collection = db.cards


PACK_SIZE = 15
CLASSES = ["Druid","Hunter","Mage","Paladin","Priest","Rogue","Shaman","Warlock","Warrior"]
NEUTRAL = "Neutral"
SETS = ["Classic", "Goblins vs Gnomes", "Blackrock Mountain", "The Grand Tournament", "The League of Explorers", "Whispers of the Old Gods"]
RARITY = ["Legendary", "Epic", "Rare", "Common"]

@memoized
def get_cards_by_set(sets):
	return list(card_collection.find({"cardSet": { '$in': sets}}))


def random_pack():
	cards = list(card_collection.find())

	pack = []
	for i in range(0,PACK_SIZE):
		pack.append(random.choice(cards))

	return pack

print map(lambda x: x['name'], random_pack())


def create_pack(num_cards = 15, sets = SETS, rarity = {"Legendary":0, "Epic":1, "Rare":3, "Common":11}):
	pack = []
	all_cards = get_cards_by_set(tuple(sets))
	
	rarities = []
	for r in RARITY:
		rarities = rarities + [r] * rarity[r]
	class_cards = CLASSES + [NEUTRAL] * 6
	random.shuffle(class_cards)

	for i in range(0, num_cards):
		cards = filter( lambda x: x["playerClass"] == class_cards[i] and x["rarity"] == rarities[i], all_cards)
		pack.append(random.choice(cards))

	return pack

print map(lambda x: x['name'], create_pack(sets=["Classic"]))





