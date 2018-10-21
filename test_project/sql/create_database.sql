/*
This file is used to bootstrap development database.

Note: ONLY development database;
*/

CREATE USER test_project SUPERUSER;
CREATE DATABASE test_project OWNER test_project ENCODING 'utf-8';
