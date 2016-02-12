from random import randint

class Room(object):

	DIRECTIONS = { "N":"North", "S":"South", "E":"East", "W":"West" }
	
	def __init__(self, room_def, x, y):
		if (x < 0):
			raise Exception("Invalid x location for room: x=%s, room_def=%s" % (x, room_def))
		# end if
		if (y < 0):
			raise Exception("Invalid y location for room: y=%s, room_def=%s" % (y, room_def))
		# end if

		self.x_location = x
		self.y_location = y
		self.doors = []
		self.items = []
		self.made_noise_once = False
		self.door_blocked_by_bear_original = None
		self.door_blocked_by_bear = None
		self.bear_is_sleeping = False
		self.user_visited = False

		tmp = room_def.split(":")
		door_flags = tmp[0]
		item_flags = tmp[1]
	
		for flag in door_flags:
			if (flag == "N" or flag == "S" or flag == "E" or flag == "W"):
				self.doors.append(self.DIRECTIONS[flag])
			elif (flag == "-"):
				pass # ignore
			else:
				raise Exception("Room contains an unknown move: %s" % flag)
			# end if
		# end for
		if (len(self.doors) == 0):
			raise Exception("Room specified without doors: room_def=%s" % room_def)
		# end if

		if (item_flags):
			for flag in item_flags:
				if (flag == "I"):
					self.items.append("Instructions")
				elif (flag == "B"):
					self.items.append("Bear")
				elif (flag == "H"):
					self.items.append("Honey")
				elif (flag == "X"):
					self.items.append("Treasure!")
				elif (flag == "n" or flag == "s" or flag == "e" or flag == "w"):
					blocked_door = self.DIRECTIONS[flag.upper()]
					print("blocked_door=%r" % blocked_door) # DEBUG
					if (blocked_door in self.doors and "Bear" in self.items):
						self.door_blocked_by_bear_original = blocked_door
					else:
						pass # ignore
					# end if
				elif (flag == "0"):
					pass # ignore
				else:
					raise Exception("Room contains an unknown item: %s" % flag)
				# end if
			# end for
		# end if
	# end initialize

	def prepare_room(self):
		if ("Bear" in self.items and not self.bear_is_sleeping):
			if (not self.door_blocked_by_bear_original):
				# Pick a random door for the bear to block
				self.door_blocked_by_bear = self.doors[randint(1, len(self.doors))-1]
			else:
				# use the original
				self.door_blocked_by_bear = self.door_blocked_by_bear_original
			# end if
		else:
			# otherwise, there is no bear or it is sleeping
			self.door_blocked_by_bear = None
		# end if
	# end prepare_room

	def inspect(self):
		return "x_location=%d " % self.x_location + \
			"y_location=%d " % self.y_location + \
			"doors=%s " % self.doors + \
			"items=%s " % self.items + \
			"made_noise_once=%s " % self.made_noise_once + \
			"door_blocked_by_bear=%s " % self.door_blocked_by_bear + \
			"bear_is_sleeping=%s " % self.bear_is_sleeping + \
			"user_visited=%s " % self.user_visited
	# end inspect
	
	def describe(self):
		print("You are in a room with exits in the following directions: ")
		for door in range(0,len(self.doors)):
			print("%s" % self.doors[door])
		# end for
		print("")
		if (len(self.items) > 0):
			print("You are not alone in this room. You can see the following: ")
			for item in range(0,len(self.items)):
				print("%s" % self.items[item])
			# end for
			print("")
			if (self.bear_is_sleeping):
				print("The bear is sleeping.")
			elif (self.door_blocked_by_bear):
				print("The bear is blocking the door to the %s." % self.door_blocked_by_bear)
			# end if
		# end if
	# end def describe

	def remove_item(self, item):
		if (item in self.items):
			self.items.remove(item)
			return item
		else:
			pass
		# end if
		return None
	# end remove_item

	def drop_item(self, item):
		self.items.append(item)
	# end drop_item

# end
