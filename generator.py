import yaml

def make_sql_request(table_name, fields):
	id_field = '	{}_id serial primary key'.format(table_name)
	sql = ['CREATE TABLE "{}" ( \n'.format(table_name)]

	for key, value in fields.items():
		sql.append('	{}_{}  {}, \n'.format(table_name, key, value))
	
	sql.append(id_field)
	sql.append(' ); \n')

	res = ''.join(sql)
	return res

def make_string():	
	sql_string = []
	with open("tables.yaml", 'r') as f:
		schema = yaml.load(f.read())
	for table, structure in schema.items():
		sql_string.append(make_sql_request(table, structure["fields"]))
	statement = ''.join(sql_string)
	with open("psql.sql", 'w') as d:
		d.write(statement)
	
	return statement

if __name__ == '__main__':
	print(make_string())