# TODO - comment everything
# TODO - finish show_known_places

import Room
from GameMap import GameMap


class Game(object):
	def __init__(self):
		self.last_room = None
		self.map = GameMap()
		self.inventory = []
		self.move_count = 1
		self.current_room = self.map.rooms[0][0]
		self.current_room.user_visited = True
	# end def __init__

	def inspect(self):
		text = self.map.inspect()
		text += "Inventory: %s" % self.inventory
	# end def inspect

	def describe_scene(self):
		# describe the room
		self.current_room.describe()
    
		# describe player's inventory
		print ("Your Inventory: ")
		if len(self.inventory) > 0:
			for item in range(0, len(self.inventory)):
				print (self.inventory[item])
			# end for
		else:
			print ("NONE")
		# end if

		print ("")
	# end def describe_scene

	def get_next_move(self):
		header = "| Move: %d |" % self.move_count
		print ("-" * len(header))
		print(header)
		print ("-" * len(header))
	
		self.describe_scene()

		self.move_count += 1
		next_move = None
		while not next_move:
			print("")
			print("What do you want to do? ...")
			choices = []
			if self.current_room:
				for door in self.current_room.doors:
					choices.append("Move %s" % door)
				# end for

				for item in self.current_room.items: 
					if (item == "Instructions"):
						choices.append("Get Instructions")
					elif (item == "Bear"):
						if not self.current_room.bear_is_sleeping:
							choices.append("Make Noise")
							choices.append("Fight Bear")
						else:
							pass # Sure?
						# end if
					elif (item == "Honey"):
						choices.append("Get Honey")
					elif (item == "Treasure!"):
						choices.append("Get Treasure!")
					else:
						raise Exception("Room contains an unknown item: %s. Should not have been possible to get here." % item)
					# end if
				# end for
			else:
				raise Exception("Room[%d][%d] is nil. Should not have been possible to get here." % (x_position, y_position))
			# end if

			for item in self.inventory:
				if (item == "Instructions"):
					choices.append("Read Instructions")
				elif (item == "Honey"):
					choices.append("Drop Honey")
					choices.append("Eat Honey")
				else:
					raise Exception("Unknown inventory: %s. Should not have been possible to get here." % item)
				# end if
			# end for
	
			choices.append("Show Places I've Been")
			choices.append("About this Game")
			choices.append("Quit")

			for choice in range(0, len(choices)):
				print("%d) %s" % (choice+1, choices[choice]))
			# end for

			print (">>> Type the number of your choice followed by <Enter> or <Return>: ")
			choice = int(input())
			print ("")
			if (choice > 0 and choice <= len(choices)):
				next_move = choices[choice-1]
			else:
				print("Sorry, I don't understand that choice. Please try again.")
			# end if
		# end while
		
		return next_move

	# end def next_move

	def do_pause(self):
		print ("\n<PRESS ANY KEY TO CONTINUE> ...")
		input()
		print ("\n\n")
	# end def do_pause

	def do_move(self, move):
		if (move == "Move North" or move == "Move South" or move == "Move East" or move == "Move West"):
			if (self.current_room.door_blocked_by_bear and self.current_room.door_blocked_by_bear in move):
				print("The bear is blocking that door!")
				print("You need to distract the bear or go in a different direction.")
			else:
				self.last_room = self.current_room
				if (move == "Move North"):
					self.current_room = self.map.rooms[self.current_room.x_location-1][self.current_room.y_location]
				elif (move == "Move South"):
					self.current_room = self.map.rooms[self.current_room.x_location+1][self.current_room.y_location]
				elif (move == "Move East"):
					self.current_room = self.map.rooms[self.current_room.x_location][self.current_room.y_location+1]
				elif (move == "Move West"):
					self.current_room = self.map.rooms[self.current_room.x_location][self.current_room.y_location-1]
				# end if
				self.current_room.user_visited = True
				self.current_room.prepare_room()
				print("Ok, you have moved in that direction.")
			# end if
			self.do_pause()
		elif (move == "Get Instructions"):
			self.inventory.append(self.current_room.remove_item("Instructions"))
			self.do_pause()
		elif (move == "Read Instructions"):
			print("The instructions are very simple:")
			print("  F I N D")
			print("  T H E")
			print("  T R E A S U R E")
			self.do_pause()
		elif (move == "Make Noise"):
			if (self.current_room.made_noise_once):
				print("You disturbed the bear again.")
				print("The bear got angry and ate your arms and legs.")
				print("You are dead. Game Over.")
				return False
			else:
				print("Wow! You're really loud.")
				print("But the bear didn't like that.")
				self.do_pause()
				self.current_room.made_noise_once = True
			# end if
		elif (move == "Fight Bear"):
			print("That wasn't very smart! The bear won.")
			print("You are dead. Game Over.")
			return False
		elif (move == "Get Honey"):
			self.inventory.append(self.current_room.remove_item("Honey"))
			print("Ok, you now have the honey.")
			self.do_pause()
		elif (move == "Drop Honey"):
			self.inventory.remove("Honey")
			print("Ok, you have dropped the honey in the room.")
			if ("Bear" in self.current_room.items):
				self.current_room.bear_is_sleeping = True
				self.current_room.door_blocked_by_bear = None
				print("I've got some good news and some bad news:")
				print("The good news is that the bear ate all the honey,")
				print("fell asleep, and is no longer guarding the door.")
				print("The bad news is that you have no more honey :(")
				self.do_pause()
			else:
				self.current_room.drop_item("Honey")
			# end if
		elif (move == "Eat Honey"):
			self.inventory.remove("Honey")
			print("That was yummy!")
			self.do_pause()
		elif (move == "Get Treasure!"):
			print("You got the treasure! YOU WIN!")
			return False
		elif (move == "Show Places I've Been"):
			self.map.show_known_map()
			self.do_pause()
		elif (move == "About this Game"):
			print("TreasureGame, written by Steve Frechette 2015")
			self.do_pause()
		elif (move == "Quit"):
			print("Sorry to see you go. Come again soon!")
			return False
		else:
			print("I don't understand that command.")
			self.do_pause()
		# end if

		return True

	# end def do_move

	def play(self):
		next_move = self.get_next_move()
		return self.do_move(next_move)
	# end def play

# end class
