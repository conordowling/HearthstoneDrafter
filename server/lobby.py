class Lobby:

	def __init__(self, name, password, owner):
		self.name = name
		self.password= password
		self.owner = owner
		self.players = [owner]

	#
	def join_lobby(self, username, password):
		if password == self.password:
			self.players.append(username)
			update_lobby()
			return True
		else:
			return False

	def leave_lobby(self, username):
		self.players = [x for x in self.players if x != username]
		update_lobby()

	def update_lobby(self):
