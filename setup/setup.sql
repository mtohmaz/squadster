
create user squadster_admin with NOCREATEUSER password 'mysharedpassword';

create database squadsterdb;
grant all privileges on database squadsterdb to squadster_admin;
