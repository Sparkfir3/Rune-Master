import discord
import json

import APIRequest
import Mode

def check_rc_spells(spell_name):
	if Mode.Mode.current == "homebrew" or Mode.Mode.current == "limited":
		for i, item in enumerate(APIRequest.rc_data.rc_spells):
			if APIRequest.rc_data.rc_spells[i]["name"] == spell_name:
				return APIRequest.rc_data.rc_spells[i]
	return None

def get_spell(spell_name):
	data = APIRequest.get_json(APIRequest.base_URL + "spells/?name=" + reformat_name(spell_name))
	if data["count"] == 0:
		data = check_rc_spells(spell_name)
		if data == None:
			embed = discord.Embed(color=0xff0000)
			description = "Unable to get data for `" + spell_name + "`, please enter a valid spell name."
			description += "\n\n*Note: not all spells are publicly available through the D&D 5e API."
			description += "\nIf your spell\'s info cannot be obtained here, please check the spell\'s source material.*"
			embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
			return embed
	else:
		data = APIRequest.get_json(data["results"][0]["url"])

	#embed = discord.Embed(color=0x0080ff)
	indent = "\u200b\t\u200b\t\u200b\t\u200b\t\u200b\t"

	# Get level and school
	main_info = "*" + get_level_and_school(data["level"], data["school"]["name"])
	if data["ritual"] == "yes":
		main_info += " (ritual)"
	main_info += "*"
	# Get basic information and stats
	main_info += "\n\n" + "**Casting Time:** " + data["casting_time"] + "\n"
	main_info += "**Range:** " + data["range"] + "\n"
	main_info += "**Components:** "
	for i, item in enumerate(data["components"]):
		main_info += item
		if i < len(data["components"]) - 1:
			main_info += ", "
	if "material" in data:
		main_info += " (" + data["material"].lower().replace(".", "") + ")"
	main_info += "\n" + "**Duration:** "
	if data["concentration"] == "yes":
		main_info += "Concentration, " + data["duration"].lower() + "\n"
	else:
		main_info += data["duration"] + "\n"
	# Fix apostraphes
	main_info = main_info.replace("â€™", "\'")

	# Get main description
	description = "\n"
	for i, item in enumerate(data["desc"]):
		if i > 0:
			description += indent
		description += item + "\n"
	if "higher_level" in data:
		description += indent + "***At Higher Levels.*** " + data["higher_level"][0] + "\n"
	# Fix apostraphes
	description = description.replace("â€™", "\'")

	# Get source book and page number
	source = "\n" + "**Source:** " + get_page_num(data["page"])

	# Check message length
	if len(main_info) + len(description) + len(source) > 2048:
		description = "Description is too long, please check source material for full information!"

	# Return
	embed = discord.Embed(color = 0x0080ff, title = reformat_name(spell_name).replace("+", " "), description = main_info + description + source)
	return embed

# Takes the spell name and converts it into an API-compatible format
def reformat_name(name):
	split_string = name.split(" ")
	final_string = ""

	for i, item in enumerate(split_string):
		if item.lower() == "of":
			final_string += "of"
		else:
			final_string += item.lower().capitalize()
		if i < len(split_string) - 1:
			final_string += "+"
	return final_string

# Returns the level and school of the spell as a properly formatted string
def get_level_and_school(level, school):
	if level == 0:
		return school + " cantrip"
	elif level == 1:
		return "1st-level " + school.lower()
	elif level == 2:
		return "2nd-level " + school.lower()
	elif level == 3:
		return "3rd-level " + school.lower()
	else:
		return str(level) + "th-level " + school.lower()

# Returns source book and page number as a properly formatted string
def get_page_num(page):
	split_string = page.split(" ")
	if split_string[0] == "phb":
		return "Player's Handbook, page " + split_string[1]
	elif split_string[0] == "rc":
		try:
			return "Runic Cataclysm, page " + split_string[1]
		except:
			return "Runic Cataclysm"
	else:
		return page