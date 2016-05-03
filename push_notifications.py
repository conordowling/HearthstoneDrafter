def make_lobby_notification(players):
	return {
		"type":"lobby",
		"data":players
	}

def make_chat_notification(sender, message):
	return {
		"type":"chat",
		"data":{
			"sender":sender,
			"message":message
		}
	}

def make_settings_notification(settings):
	return {
		"type":"settings",
		"data":settings
	}

def make_pack_notification(pack):
	return {
		"type":"pack",
		"data":pack
	}