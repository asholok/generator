CREATE TABLE "category" ( 
	category_id serial primary key, 
	category_title  VARCHAR(50), 
	category_creation_date integer NOT NULL DEFAULT cast(extract(epoch from now()) as integer),
	category_modified integer DEFAULT 0
); 

CREATE OR REPLACE FUNCTION update_category()
RETURN TRIGGER AS $$
BEGIN
	UPDATE "category" SET category_modified = cast(extract(epoch from now()) as integer);
END;

CREATE OR ALERT TRIGGER category_updated_trigger 
	AFTER UPDATE ON "category" 
	FOR EACH ROW EXECUTE PROCEDURE update_category();
CREATE TABLE "article" ( 
	article_id serial primary key, 
	article_text  TEXT, 
	article_title  VARCHAR(50), 
	article_creation_date integer NOT NULL DEFAULT cast(extract(epoch from now()) as integer),
	article_modified integer DEFAULT 0
); 

CREATE OR REPLACE FUNCTION update_article()
RETURN TRIGGER AS $$
BEGIN
	UPDATE "article" SET article_modified = cast(extract(epoch from now()) as integer);
END;

CREATE OR ALERT TRIGGER article_updated_trigger 
	AFTER UPDATE ON "article" 
	FOR EACH ROW EXECUTE PROCEDURE update_article();
