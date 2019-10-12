import requests
import json

base_URL = "http://dnd5eapi.co/api/"

class rc_data(object):
	with open("RC-Database/RC-Spells.json") as myfile:
		data = myfile.read()
	rc_spells = json.loads(data)

	with open("RC-Database/RC-Enchantments.json") as myfile2:
		data2 = myfile2.read()
	rc_enchants = json.loads(data2)

	with open("RC-Database/RC-Monsters.json") as myfile3:
		data3 = myfile3.read()
	rc_monsters = json.loads(data3)

	with open("RC-Database/RC-Equipment.json") as myfile4:
		data4 = myfile4.read()
	rc_equipment = json.loads(data4)

	with open("RC-Database/RC-Items.json") as myfile5:
		data5 = myfile5.read()
	rc_items = json.loads(data5)

def get_json(url):
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		return 0