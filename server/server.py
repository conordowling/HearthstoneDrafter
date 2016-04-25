from flask import Flask, session, redirect, url_for, escape, request, render_template

# Forms stuff
from flask.ext.wtf import form 
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
import custom_forms

# needs redis to run
from juggernaut import Juggernaut

app = Flask(__name__)

app.secret_key = 'yolo'

@app.route('/home')
@app.route('/')
def home():
	return render_template('test.html')



#Server Functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		flash('Login requested with username %s' % username)
		if not users.get(username, None):
			session['username'] = username
			users[username] = User(username)
			return 'success'
		else:
			return 'username taken'
	else:
		return 'Please enter a username'

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

@app.route('/start')
def start_draft():
	lobby = lobbies[session['lobby']]
	if session['username'] == lobby.owner:
		lobby.start_draft()

	else:
		return 'you are not the owner of this lobby'

@app.route('/pick/<lobby>/<username>/<card>', methods=['POST'])
def pick_card():
	pass

@app.route('/chat')
def send_chat():
	form = ChatForm()
	if form.validate_on_submit():
		message = form.message.data

		lobby = lobbies.get(session['lobby'], None)
		if not lobby:
			print 'no such lobby'
			return

		for name in lobby.players:
			user = users[name]
			user.message(session['username'], message)

	else:
		return 'no text'


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
			user.message(sender + ": " + text)

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
