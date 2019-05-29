import discord
import json

import APIRequest

def get_condition(cond_name):
	data = APIRequest.get_json(APIRequest.base_URL + "conditions/")
	cond_name = catch_name(cond_name)
	if "results" in data:
		for list_item in data["results"]:
			if cond_name == list_item["name"]:
				data = APIRequest.get_json(list_item["url"])
				description = ""
				for desc in data["desc"]:
					description += desc + "\n"
				embed = discord.Embed(color = 0x0080ff, title = cond_name, description = description)
				return embed

		embed = discord.Embed(color = 0xff0000)
		description = "Unable to get data for `" + cond_name + "`, please enter a valid condition name."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed
	else:
		embed = discord.Embed(color = 0xff0000)
		description = "There was an error in attempting to retrieve the data. Please try again later."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed

# Reformats name if it was inputted slightly off
def catch_name(name):
	if name == "Blind" or name == "Charm" or name == "Deafen" or name == "Frighten" or name == "Poison" or name == "Restrain":
		name += "ed"
	elif name == "Grapple" or name == "Incapacitate" or name == "Paralyze":
		name += "d"
	elif name == "Deaf":
		name += "ened"
	elif name == "Stun":
		name += "ned"
	return name