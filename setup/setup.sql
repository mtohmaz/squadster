drop user if exists squadster_admin;
create user squadster_admin with SUPERUSER password 'mysharedpassword';

create database squadsterdb;
grant all privileges on database squadsterdb to squadster_admin;
