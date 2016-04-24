from flask import Flask, session, redirect, url_for, escape, request

# needs redis to run
from juggernaut import Juggernaut

app = Flask(__name__)

app.secret_key = 'yolo'

@app.route('/')
def hello_world():
	return 'Hello World'




#Server Functionality
@app.route('/login/<username>', methods=['GET', 'POST'])
def login(username):
	if not users.get(username, None):
		session['username'] = username
		users[username] = User(username)
		return 'success'
	else:
		return 'username taken'

@app.route('/logout')
def logout():
	del users[ session['username'] ]
	session.pop('username',None)
	return 'logged out'

@app.route('/create/<name>/<password>', methods = ['GET', 'POST'])
def create_lobby(name, password):
	print name, password
	if not session.get('username', None):
		return 'you are not logged in'
	if not lobbies.get(name, None):
		lobbies[name] = Lobby(name, password, session['username'])
		return 'lobby created'
	else:
		return 'lobby name taken'

@app.route('/join/<name>/<password>', methods=['GET', 'POST'])
def join_lobby(name, password):
	if not session['username']:
		return 'log in first'
	lobby = lobbies.get(name, None)
	if not lobby:
		return 'lobby does not exist'
	if lobby.join_lobby(session['username'], password):
		return 'joined lobby'
	else:
		return 'incorrect password'
	pass

@app.route('/lobbies')
def get_lobbies():
	return lobbies

@app.route('/start/<lobby>')
def start_draft():
	pass

@app.route('/pick/<lobby>/<username>/<card>', methods=['POST'])
def pick_card():
	pass

def send_chat(sender, lobby_name, message):
	lobby = lobbies.get(lobby_name, None)
	if not lobby:
		print 'no such lobby'
		return

	for username in lobby.players:
		user = users[username]
		user.message(sender + ": " + message)


# lobby names -> lobby objects
lobbies = {}

class Lobby:

	def __init__(self, name, password, owner):
		self.name = name
		self.password= password
		self.owner = owner
		self.players = [owner]
		self.messages = []
		self.draft = None

	def join_lobby(self, username, password):
		if password == self.password:
			self.players.append(username)
			#update_lobby()
			return True
		else:
			return False

	def leave_lobby(self, username):
		self.players = [x for x in self.players if x != username]
		update_lobby()

	def update_lobby(self):
		pass

	def message(self, sender, text):
		self.messages.append(text)
		for user in self.players:
			user.message(sender ": " + text)

	def start_draft(self):
		self.draft = Draft(players)


# username -> user objects
users = {}

class User:

	def __init__(self, name):
		self.name = name
		self.channel = name


	def message(self, message):
		jug.publish(self.channel, message)

if __name__ == "__main__":
	app.run(debug=True)
	
	lobbies = []
	jug = Juggernaut()
