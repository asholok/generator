import yaml

first_sentence 	= 'CREATE TABLE "{0}" ( \n	{0}_id SERIAL PRIMARY KEY, \n'
blank 			= '	{}_{}  {}, \n'
relation_o_to_m = '	{0}_id  INTEGER REFERENCES {0}({0}_id),\n'
date_control 	= """	{0}_creation_date integer NOT NULL DEFAULT cast(extract(epoch from now()) as integer),
	{0}_modified integer DEFAULT 0
	);
"""
trigger 		= """CREATE OR REPLACE FUNCTION update_{0}()
RETURN TRIGGER AS $$
BEGIN
	UPDATE "{0}" SET {0}_modified = cast(extract(epoch from now()) as INTEGER);
	END;

CREATE OR ALERT TRIGGER {0}_updated_trigger
	BERORE UPDATE ON "{0}"
		FOR EACH ROW EXECUTE PROCEDURE update_{0}();
"""

relation_table 	= """CREATE TABLE {0}_{1}_relation (
	{0}_id INTEGER REFERENCES "{0}"({0}_id) UPDATE ON CASCADE,
	{1}_id INTEGER REFERENCES "{1}"({1}_id) UPDATE ON CASCADE,
	{0}_{1}_pkey primary key ({0}_id, {1}_id)
);
"""

class Generator(object):
	_filename = "tables.yaml"
	_relations = {}
	_tables = {}

	
	def __init__(self):
		with open(self._filename, 'r') as f:
			schema = yaml.load(f.read())
		self._set_relations(schema)
		self._set_tables(schema)
		
	def _set_relations(self, schema):
		for table, structure in schema.items():
			if "relations" in structure:
				self._relations[table] = structure["relations"]

	def _set_tables(self, schema):
		for table, structure in schema.items():
			self._tables[table] = structure["fields"]

	def _many_to_many(self):
		relation_tables = []

		for table, relation in self._relations.items():
			for bound, value in self._relations[table].items():
				if value == 'many' and self._relations[bound][table] == 'many' and table < bound:
					relation_tables.append(relation_table.format(table, bound))

		return ''.join(relation_tables)

	def _one_to_many(self, table_name):
		relation_str = []

		if not table_name in self._relations:
			return ''

		for bound, value in self._relations[table_name].items():
			if not table_name in self._relations[bound]:
				raise Exception("no relations with {} <=> {} ".format(table_name, bound))
			if value == 'one' and self._relations[bound][table_name] == 'many':
				relation_str.append(relation_o_to_m.format(bound))

		return ''.join(relation_str)
	
	def _make_table(self, table_name, fields):
		sql = [first_sentence.format(table_name)]

		sql.append(self._one_to_many(table_name))
		for field, content in fields.items():
			sql.append(blanck.format(table_name, field, content))
		sql.append(date_control.format(table_name))

		return ''.join(sql)

	def make_content(self):
		content = []
		
		for table, fields in self._tables.items():
			content.append(self._make_table(table, fields))
			content.append(trigger.format(table))
		content.append(self._many_to_many())

		return ''.join(content)

	def write_into_file(self):	
		sql_string = []
		with open("psql.sql", 'w') as w:
			w.write(self.make_content())
