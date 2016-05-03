from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('username')

class ChatForm(Form):
    message = StringField('message')

class LobbyForm(Form):
	name = StringField('name')
	password = StringField('password')

class DraftSettingsForm(Form):
	pass
	