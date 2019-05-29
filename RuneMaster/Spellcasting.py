import discord
import json

import APIRequest

def get_spellcasting_info(class_name):
	data = APIRequest.get_json(APIRequest.base_URL + "spellcasting/")
	if "results" in data:
		embed = discord.Embed(color = 0xff0000)
		description = "Hey this command is still a WIP, so come back later, okay?"
		embed.add_field(name = "Command Failed", value = description, inline = False)
		return embed

		#for class_item in data["results"]:
		#	if class_name == list_item["name"]:
		#		data = APIRequest.get_json(list_item["url"])

	else:
		embed = discord.Embed(color = 0xff0000)
		description = "There was an error in attempting to retrieve the data. Please try again later."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed
