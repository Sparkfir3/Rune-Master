import requests
import json

base_URL = "http://dnd5eapi.co/api/"

def get_json(url):
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		return 0
