# import pgdb

# from quasiidentifier import *

from psycopg2.extensions import AsIs

class PrivateTable(object):
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

			columns = ["RID BIGINT PRIMARY KEY", "EID BIGINT"]
			for qid in self.qids:
				columns.append("ATT_%d VARCHAR(128)" % qid.index)

			query += "(%s);" % ",".join(columns)

			self.backend.execute_sql(query, params)
			self.backend.connection.commit()

			"""
			query = "SELECT * from INFORMATION_SCHEMA.TABLES where TABLE_NAME = '%s';"
			params = (AsIs(self.name),)

			result = self.backend.excute(query, params)["tuples"]

			if len(result) > 0:
				query = "DROP TABLE %s"
				params = (AsIs(self.name),)
				self.backend.excute(query, params)

			query = "CREATE TABLE %s "
			params = [AsIs(self.name)]

			columns = ["RID BIGINT PRIMARY KEY", "EID BIGINT"]
			for qid in self.qids:
				columns.append("ATT_%d FLOAT")
				params.append(AsIs(qid.index))

			query += "(%s);" % ",".join(columns)

			self.backend.execute(query, params)
			self.backend.connection.commit()

			select_sql = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'%s\';" % self.name
			result = self.cursor.execute(select_sql).fetchall()

			if len(result) > 0:
				drop_sql = "DROP TABLE %s" % self.name
				self.cursor.execute(drop_sql)

			create_sql = "CREATE TABLE %s " % self.name

			columns = ["RID BIGINT PRIMARY KEY", "EID BIGINT"]
			for qid in self.qids:
				columns.append("ATT_%d FLOAT" % qid.index)

			create_sql += "(%s);" % ",".join(columns)

			self.backend.execute(query, params)
			self.backend.connection.commit()
			"""
		except Exception as e:
			raise e

	def insert(self, eid, qid_values):
		try:
			rid = 0

			query = "SELECT MAX(RID) FROM %s.%s"
			params = [AsIs(self.repo), AsIs(self.name)]
			result = self.backend.execute_sql(query, params)["tuples"]

			if result[0][0] is not None:
				rid = int(result[0][0]) + 1
				
			query = "INSERT INTO %s.%s VALUES "
			params = [AsIs(self.repo), AsIs(self.name)]

			columns = [str(rid), str(eid)]
			for value in qid_values:
				columns.append("'%s'" % value)

			query += "(%s);" % ",".join(columns)

			self.backend.execute_sql(query, params)
			self.backend.connection.commit()

			"""
			rid = 0

			select_sql = "SELECT MAX(RID) FROM %s" % self.name
			result = self.cursor.execute(select_sql).fetchall()
			if result[0][0] is not None:
				rid = int(result[0][0]) + 1

			insert_sql = "INSERT INTO %s VALUES " % self.name

			columns = [str(rid), str(eid)]
			for value in qid_values:
				columns.append(str(value))

			insert_sql += "(%s);" % ",".join(columns)

			self.cursor.execute(insert_sql)
			self.connection.commit()
			"""
		# except pgdb.ProgrammingError:
		# 	print "Please check your values."
		# 	self.connection.rollback()
		except Exception as e:
			raise e

	def insert_values(self, eid, values):
		qid_values = []
		for qid in self.qids:
			value = values[qid.index]
			if qid.category_mapping:
				qid_values.append(qid.category_mapping[value])
			else:
				qid_values.append(float(value))

		self.insert(eid, qid_values)

	def delete(self):
		try:
			self.backend.delete_table(self.repo, self.name)
		except Exception as e:
			raise e

	def update_eid(self, old_eid, new_eid):
		try:
			query = "UPDATE %s.%s SET EID = %s WHERE EID = %s;"
			params = [AsIs(self.repo), AsIs(self.name), AsIs(new_eid), AsIs(old_eid)]

			self.backend.execute_sql(query, params)
			self.backend.connection.commit()

			"""
			update_sql = "UPDATE %s SET EID = %s WHERE EID = %s" % (self.name, str(new_eid), str(old_eid))
			self.cursor.execute(update_sql)
			self.connection.commit()
			"""
		except Exception as e:
			raise e

	def copy_from_table(self, table, old_eid, new_eid):
		try:
			query = "INSERT INTO %s.%s SELECT "
			params = [AsIs(self.repo), AsIs(self.name)]

			columns = ["RID", str(new_eid)]
			for qid in self.qids:
				columns.append("ATT_%d" % qid.index)

			query += ",".join(columns) + " FROM %s.%s WHERE EID = %s" % (table.repo, table.name, str(old_eid))

			self.backend.execute_sql(query, params)
			self.backend.connection.commit()

			"""
			insert_sql = "INSERT INTO %s SELECT " % self.name

			columns = ["RID", str(new_eid)]
			for qid in self.qids:
				columns.append("ATT_%d" % qid.index)

			insert_sql += ",".join(columns) + " FROM %s WHERE EID = %s" % (table.name, str(old_eid))
			self.cursor.execute(insert_sql)
			self.connection.commit()
			"""
		except Exception as e:
			raise e

	def get_equivalence_size(self, eid):
		try:
			query = "SELECT COUNT (*) FROM %s.%s WHERE EID = %s;"
			params = [AsIs(self.repo), AsIs(self.name), AsIs(eid)]

			result = self.backend.execute_sql(query, params)["tuples"]
			
			if len(result) > 0:
				return int(result[0][0])

			return 0

			"""
			select_sql = "SELECT COUNT (*) FROM %s WHERE EID = %s" % (self.name, str(eid))
			result = self.cursor.execute(select_sql).fetchall()

			if len(result) > 0:
				return int(result[0][0])

			return 0
			"""
		except Exception as e:
			raise e

	def is_k_anonymous(self, k):
		try:
			query = "SELECT COUNT(*) FROM %s.%s GROUP BY EID ORDER BY COUNT(*) ASC;"
			params = [AsIs(self.repo), AsIs(self.name)]

			result = self.backend.execute_sql(query, params)["tuples"]
			
			if len(result) > 0:
				min_count = int(result[0][0])
				return min_count >= k
			
			return True

			"""
			select_sql = "SELECT COUNT(*) FROM %s GROUP BY EID ORDER BY COUNT(*) ASC" % self.name
			result = self.cursor.execute(select_sql).fetchall()

			if len(result) > 0:
				min_count = int(result[0][0])
				return min_count >= k
			
			return True
			"""
		except Exception as e:
			raise e

# q1 = QuasiIdentifier(0, "age")
# q2 = QuasiIdentifier(1, "gender")
# p = PrivateTable("localhost", "testdb", "test", [q1, q2])