import discord
import random
import re

# Rolls dice given string message, and returns as an embed
def roll_dice_embed(message):
	dice_string = message.replace(" ", "")
	embed = discord.Embed(color=0x0080ff)
	char_search = re.compile(r'[d\d+-]')

	if char_search.search(dice_string):
		multi_strings = dice_string.split("+")
		total = 0
		sum_string = ""

		for i, item in enumerate(multi_strings):
			# Calculate subtraction
			if "-" in item:
				diff_string = item.split("-")
				for j, diff in enumerate(diff_string):
					roll = eval_dice_roll(diff)
					if j == 0:
						total += dice_roll_total(roll)
					else:
						total -= dice_roll_total(roll)
					if "+" in roll:
						sum_string += "(" + roll + ")"
					else:
						sum_string += roll

					# If there are more rolls to calculate, add " - " to end of string
					if(j < len(diff_string) - 1):
						sum_string += " - "

			# Calculate addition
			else:
				roll = eval_dice_roll(item)
				total += dice_roll_total(roll)
				if "+" in roll:
					sum_string += "(" + roll + ")"
				else:
					sum_string += roll

			# If there are more rolls to calculate, add " + " to end of string
			if(i < len(multi_strings) - 1):
				sum_string += " + "

		embed.add_field(name = "Rolling " + dice_string, value = "`" + str(total) + " = " + sum_string + "`", inline = False)
	else:
		embed = discord.Embed(color = 0xff0000)
		embed.add_field(name = "Attempting to roll " + dice_string, value = "Unable to resolve `" + message.strip() + "`, please enter a valid message", inline = False)
	
	return embed

# Calculate dice rolls from a string, returns as sum of rolls in string
def eval_dice_roll(roll_string):
	if "d" in roll_string:
		numbers = roll_string.split("d")

		# If string contains multiple "d"s, return error
		if len(numbers) != 2:
			return "-1"
		# First string is not empty (specified number of dice rolls)
		elif bool(numbers[0]):
			net_rolls = ""
			for i in range(int(numbers[0])):
				net_rolls += str(random.randint(1, int(numbers[1])))
				if i < int(numbers[0]) - 1:
					net_rolls += " + "
			return net_rolls
		# First string is empty (default to one dice roll)
		else:
			return str(random.randint(1, int(numbers[1])))

	else:
		return roll_string

# Converts sum of rolls from eval_dice_roll into an integer
def dice_roll_total(sum_string):
	total = 0
	# Rolled more than one dice
	if "+" in sum_string:
		indiv_rolls = sum_string.replace(" ", "").split("+")
		for num in indiv_rolls:
			total += int(num)
	# Only rolled one dice
	else:
		total = int(sum_string)
	
	return total

# Gets automatic dice roll for initiative, returns integer
def init_auto_dice_roll(string):
	if "+" in string:
		split = string.split("+")
		return random.randint(1, 20) + int(split[1])
	elif "-" in string:
		split = string.split("-")
		return random.randint(1, 20) - int(split[1])
	else:
		return random.randint(1, 20)