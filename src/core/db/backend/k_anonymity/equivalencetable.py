from interval import *

from quasiidentifier import *

# import pgdb

from psycopg2.extensions import AsIs

class EquivalenceTable(object):
	def __init__(self, backend, repo, name, qids):
		self.backend = backend

		self.repo = repo
		self.name = name
		self.qids = qids

		self._create()

	def _create(self):
		try:
			query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'%s\';"
			params = [AsIs(self.name)]
			result = self.backend.execute_sql(query, params)["tuples"]

			if len(result) > 0:
				self.backend.delete_table(self.repo, self.name)

			query = "CREATE TABLE %s.%s "
			params = [AsIs(self.repo), AsIs(self.name)]

			columns = ["EID BIGINT PRIMARY KEY"]
			for qid in self.qids:
				columns.append("ATT_%d VARCHAR(128)" % qid.index)

			query += "(%s);" % ",".join(columns)

			self.backend.execute_sql(query, params)
			self.backend.connection.commit()
		except Exception as e:
			raise e

	def insert(self, qid_values):
		try:
			eid = self.get_eid(qid_values)

			if eid == -1:
				eid = 0

				query = "SELECT MAX(EID) FROM %s.%s"
				params = [AsIs(self.repo), AsIs(self.name)]
				result = self.backend.execute_sql(query, params)["tuples"]

				if result[0][0] is not None:
					eid = int(result[0][0]) + 1

				query = "INSERT INTO %s.%s VALUES "
				params = [AsIs(self.repo), AsIs(self.name)]

				columns = [str(eid)]
				for value in qid_values:
					columns.append("'%s'" % value)

				query += "(%s);" % ",".join(columns)

				self.backend.execute_sql(query, params)
				self.backend.connection.commit()

			return eid
		except Exception as e:
			raise e

	def insert_values(self, values):
		try:
			qid_values = []
			for qid in self.qids:
				value = values[qid.index]
				if qid.category_mapping:
					value = qid.category_mapping[value]
				interval = Interval(str(value))
				qid_values.append(interval.str)

			eid = self.get_eid(qid_values)

			if eid == -1:
				eid = self.insert(qid_values)

			return eid
		except Exception as e:
			raise e

	def delete(self):
		try:
			self.backend.delete_table(self.repo, self.name)
		except Exception as e:
			raise e

	def delete_eid(self, eid):
		try:
			query = "DELETE FROM %s.%s WHERE EID = %s;"
			params = [AsIs(self.repo), AsIs(self.name), AsIs(eid)]

			self.backend.execute_sql(query, params)
			self.backend.connection.commit()
		except Exception as e:
			raise e

	def get_eid(self, qid_values):
		try:
			query = "SELECT EID FROM %s.%s WHERE "
			params = [AsIs(self.repo), AsIs(self.name)]

			columns = []
			for i in range(len(self.qids)):
				columns.append("ATT_%d = '%s'" % (self.qids[i].index, qid_values[i]))

			query += " AND ".join(columns)

			result = self.backend.execute_sql(query, params)["tuples"]

			if len(result) > 0:
				return int(result[0][0])

			return -1
		except Exception as e:
			raise e

	def get_equivalence(self, eid):
		try:
			query = "SELECT * FROM %s.%s WHERE EID = %s;"
			params = [AsIs(self.repo), AsIs(self.name), AsIs(eid)]

			result = self.backend.execute_sql(query, params)["tuples"]
			
			if len(result) > 0:
				values = []
				for i in range(len(self.qids)):
					values.append(result[0][i+1])
				return values
			
			return None
		except Exception as e:
			raise e

	def test(self):
		columns_sql = "SELECT * from test3"
		return self.cursor.execute(columns_sql).fetchall()