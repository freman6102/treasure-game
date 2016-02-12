import os
from Room import Room

class GameMap(object):

	def __init__(self):
		self.rooms = []

		map_file = open(self.choose_map())
		map_code = map_file.read()
		map_file.close()
		print("map_code=%s" % map_code) # DEBUG
		
		game_map = eval(map_code)

		for x in range(0, len(game_map)):
			begin_map_row = game_map[x]
			game_map_row = []
			for y in range(0, len(begin_map_row)):
				begin_map_room = begin_map_row[y]
				if (begin_map_room):
					game_map_row.append(Room(begin_map_room, x, y))
				else:
					game_map_row.append(None)
				# end if
			# end for
			self.rooms.append(game_map_row)
		# end for
		#print(self.inspect()) # DEBUG
	# end __init__

	def inspect(self):
		text = "Rooms:\n"
		for map_row in self.rooms:
			for r in map_row:				
				text += " #%s\n" % r.inspect()
			# end for
		# end for
		return text
	# end inspect

	def show_known_map(self, maprooms = None):
		if not maprooms: maprooms = self.rooms
		print("Coming Soon ...")
	# end show_known_map

	def choose_map(self):
		# list the available maps
		maps_path = os.path.realpath(os.path.dirname(__file__)) + "/maps"
		print("maps_path=%s" % maps_path)

		choices = {}

		for x in os.listdir(maps_path):
			print("x=%s" % x)  # DEBUG
			if not os.path.isfile(os.path.join(maps_path, x)):
				continue # not a file
			name = os.path.basename(x)
			print("basename=%s" % name)
			base, ext = os.path.splitext(name)
			print("base=%s" % base)  # DEBUG
			print("ext=%s" % ext)  # DEBUG
			if ext.lower() == ".py":
				choices[base] = maps_path + "/" + x
				print("choices[%s]=%s" % (base, choices[base]))  # DEBUG
			# end if
		# end for
		map_file = None
		keys = list(choices)
		if (len(keys) > 0):
			while not map_file:
				print("Please pick a Treasure Map: ")
				for choice in range(0, len(keys)):
					print("%s) %s" % (choice+1, keys[choice]))
				# end for
				print(">>> Type the number of your choice followed by <Enter> or <Return>: ")
				
				choice = input().strip()
				try: 
					choice = int(choice)
					print()
					if (choice > 0 and choice <= len(choices)):
						print("*** choice=%d" % choice)
						print("*** keys[choice]=%s" % keys[choice-1])
						print("*** map_file==choices[keys[choice]]=%s" % choices[keys[choice-1]])
						map_file = choices[keys[choice-1]]
					else:
						pass
					# end if
				except ValueError:
					pass
				# end try
				
				if not map_file:
					print("Sorry, I don't understand that choice. Please try again.")
				# end if
			# end while
		else:
			raise(Exception("TreasureMaps not found in folder: %s" % maps_path))
		# end if
		return map_file
	# end choose_map

# end class

