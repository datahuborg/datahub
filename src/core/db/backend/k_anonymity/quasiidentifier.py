from interval import *

import collections
import json
import os

class QuasiIdentifier(object):
	def __init__(self, index, template):
		self.index = index
		self.name = template["column"]

		"""
		self.name = name

		directory = os.path.dirname(__file__)
		fp = os.path.join(directory, 'generalizations/%s.json' % self.name)

		if not os.path.exists(fp):
			raise Exception("The attribute %s is not supported." % self.name)

		with open(fp, "r") as f:
			template = json.load(f)
		"""
			
		self.category_mapping = template["category"]

		self.reverse_category_mapping = {}
		for key in template["category"]:
			self.reverse_category_mapping[template["category"][key]] = str(key)

		self._parse_hierarchy(template["hierarchy"])

	def _parse_hierarchy(self, root):
		self.parent_lookup = {}
		self.children_lookup = {}
		self.leaf_intervals = []
		self.suppression_value = str(root["value"])

		queue = collections.deque()
		queue.append(root)

		while len(queue) > 0:
			node = queue.popleft()

			parent_value = str(node["value"])
			parent_interval = Interval(parent_value)
			children_values = []

			for child in node["children"]:
				child_value = str(child["value"])

				self.parent_lookup[child_value] = parent_value

				queue.append(child)
				children_values.append(child_value)

				if not parent_interval.contains_interval(Interval(child_value)):
					raise Exception("The hierachy is ill-formatted.")

			if node["children"]:
				self.children_lookup[parent_value] = children_values
			else:
				self.leaf_intervals.append(parent_interval)

		# if self.category_mapping:
		# 	for key in self.category_mapping:
		# 		value = self.category_mapping[key]
		# 		gen_value = self.generalize(str(value))
		# 		if not gen_value:
		# 			raise Exception("A category value cannot be generalized to any value.")

	def generalize(self, value):
		if value == self.suppression_value:
			return value

		if value in self.parent_lookup:
			return self.parent_lookup[value]

		for interval in self.leaf_intervals:
			if interval.compare_str(value):
				return interval.str

		return None