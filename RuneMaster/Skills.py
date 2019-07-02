import discord
import json

import APIRequest

def get_skill(skill_name):
	data = APIRequest.get_json(APIRequest.base_URL + "features/")
	skill_name = reformat_name(skill_name)
	if "results" in data:
		for list_item in data["results"]:
			if skill_name == list_item["name"]:
				data = APIRequest.get_json(list_item["url"])
				indent = "\u200b\t\u200b\t\u200b\t\u200b\t\u200b\t"
				
				description = ""
				for i, item in enumerate(data["desc"]):
					if i > 0:
						description += indent
					description += item + "\n"
				embed = discord.Embed(color = 0x0080ff, title = skill_name, description = description)
				return embed

		embed = discord.Embed(color = 0xff0000)
		description = "Unable to get data for `" + skill_name + "`, please enter a valid skill name."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed
	else:
		embed = discord.Embed(color = 0xff0000)
		description = "There was an error in attempting to retrieve the data. Please try again later."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed

# Takes the skill name and converts it into an API-compatible format
def reformat_name(name):
	split_string = name.split(" ")
	final_string = ""

	for i, item in enumerate(split_string):
		final_string += item.lower().capitalize()
		if i < len(split_string) - 1:
			final_string += " "

	# Catch statements for specific formatting
	if " Of The " in final_string:
		final_string = final_string.strip().replace(" Of The ", " of the ")
	elif final_string == "Destroy Undead": # 91
		final_string = "Destroy Undead (CR 2 or below)"
	elif "Circle of the Land" in final_string: # 104 to 111
		final_string = final_string.strip()
		if "Land " in final_string:
			final_string = final_string.replace("Land ", "Land: ")
	elif final_string == "Lands Stride": # 118
		final_string = "Land's Stride"
	elif "Natures" in final_string: # 123, 125
		final_string = final_string.replace("Natures", "Nature's")
	elif "Fighting Style" in final_string: # 132, 137
		final_string = final_string.strip().replace("Style ", "Style: ")

	return final_string