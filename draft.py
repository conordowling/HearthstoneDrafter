import pack_maker as pm
from python_algorithms.basic.queue import Queue

NUM_PACKS = 3

class Draft:

	def __init__(self, player_ids, settings = {}):
		self.player_names = { player_ids[i]: i for i in range(0,len(player_ids)) }
		self.settings = settings
		players = [ Player(players_ids[i]) for i in range(0,len(player_ids)) ]
		for player in players:
			player.pack_queue.put(pm.create_pack())
			player.packs += 1



	def pick_card(self, player, cardId):
		pid = self.player_names[player]
		p = self.players[pid]
		pack = p.pack_queue.peek()
		for i in range(0, len(pack)):
			if cardId == pack[i]['cardId']:
				p.card_pool.append(card)
				#pops off the current pack and adds to the next queue
				pack = p.pack_queue.get()
				del pack[i]
				if not pack:
					if p.packs < NUM_PACKS;
						pack = pm.create_pack()
						p.packs += 1
					else:
						p.done = True
				players[pid + 1].pack_queue.put(pack)
				return True

		print "card is not in pack"
		return False

	def get_pack(self, player):
		pid = self.player_names[player]
		p = self.players[pid]
		if p.pack_queue.empty():
			return False
		else:
			return p.pack_queue.peek()

	def is_finished(self):
		return all(map(lambda x: x.done, self.players))


class Player:

	def __init__(self, name):
		self.name = name
		self.num_packs = 0
		self.pack_queue = Queue()
		self.card_pool = []
		self.done = False






