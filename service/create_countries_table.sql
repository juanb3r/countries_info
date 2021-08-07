CREATE TABLE IF NOT EXISTS countries (
	id integer PRIMARY KEY AUTOINCREMENT,
	region text NOT NULL,
	country text NOT NULL,
	language integer NOT NULL,
	time integer
);