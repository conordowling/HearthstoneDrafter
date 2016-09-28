from server import db

class User(db.Document):
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

class DraftRecord(db.Document):
	name = db.StringField()
	time = db.IntField()
	settings = db.EmbeddedDocumentField('Settings')
	players = db.ListField(db.EmbeddedDocumentField('PlayerDraft'))


class Settings(db.Document):
	pass

class PlayerDraft(db.Document):
	user = db.StringField()
	card_pool = db.ListField()

