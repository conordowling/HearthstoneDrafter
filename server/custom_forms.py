from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired])

class ChatForm(Form):
    message = StringField('message', validators=[DataRequired()])

class LobbyForm(Form):
	name = StringField('name', validators=[DataRequired()])
	password = StringField('password')

class DraftSettingsForm(Form):
	pass
	