# import pgdb
import sys

from interval import *
from quasiidentifier import *
from privatetable import *
from equivalencetable import *
from collections import deque

from psycopg2.extensions import AsIs

class KAnonymizer(object):
	def __init__(self, backend, repo, table_name, templates, k):
		self.backend = backend

		self.repo = repo
		self.table_name = table_name
		self.qids = self._create_quasi_ids(templates)

		self.k = k
		self.suppression_threshold = k
		self.full_domain_gen = True

		self.pv_table_index = 1
		self.eq_table_index = 1

		self.pv_table = PrivateTable(backend, repo, "pv_%s" % self.pv_table_index, self.qids)
		self.eq_table = EquivalenceTable(backend, repo, "eq_%s" % self.eq_table_index, self.qids)

		self._insert_values()

	def _create_quasi_ids(self, templates):
		try:
			query = "SELECT * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '%s';"
			params = (AsIs(self.table_name),)

			result = self.backend.execute_sql(query, params)
			rows, positions = result['tuples'], result['positions']

			column_map = {}
			for row in rows:
				column_map[row[positions['column_name']]] = row[positions['ordinal_position']] - 1

			quasi_ids = []
			for template in templates:
				index = column_map[template["column"]]
				quasi_ids.append(QuasiIdentifier(index, template))

			return quasi_ids

		except KeyError:
			raise Exception("Please make sure the quasi attributes are columns of the specified table.")
		except:
			raise Exception("An unknown error occurred.")

	def _insert_values(self):
		try:
			query = "SELECT * FROM %s.%s"
			params = [AsIs(self.repo), AsIs(self.table_name)]
			rows = self.backend.execute_sql(query, params)["tuples"]

			for row in rows:
				values = list(row)
				eid = self.eq_table.insert_values(values)
				self.pv_table.insert_values(eid, values)
		except Exception as e:
			raise e

	def is_ready_for_suppression(self):
		size_sum = 0
		eq_to_be_suppressed = deque()

		query = "SELECT EID, COUNT(*) FROM %s.%s GROUP BY EID ORDER BY COUNT(*) ASC;"
		params = [AsIs(self.repo), AsIs(self.pv_table.name)]
		result = self.backend.execute_sql(query, params)["tuples"]

		for eid, count in result:
			eid, count = float(eid), int(count)

			if count < self.k:
				eq_to_be_suppressed.append(eid)
				size_sum += count
				if self.suppression_threshold > 0 and size_sum > self.suppression_threshold:
					return None
			else:
				return eq_to_be_suppressed

		return eq_to_be_suppressed

	def suppress_eq(self, suppression_list):
		gen_vals = []
		for qid in self.qids:
			gen_vals.append(qid.suppression_value)

		if suppression_list:
			suppression_eid = -1
			if len(suppression_list) > 0:
				try:
					suppression_eid = self.eq_table.insert(gen_vals)
				except:
					raise Exception("Error while trying to insert suppression values")

			while len(suppression_list) > 0:
				eid = suppression_list.popleft()
				self.eq_table.delete_eid(eid)
				self.pv_table.update_eid(eid, suppression_eid)

	def create_public_table(self):
		try:
			query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'%s\';"
			params = [AsIs(self.table_name + "_public")]
			result = self.backend.execute_sql(query, params)["tuples"]

			if len(result) > 0:
				self.backend.delete_table(self.repo, self.table_name + "_public")

			query = "SELECT * INTO %s.%s_public FROM %s.%s WHERE 1 = 2;"
			params = [AsIs(self.repo), AsIs(self.table_name), AsIs(self.repo), AsIs(self.table_name)]
			self.backend.execute_sql(query, params)
			self.backend.connection.commit()

			for qid in self.qids:
				query = "ALTER TABLE %s.%s_public ALTER COLUMN %s TYPE VARCHAR(50);"
				params = [AsIs(self.repo), AsIs(self.table_name), AsIs(qid.name)]
				self.backend.execute_sql(query, params)
				self.backend.connection.commit()

			query = "SELECT * FROM %s.%s;"
			params = [AsIs(self.repo), AsIs(self.table_name)]
			result = self.backend.execute_sql(query, params)["tuples"]

			for rid in range(len(result)):
				row = result[rid]
				row_values = list(row)

				query = "SELECT * FROM %s.%s WHERE RID = %s;"
				params = [AsIs(self.repo), AsIs(self.pv_table.name), AsIs(rid)]

				res = self.backend.execute_sql(query, params)
				positions = res["positions"]
				pv_row = res["tuples"][0]

				for qid in self.qids:
					column = "att_%s" % qid.index

					query = "SELECT %s FROM %s.%s WHERE EID = %s;"
					params = [AsIs(column), AsIs(self.repo), AsIs(self.eq_table.name), AsIs(pv_row[positions["eid"]])]
					eq_value = self.backend.execute_sql(query, params)["tuples"][0][0]

					new_value = eq_value
					if qid.reverse_category_mapping:
						if eq_value == qid.suppression_value:
							new_value = qid.reverse_category_mapping[-1]
						else:
							interval = Interval(eq_value)
							new_value = qid.reverse_category_mapping[interval.low]

					row_values[qid.index] = new_value

				query = "INSERT INTO %s.%s_public VALUES "
				params = [AsIs(self.repo), AsIs(self.table_name)]

				columns = []
				for value in row_values:
					columns.append("'%s'" % value)

				query += "(%s);" % ",".join(columns)

				self.backend.execute_sql(query, params)
				self.backend.connection.commit()

			return "%s_public" % self.table_name

		except Exception as e:
			raise e

	def anonymize(self):
		try:
			query = "SELECT COUNT(*) FROM %s.%s;"
			params = [AsIs(self.repo), AsIs(self.pv_table.name)]
			result = self.backend.execute_sql(query, params)["tuples"]

			size = int(result[0][0])
			if size < self.k:
				raise Exception("The number of elements in the anon table is less than k.")

			suppression_list = self.is_ready_for_suppression()
			while suppression_list is None:
				gen_domain_counts = []
				for qid in self.qids:
					query = "SELECT COUNT(*) FROM (SELECT COUNT(*) FROM %s.%s GROUP BY ATT_%s) AS T;"
					params = [AsIs(self.repo), AsIs(self.eq_table.name), AsIs(qid.index)]
					result = self.backend.execute_sql(query, params)["tuples"]
					gen_domain_counts.append(int(result[0][0]))

				gen_att = 0
				for i in range(len(gen_domain_counts)):
					if gen_domain_counts[i] > gen_domain_counts[gen_att]:
						gen_att = i

				self.eq_table_index += 1
				new_eq_table_name = "eq_%d" % self.eq_table_index
				new_eq_table = EquivalenceTable(self.backend, self.repo, new_eq_table_name, self.qids)

				self.pv_table_index += 1
				new_pv_table_name = "pv_%d" % self.pv_table_index
				new_pv_table = PrivateTable(self.backend, self.repo, new_pv_table_name, self.qids)

				query = "SELECT EID FROM %s.%s;"
				params = [AsIs(self.repo), AsIs(self.eq_table.name)]
				result = self.backend.execute_sql(query, params)["tuples"]

				for row in result:
					old_eid = float(row[0])
					old_count = self.pv_table.get_equivalence_size(old_eid)

					gen_vals = self.eq_table.get_equivalence(old_eid)

					if old_count < self.k or self.full_domain_gen:
						gen_vals[gen_att] = self.qids[gen_att].generalize(gen_vals[gen_att])

					new_eid = new_eq_table.get_eid(gen_vals)
					if new_eid == -1:
						new_eid = new_eq_table.insert(gen_vals)

					new_pv_table.copy_from_table(self.pv_table, old_eid, new_eid)

				self.pv_table.delete()
				self.pv_table = new_pv_table

				self.eq_table.delete()
				self.eq_table = new_eq_table

				suppression_list = self.is_ready_for_suppression()

			self.suppress_eq(suppression_list)

			self.create_public_table()

			self.pv_table.delete()
			self.eq_table.delete()
		except Exception as e:
			raise e