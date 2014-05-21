import yaml

first_sentence 	= 'CREATE TABLE "{0}" ( \n	{0}_id serial primary key, \n'
blanck 			= '	{}_{}  {}, \n'
date_control 	= '	{0}_creation_date integer NOT NULL DEFAULT cast(extract(epoch from now()) as integer),\n	{0}_modified integer DEFAULT 0\n); \n\n'
trigger 		= 'CREATE OR REPLACE FUNCTION update_{0}()\nRETURN TRIGGER AS $$\nBEGIN\n	UPDATE "{0}" SET {0}_modified = cast(extract(epoch from now()) as integer);\nEND;\n\nCREATE OR ALERT TRIGGER {0}_updated_trigger \n	AFTER UPDATE ON "{0}" \n	FOR EACH ROW EXECUTE PROCEDURE update_{0}();\n'

def make_sql_request(table_name, fields):
	sql = [first_sentence.format(table_name)]
	
	for key, value in fields.items():
		sql.append(blanck.format(table_name, key, value))
	
	sql.append(date_control.format(table_name))
	sql.append(trigger.format(table_name))
	
	return ''.join(sql)

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