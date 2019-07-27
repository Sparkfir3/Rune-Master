import discord
import json

import APIRequest
import Mode

def get_enchantment(enchant_string):
	if Mode.Mode.current == "homebrew":
		data = APIRequest.rc_data.rc_enchants
		for i, item in enumerate(data):
			if APIRequest.rc_data.rc_enchants[i]["name"] == enchant_string:
				indent = "\u200b\t\u200b\t\u200b\t\u200b\t\u200b\t"
				description = "*{}, {}*\n\n".format(item["rarity"], format_level(item["level"]))

				if "armor-desc" in item:
					description += "***Armor:***  "
					for j, desc in enumerate(item["armor-desc"]):
						if j > 0:
							description += indent
						description += desc + "\n"
				if "melee-desc" in item:
					if "armor-desc" in item:
						description += "\n"
					if "ranged-desc" in item:
						description += "***Melee and Ranged Weapons:***  "
					else:
						description += "***Melee Weapons:***  "
					for j, desc in enumerate(item["melee-desc"]):
						if j > 0:
							description += indent
						description += desc + "\n"
				elif "ranged-desc" in item:
					description += "***Ranged Weapons:***  "
					for j, desc in enumerate(item["ranged-desc"]):
						if j > 0:
							description += indent
						description += desc + "\n"
				elif "shield-desc" in item:
					description += "***Shields:***  "
					for j, desc in enumerate(item["shield-desc"]):
						if j > 0:
							description += indent
						description += desc + "\n"

				description += "\n" + "**Source:** " + get_page_num(item["page"])

				embed = discord.Embed(color = 0x0080ff, title = enchant_string, description = description)
				return embed

		if enchant_string == "":
			enchant_string = " "
		description = "Unable to get data for `{}`, please enter a valid enchantment name.".format(enchant_string)
		embed = discord.Embed(color = 0xff0000, title = "Attempting to Get Info", description = description)
		return embed

	else:
		description = "Bot mode must be set to `homebrew` to use this command!"
		description += "\nUse the `$mode` command to set bet mode."
		embed = discord.Embed(color=0xff0000, title = "Cannot Use Command", description = description)
		return embed

def format_level(level):
	if level == 1:
		return "1st level"
	elif level == 2:
		return "2nd level"
	elif level == 3:
		return "3rd level"
	else:
		return str(level) + "th level"

def get_page_num(page):
	split_string = page.split(" ")
	if split_string[0] == "rc":
		try:
			return "Runic Cataclysm, page " + split_string[1]
		except:
			return "Runic Cataclysm"
	else:
		return page