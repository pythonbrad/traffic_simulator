import random

class Path:
	'''
		This class contruct a path begin by A and end by B in using the carrefour_data
	'''
	def __init__(self, carrefour_data):
		self.carrefour_data = carrefour_data
		self.begin = None
		self.end = None
		self.path = []
		self.carrefour_to_ignore = {}
		# If true, we will increase the probability to obtain different paths with same begin and end
		self.random_path = 0
	def find(self, begin, end):
		self.begin = begin
		self.end = end
		# We clean data
		self.path = [self.begin]
		if not end in self.carrefour_to_ignore:
			self.carrefour_to_ignore[end] = []
		# We start the browse and return the status
		return self.browse(1)
	def browse(self, path_length):
		# We verify if path end by end
		if self.path[-1] == self.end:
			return 1
		else:
			# We get near carrefours
			near_carrefours = self.carrefour_data[self.path[-1]]
			# We shuffle to obtain an random path
			if self.random_path:
				random.shuffle(near_carrefours)
			# We browse it if not already present and used
			for near_carrefour in near_carrefours:
				# We restore the path if modified
				# Because can be modified the previous loop
				self.path = self.path[:path_length]
				if not near_carrefour in self.path and not near_carrefour in self.carrefour_to_ignore[self.end]:
					# We save the near carrefour
					self.path.append(near_carrefour)
					# We start a new browse, and increment the path length
					path_found = self.browse(path_length+1)
					# We verify if path found
					if path_found:
						return path_found
					else:
						# We mark it inutile to evit an inutile browse
						self.carrefour_to_ignore[self.end].append(near_carrefour)
		# If we arrive here, path not found
		return 0
