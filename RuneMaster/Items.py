import discord
import json

import APIRequest
import Mode

indent = "\u200b\t\u200b\t\u200b\t\u200b\t\u200b\t"

def check_rc_equipment(item_name):
	if Mode.Mode.current == "homebrew":
		for item in APIRequest.rc_data.rc_equipment:
			if item["name"] == item_name:
				return item
	return None

def check_rc_items(item_name):
	if Mode.Mode.current == "homebrew":
		for item in APIRequest.rc_data.rc_items:
			if item["name"] == item_name:
				return item
	return None

# Checks to see if the item is in the database, and retrieves it if so
def get_item(item_name):
	item_name = reformat_name(item_name)

	data = check_rc_equipment(item_name)
	if data != None:
		return collect_data(data, item_name)
	else:
		data = check_rc_items(item_name)
		if data != None:
			return etheric_item(data, item_name)

		data = APIRequest.get_json(APIRequest.base_URL + "equipment/")
		if "results" in data:
			for list_item in data["results"]:
				if item_name == list_item["name"]:
					data = APIRequest.get_json(list_item["url"])
					return collect_data(data, item_name)
				
	# Unable to get data (item doesn't exist in database or not supported)
	embed = discord.Embed(color = 0xff0000)
	description = "Unable to get data for `" + item_name + "`, please enter a valid item name."
	embed.add_field(name = "Attempting to Get Info", value = description, inline = False)
	return embed

# Collects the data for the item
def collect_data(data, item_name):
	description = ""
	if data["equipment_category"] == "Weapon":
		description = weapon_info(data)
	elif data["equipment_category"] == "Armor":
		description = armor_info(data)
		if data["armor_category"] != "Shield":
			item_name += " Armor"
	elif data["equipment_category"] == "Adventuring Gear":
		description = adventuring_gear_info(data)

	embed = discord.Embed(color = 0x0080ff, title = item_name, description = description)
	return embed

# Takes the item name and converts it into an API-compatible format
def reformat_name(name):
	split_string = name.split(" ")
	final_string = ""
	for i, item in enumerate(split_string):
		item = item.lower()
		if i == 0:
			final_string += item.capitalize()
		else:
			if item == "light" or item == "heavy" or item == "hand" or item == "pick":
				final_string += item
			else:
				final_string += item.capitalize()

		if i < len(split_string) - 1:
			final_string += " "
	final_string = final_string.replace(" Armor", "")
	return final_string

# Formats cost of items
def format_cost(cost):
	if cost["unit"] == "n/a":
		return "Unpurchasable"
	else:
		total = str(cost["quantity"]) + " " + cost["unit"]
	return total

# ---------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------

# Returns formated source book and page number
def get_page_num(page):
	split_string = page.split(" ")
	if split_string[0] == "rc":
		try:
			return "Runic Cataclysm, page {}".format(split_string[1])
		except:
			return "Runic Cataclysm"
	return page

def adventuring_gear_info(data):
	description = "*{} ({})*\n\n".format(data["equipment_category"], data["gear_category"])
	description += "**Cost:** {}\n".format(format_cost(data["cost"]))
	description += "**Weight:** {} lb.\n".format(str(data["weight"]))
	if "desc" in data:
		description += "\n"
		for i, item in enumerate(data["desc"]):
			description += "{}{}\n".format(indent if i > 0 else "", item)
	if "source" in data:
		description += "\n**Source:** {}".format(get_page_num(data["source"]))
	return description

# ---------------------------------------------------------------------------------------------------

# Gets and formats item type
def get_etheric_item_type(type):
	if type == "Wondrous":
		return "Wondrous item"
	else:
		return type

def etheric_item(data, item_name):
	description = "*{}, {}*\n\n".format(get_etheric_item_type(data["type"]), data["rarity"])
	for i, item in enumerate(data["desc"]):
		description += "{}{}\n".format(indent if i > 0 else "", item)
	description += "\n**Source:** {}".format(get_page_num(data["source"]))

	embed = discord.Embed(color = 0x0080ff, title = item_name, description = description)
	return embed