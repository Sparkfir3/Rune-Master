import discord
import json

import APIRequest

def get_monster_stats(monster_name):
	data = APIRequest.get_json(APIRequest.base_URL + "monsters/")
	if "results" in data:
		for list_item in data["results"]:
			if monster_name == list_item["name"]:
				data = APIRequest.get_json(list_item["url"])

				description = "*" + data["size"] + " " + data["type"] + ", " + data["alignment"] + "*\n\n"
				description += "**Armor Class** " + str(data["armor_class"]) + "\n"
				description += "**Hit Points** " + str(data["hit_points"]) + " (" + data["hit_dice"] + ")\n"
				description += "**Speed** " + str(data["speed"]) + "\n\n"
				
				description += "**STR** " + reformat_stat(data["strength"]) + "\n"
				description += "**DEX** " + reformat_stat(data["dexterity"]) + "\n"
				description += "**CON** " + reformat_stat(data["constitution"]) + "\n"
				description += "**INT** " + reformat_stat(data["intelligence"]) + "\n"
				description += "**WIS** " + reformat_stat(data["wisdom"]) + "\n"
				description += "**CHA** " + reformat_stat(data["charisma"]) + "\n\n"

				description += get_dam_vuln(data["damage_vulnerabilities"])
				description += get_dam_res(data["damage_resistances"])
				description += get_dam_immune(data["damage_immunities"])
				description += get_cond_immune(data["condition_immunities"])
				description += "**Senses** " + data["senses"] + "\n"
				description += get_languages(data["languages"])
				description += get_cr(data["challenge_rating"])

				embed = discord.Embed(color = 0x0080ff, title = monster_name + " - Stats", description = description)
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

# Reformats the number string for stats
def reformat_stat(stat):
	return str(stat) + " (" + get_bonus(stat) + ")"

# Converts a stat number to its corresponding bonus
def get_bonus(stat):
	if stat >= 20:
		return "+5"
	elif stat >= 18:
		return "+4"
	elif stat >= 16:
		return "+3"
	elif stat >= 14:
		return "+2"
	elif stat >= 12:
		return "+1"
	elif stat >= 10:
		return "+0"
	elif stat >= 8:
		return "-1"
	elif stat >= 6:
		return "-2"
	elif stat >= 4:
		return "-3"
	elif stat >= 2:
		return "-4"
	else:
		return "-5"

# Gets damage vulnerabilites of the monster and returns as a string
def get_dam_vuln(vuln):
	if vuln != "":
		return "**Damage Vulnerabilities** " + vuln + "\n"
	else:
		return vuln

# Gets damage resistances of the monster and returns as a string
def get_dam_res(res):
	if res != "":
		return "**Damage Resistances** " + res + "\n"
	else:
		return res

# Gets damage immunities of the monster and returns as a string
def get_dam_immune(immune):
	if immune != "":
		return "**Damage Immunities** " + immune + "\n"
	else:
		return immune

# Gets condition immunities of the monster and returns as a string
def get_cond_immune(immune):
	if immune != "":
		return "**Condition Immunities** " + immune + "\n"
	else:
		return immune

# Gets languages of the monster and returns as a string
def get_languages(lang):
	if lang != "":
		return "**Languages** " + lang + "\n"
	else:
		return "**Languages** –\n"

# Gets challenge rating of the monster, formats it, and returns as a string
def get_cr(cr):
	challenge = "**Challenge** "
	if cr == 0.125:
		challenge += "1/8 (25 XP)"
	elif cr == 0.25:
		challenge += "1/4 (50 XP)"
	elif cr == 0.5:
		challenge += "1/2 (100 XP)"
	else:
		challenge += str(cr) + " (" + str(200 * cr) + " XP)"
	return challenge + "\n"

# Gets monster special abilities
def get_abilities(monster_name):
	data = APIRequest.get_json(APIRequest.base_URL + "monsters/")
	if "results" in data:
		for list_item in data["results"]:
			if monster_name == list_item["name"]:
				data = APIRequest.get_json(list_item["url"])

				description = ""
				for ability in data["special_abilities"]:
					description += "***{}.*** {}\n\n".format(ability["name"], ability["desc"])
				if description == "":
					description = "This monster has no special abilities."

				embed = discord.Embed(color = 0x0080ff, title = monster_name + " - Abilities", description = description)
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

# Gets monster actions
def get_actions(monster_name):
	data = APIRequest.get_json(APIRequest.base_URL + "monsters/")
	if "results" in data:
		for list_item in data["results"]:
			if monster_name == list_item["name"]:
				data = APIRequest.get_json(list_item["url"])

				description = ""
				for action in data["actions"]:
					description += "***{}.*** {}\n\n".format(action["name"], action["desc"])
				embed = discord.Embed(color = 0x0080ff, title = monster_name + " - Actions", description = description)

				if "legendary_actions" in data:
					description = ""
					for leg_action in data["legendary_actions"]:
						description += "**{}.** {}\n\n".format(leg_action["name"], leg_action["desc"])
					embed.add_field(name = monster_name + " - Legendary Actions", value = description, inline = False)

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