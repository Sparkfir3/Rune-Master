import discord
import json

import APIRequest

def get_item(item_name):
	data = APIRequest.get_json(APIRequest.base_URL + "equipment/")
	item_name = reformat_name(item_name)
	if "results" in data:
		for list_item in data["results"]:
			if item_name == list_item["name"]:
				data = APIRequest.get_json(list_item["url"])
				description = ""
				if data["equipment_category"] == "Weapon":
					description = weapon_info(data)
				elif data["equipment_category"] == "Armor":
					description = armor_info(data)
					if data["armor_category"] != "Shield":
						item_name += " Armor"
				else:
					break
				embed = discord.Embed(color = 0x0080ff, title = item_name, description = description)
				return embed

		embed = discord.Embed(color = 0xff0000)
		description = "Unable to get data for `" + item_name + "`, please enter a valid item name."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed
	else:
		embed = discord.Embed(color = 0xff0000)
		description = "There was an error in attempting to retrieve the data. Please try again later."
		embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
		return embed

# Takes the item name and converts it into an API-compatible format
def reformat_name(name):
	split_string = name.split(" ")
	final_string = ""
	for i, item in enumerate(split_string):
		if i == 0:
			final_string += item.lower().capitalize()
		else:
			if item == "Leather" or item == "Shirt" or item == "Mail":
				final_string += item.lower().capitalize()
			else:
				final_string += item.lower()
		if i < len(split_string) - 1:
			final_string += " "
	final_string = final_string.replace(" armor", "")
	return final_string

# Formats cost of items
def format_cost(cost):
	total = str(cost["quantity"]) + " " + cost["unit"]
	return total

# Formats damage of weapons
def format_damage(damage):
	total = str(damage["dice_count"]) + "d" + str(damage["dice_value"]) + " " + damage["damage_type"]["name"].lower()
	return total

# Formats properties of weapons
def format_properties(properties):
	total = ""
	for i, prop in enumerate(properties):
		if i == 0:
			total += prop["name"]
		else:
			total += ", " + prop["name"].lower()
	if total == "":
		total = "None"
	return total

# Gets and formats description for weapons
def weapon_info(data):
	description = "*" + data["category_range"] + " Weapon*\n\n"
	description += "**Cost:** " + format_cost(data["cost"]) + "\n"
	description += "**Damage:** " + format_damage(data["damage"]) + "\n"
	description += "**Weight:** " + str(data["weight"]) + " lb.\n"
	description += "**Properties:** " + format_properties(data["properties"])
	return description

# Formats armor class of armor
def format_armor_class(ac):
	total = str(ac["base"])
	if ac["dex_bonus"] == True:
		total += " + Dex modifier"
		if ac["max_bonus"] == 2:
			total += " (max 2)"
	return total

# Gets and formats strength minimum of armor
def get_armor_str_min(min):
	total = ""
	if min != 0:
		total = "**Str Min:** " + str(min) + "\n"
	return total

# Gets and formats stealth disadvantage of armor
def get_stealth_disadv(value):
	total = ""
	if value == True:
		total = "*Gives Stealth Disadvantage*"
	return total

# Gets and formats description for armor
def armor_info(data):
	description = ""
	if data["armor_category"] == "Shield":
		description += "**Cost:** " + format_cost(data["cost"]) + "\n"
		description += "**Armor Class:** " + "+2\n"
		description += "**Weight:** " + str(data["weight"]) + "lb.\n"
	else:
		description += "*" + data["armor_category"] + " Armor*\n\n"
		description += "**Cost:** " + format_cost(data["cost"]) + "\n"
		description += "**Armor Class:** " + format_armor_class(data["armor_class"]) + "\n"
		description += "**Weight:** " + str(data["weight"]) + "lb.\n"
		description += get_armor_str_min(data["str_minimum"])
		description += get_stealth_disadv(data["stealth_disadvantage"])
	return description
