
create user team1 with NOCREATEUSER password 'mysharedpassword';

create database team1db;
grant all privileges on database team1db to team1;
