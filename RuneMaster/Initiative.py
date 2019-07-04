import discord

from random import shuffle

# Object that stores the list
class Init_List(object):
	list = []
	shuffled = False

# Adds initiative with name "name" and value "value" into list
def add_initiative(value, name):
	if len(Init_List.list) == 0:
		Init_List.shuffled = False
	if update_initiative(value, name):
		embed = discord.Embed(color=0x0080ff)
		embed.add_field(name = "Success", value = "Updated \"{name}\" with initiative {init} to the ordering.\nInitiative list now has {size} item(s)".format(name=name, init=str(value), size=str(len(Init_List.list))), inline = False)
		return embed
	else:
		new_item = (value, name)
		Init_List.list.append(new_item)
		embed = discord.Embed(color=0x0080ff)
		embed.add_field(name = "Success", value = "Added \"{name}\" with initiative {init} to the ordering.\nInitiative list now has {size} item(s)".format(name=name, init=str(value), size=str(len(Init_List.list))), inline = False)
		return embed

# Updates iniative value for given "name" if it already exists in the list
def update_initiative(value, name):
	for i in range(len(Init_List.list)):
		if name == Init_List.list[i][1]:
			new_item = (value, name)
			Init_List.list[i] = new_item
			return True
	return False

# Removes value from the list, if it exists
def remove_initiative(name):
	for i in range(len(Init_List.list)):
		if name == Init_List.list[i][1]:
			del Init_List.list[i]
			embed = discord.Embed(color = 0x0080ff, title = "Success", description = "Successfully removed \"{}\" from the initiative list.\nInitiative list now has {} item(s)".format(name, str(len(Init_List.list))))
			return embed
	embed = discord.Embed(color = 0xff0000, title = "Item Does Not Exist", description = "There is no item with name \"{}\" in the initiative list.".format(name))
	return embed

# Prints list as sorted embed
def print_list(display_values = True):

	sorted_list = []
	if not Init_List.shuffled:
		sorted_list = sorted(Init_List.list, key = lambda init: init[0])
		sorted_list = shuffle_list(sorted_list)
		sorted_list.reverse()
		Init_List.list = sorted_list
	else:
		sorted_list = Init_List.list

	if len(sorted_list) > 0:
		embed = discord.Embed(color=0x0080ff)
		description = ""
		for item in sorted_list:
			if display_values:
				description += str(item[0]) + " - "
			description += item[1] + "\n"
		embed.add_field(name = "Initiatives", value = description, inline = False)
		return embed
	else:
		embed = discord.Embed(color=0xff0000)
		embed.add_field(name = "No Initiatives Available", value = "Please input initiatives using `$initiative <name> <value>` before displaying", inline = False)
		return embed

# Randomizes placement of items with the same initiative value
def shuffle_list(old_list):
	new_list = []
	current_value = -10
	sorted_items = []
	for i, old_item in enumerate(old_list):
		if current_value == old_item[0]:
			sorted_items.append(old_item)
			if i == len(old_list) - 1: # Last item in list
				shuffle(sorted_items)
				for new_item in sorted_items:
					new_list.append(new_item)
		else:
			shuffle(sorted_items)
			for new_item in sorted_items:
				new_list.append(new_item)
			if i == len(old_list) - 1: # Last item in list
				new_list.append(old_item)
			else:
				current_value = old_item[0]
				sorted_items = []
				sorted_items.append(old_item)
	Init_List.shuffled = True
	return new_list

# Clears the list
def clear():
	Init_List.shuffled = False
	count = len(Init_List.list)
	Init_List.list = []
	if count > 0:
		embed = discord.Embed(color=0x0080ff)
		embed.add_field(name = "Success", value = "Cleared initiative list of {count} values".format(count=str(count)), inline = False)
		return embed
	else:
		embed = discord.Embed(color=0x0000ff)
		embed.add_field(name = "Success", value = "No values to clear from initiative list", inline = False)
		return embed