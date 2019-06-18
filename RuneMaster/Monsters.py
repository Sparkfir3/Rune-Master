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
	new_stat = int((stat / 2) - 5)
	if new_stat >= 0:
		return "+" + str(new_stat)
	else:
		return str(new_stat)

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
	if cr == 0:
		challenge += "0 (0 XP)"
	elif cr == 0.125:
		challenge += "1/8 (25 XP)"
	elif cr == 0.25:
		challenge += "1/4 (50 XP)"
	elif cr == 0.5:
		challenge += "1/2 (100 XP)"
	elif cr == 1:
		challenge += "1 (200 XP)"
	elif cr == 2:
		challenge += "2 (450 XP)"
	elif cr == 3:
		challenge += "3 (700 XP)"
	elif cr == 4:
		challenge += "4 (1,100 XP)"
	elif cr == 5:
		challenge += "5 (1,800 XP)"
	elif cr == 6:
		challenge += "6 (2,300 XP)"
	elif cr == 7:
		challenge += "7 (2,900 XP)"
	elif cr == 8:
		challenge += "8 (3,900 XP)"
	elif cr == 9:
		challenge += "9 (5,000 XP)"
	elif cr == 10:
		challenge += "10 (5,900 XP)"
	elif cr == 11:
		challenge += "11 (7,200 XP)"
	elif cr == 12:
		challenge += "12 (8,400 XP)"
	elif cr == 13:
		challenge += "13 (10,000 XP)"
	elif cr == 14:
		challenge += "14 (11,500 XP)"
	elif cr == 15:
		challenge += "15 (13,000 XP)"
	elif cr == 16:
		challenge += "16 (15,000 XP)"
	elif cr == 17:
		challenge += "17 (18,000 XP)"
	elif cr == 18:
		challenge += "18 (20,000 XP)"
	elif cr == 19:
		challenge += "19 (22,000 XP)"
	elif cr == 20:
		challenge += "20 (25,000 XP)"
	elif cr == 21:
		challenge += "21 (33,000 XP)"
	elif cr == 22:
		challenge += "22 (41,000 XP)"
	elif cr == 23:
		challenge += "23 (50,000 XP)"
	elif cr == 24:
		challenge += "24 (62,000 XP)"
	elif cr == 30:
		challenge += "30 (155,000 XP)"
	else:
		challenge += str(cr)
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