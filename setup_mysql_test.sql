-- create a database call hbnb_test_db  for hbnb test project
-- create a new user call hbnb_test in localhost
-- grat all privelage for hbn_test user on hbnb_test_db database
-- grant only select privellage for hbn_test user on perfomance_schema

CREATE DATABASE IF NOT EXISTS hbnb_test_db;

CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

GRANT ALL PRIVILEGES on `hbnb_test_db`.*
	TO 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

GRANT SELECT on `performance_schema`.*
	TO 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

FLUSH PRIVILEGES;
