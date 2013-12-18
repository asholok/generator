CREATE TABLE "category" ( 
	category_title  VARCHAR(50), 
	category_id serial primary key ); 
CREATE TABLE "article" ( 
	article_text  TEXT, 
	article_title  VARCHAR(50), 
	article_id serial primary key ); 
