-- create a database call hbnb_dev_db  for hbnb project
-- create a new user call hbnb_dev in localhost
-- grat all privelage for hbn_dev user on hbnb_dev_db database
-- grant only select privellage for hbn_dev user on perfomance_schema

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

GRANT ALL PRIVILEGES on `hbnb_dev_db`.*
	TO 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

GRANT SELECT on `performance_schema`.*
	TO 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

FLUSH PRIVILEGES;
