import discord

# Object that stores the list
class Init_List(object):
	list = []

# Adds initiative with name "name" and value "value" into list
def add_initiative(value, name):
	new_item = (value, name)
	Init_List.list.append(new_item)
	embed = discord.Embed(color=0x0080ff)
	embed.add_field(name = "Success", value = "Added \"{name}\" with initiative {init} to the ordering.\nInitiative list now has {size} items".format(name=name, init=str(value), size=str(len(Init_List.list))), inline = False)
	return embed

# Prints list as sorted embed
def print_list(display_values = True):
	sorted_list = sorted(Init_List.list, key = lambda init: init[0])
	Init_List.list = sorted_list
	if len(sorted_list) > 0:
		sorted_list.reverse()
		embed = discord.Embed(color=0x0080ff)
		description = ""
		value_list = ""
		for item in sorted_list:
			description += item[1] + "\n"
			if display_values:
				value_list += str(item[0]) + "\n"
		embed.add_field(name = "Initiatives", value = description, inline = True)
		if display_values:
			embed.add_field(name = "\u200b", value = value_list, inline = True)
		return embed
	else:
		embed = discord.Embed(color=0xff0000)
		embed.add_field(name = "No Initiatives Available", value = "Please input initiatives using `$initiative <name> <value>` before displaying", inline = False)
		return embed

# Clears the list
def clear():
	count = len(Init_List.list)
	Init_List.list = []
	if count > 0:
		embed = discord.Embed(color=0x0080ff)
		embed.add_field(name = "Success", value = "Cleared initiative list of " + str(count) + " values", inline = False)
		return embed
	else:
		embed = discord.Embed(color=0x0000ff)
		embed.add_field(name = "Success", value = "No values to clear from initiative list", inline = False)
		return embed