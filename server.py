from flask import Flask, session, redirect, url_for, escape, request, render_template

# Forms stuff
from flask.ext.wtf import form 
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from custom_forms import *

# needs redis to run
from juggernaut import Juggernaut
from push_notifications import *

# social stuff
from flask.ext.social import Social
from flask.ext.security import Security

#db stuff
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension

# random stuff
import time

from config import *

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': FB_CONSUMER_KEY,
    'consumer_secret': FB_APP_SECRET
}


#app.config['MONGODB_SETTINGS'] = {
#    'db': 'hearthstone',
#    'username':'webapp',
#    'password':'pwd123'
#}

app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']


db = MongoEngine(app)

# ... define user and role models ...

class Connection(db.Document):
    id = db.IntField()
    user_id = db.IntField()
    provider_id = db.StringField()
    provider_user_id = db.StringField()
    access_token = db.StringField()
    secret = db.StringField()
    display_name = db.StringField()
    profile_url = db.StringField()
    image_url = db.StringField()
    rank = db.IntField()

Security(app, MongoEngineSessionInterface(db))
Social(app, db)

@app.route('/home')
@app.route('/')
def home():
	return render_template('test.html', login_form=LoginForm())


#Server Functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	print "username", form.username.data
	print form
	if form.validate():
		username = form.username.data
		flash('Login requested with username %s' % username)
		if not users.get(username, None):
			session['username'] = username
			session['logged_in'] = True
			users[username] = User(username)
			return 'success'
		else:
			return 'username taken'
	else:
		return 'Form did not validate'

@app.route('/logout')
def logout():
	del users[ session['username'] ]
	session.pop('username',None)
	session["logged_in"] = False
	session.pop('lobby', None)
	return 'logged out'

@app.route('/create', methods = ['GET', 'POST'])
def create_lobby():
	form = LobbyForm()
	if not form.validate_on_submit():
		return 'fill in the fields please'
	if not session.get('username', None):
		return 'you are not logged in'
	if not lobbies.get(form.name.data, None):
		lobbies[form.name.data] = Lobby(form.name.data, form.password.data, session['username'])
		session["lobby"] = form.name.data
		session["owner"] = True
		return 'lobby created'
	else:
		return 'lobby name taken'

@app.route('/join', methods=['GET', 'POST'])
def join_lobby():
	form = LobbyForm()
	if not form.validate_on_submit():
		return 'Lobby name required'
	if not session['username']:
		return 'log in first'
	lobby = lobbies.get(form.name.data, None)
	if not lobby:
		return 'lobby does not exist'
	if lobby.join_lobby(session['username'], form.password.data):
		session["lobby"] = form.name.data
		session["owner"] = ( lobby.owner == session["username"] )
		return 'joined lobby'
	else:
		return 'incorrect password'

@app.route('/lobbies')
def get_lobbies():
	return filter(lambda x: x[draft] == None, lobbies)

@app.route('/start')
def start_draft():
	lobby = lobbies[session['lobby']]
	if session['username'] == lobby.owner:
		lobby.start_draft()
	else:
		return 'you are not the owner of this lobby'

@app.route('/pick/<lobby>/<username>/<card>', methods=['POST'])
def pick_card(lobby, username, card):
	pass

@app.route('/pack')
def get_pack():
	lobby = lobbies[ session['lobby'] ]
	lobby.draft

@app.route('/chat')
def send_chat():
	form = ChatForm()
	if form.validate_on_submit():
		message = form.message.data

		lobby = lobbies.get(session['lobby'], None)
		if not lobby:
			print 'no such lobby'
			return

		lobby.message(session['username'], message)

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
			self.update_lobby()
			return True
		else:
			return False

	def leave_lobby(self, username):
		self.players = [x for x in self.players if x != username]
		self.update_lobby()

	def update_lobby(self):
		for user in self.players:
			users[user].message( make_lobby_notification(self.players) )

	def message(self, sender, text):
		self.messages.append(text)
		for user in self.players:
			users[user].message( make_chat_notification(sender, text) )


	def start_draft(self):
		self.draft = Draft(players)

	def save_draft(self):
		pass
		draft_save = {}
		draft_save['name'] = self.name

		draft_save['pools'] = {}
		for player in self.draft.players:
			draft_save['pools'][player.name] = player.card_pool
			# TO DO: save the draft in each players' draft history.

		draft_save['time'] = time.time()

# username -> user objects
users = {}

class User:

	def __init__(self, name):
		self.name = name
		self.channel = name


	def message(self, message):
		jug.publish(self.channel, message)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
	
	lobbies = []
	jug = Juggernaut()
