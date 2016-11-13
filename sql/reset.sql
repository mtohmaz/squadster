drop database squadsterdb;
create database squadsterdb;

drop user if exists squadster_admin;
create user squadster_admin with SUPERUSER password 'mysharedpassword';
grant all privileges on database squadsterdb to squadster_admin;
