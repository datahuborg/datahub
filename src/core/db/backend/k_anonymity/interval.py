TYPE_INCLUDE_LOW_INCLUDE_HIGH = 1
TYPE_INCLUDE_LOW_EXCLUDE_HIGH = 2
TYPE_EXCLUDE_LOW_INCLUDE_HIGH = 3
TYPE_EXCLUDE_LOW_EXCLUDE_HIGH = 4

class Interval(object):
	def __init__(self, s):
		if ":" in s:
			self.low, self.high = map(float, s[1:-1].split(":"))
			self.str = s

			if s[0] == "[":
				if s[-1] == "]":
					self.type = TYPE_INCLUDE_LOW_INCLUDE_HIGH
				else:
					self.type = TYPE_INCLUDE_LOW_EXCLUDE_HIGH
			else:
				if s[-1] == "]":
					self.type = TYPE_EXCLUDE_LOW_INCLUDE_HIGH
				else:
					self.type = TYPE_EXCLUDE_LOW_EXCLUDE_HIGH

			if self.low > self.high or (self.low == self.high and self.type != TYPE_INCLUDE_LOW_INCLUDE_HIGH):
				raise Exception("The interval is empty.")
		else:
			if (s.startswith("(") or s.startswith("[")) and \
				(s.endswith(")") or s.endswith("]")):
					if s[0] == "(" and s[-1] == ")":
						raise Exception("Empty interval")
					s = s[1:-1]

			value = float(s)
			self.low = value
			self.high = value
			self.str = "[%s]" % value
			self.type = TYPE_INCLUDE_LOW_INCLUDE_HIGH

	def includes_low(self):
		return self.type == TYPE_INCLUDE_LOW_INCLUDE_HIGH or self.type == TYPE_INCLUDE_LOW_EXCLUDE_HIGH

	def includes_high(self):
		return self.type == TYPE_INCLUDE_LOW_INCLUDE_HIGH or self.type == TYPE_EXCLUDE_LOW_INCLUDE_HIGH

	def contains_value(self, value):
		value = float(value)

		if self.type == TYPE_INCLUDE_LOW_INCLUDE_HIGH:
			return self.low <= value <= self.high
		elif self.type == TYPE_INCLUDE_LOW_EXCLUDE_HIGH:
			return self.low <= value < self.high
		elif self.type == TYPE_EXCLUDE_LOW_INCLUDE_HIGH:
			return self.low < value <= self.high
		elif self.type == TYPE_EXCLUDE_LOW_EXCLUDE_HIGH:
			return self.low < value < self.high
		else:
			raise Exception("The value does not belong to the interval.")

	def contains_interval(self, interval):
		if self.low > interval.low:
			return False

		if self.high < interval.high:
			return False

		if self.low == interval.low and self.includes_low() != interval.includes_low():
			return False

		if self.high == interval.high and self.includes_high() != interval.includes_high():
			return False

		return True

	def compare_str(self, s):
		try:
			val = float(s)
			return self.contains_value(val)
		except Exception:
			try:
				interval = Interval(s)
				return self.contains_value(interval.low)
			except Exception:
				raise Exception("Error while comparing value.")