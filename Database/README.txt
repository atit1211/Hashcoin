if you do not want to import the files in your database copy paste the following query
in the MySQL command line interface


create database hashcoin;
use hashcoin;
create table ledger(
transaction_id varchar(17),
sender varchar(6),
reciever varchar(6),
amount int,
hash varchar(50),
prev_hash varchar(50),
primary key(transaction_id));
create table sum_hash(
sum varchar(100));
create table user(
user_id varchar(26),
fname varchar(26),
lname varchar(26),
pin_no varchar(26),
private_key varchar(26),
password varchar(26),
primary key(user_id),
unique (private_key));
create table wallet(
wallet_id varchar(6),
user_id varchar(26),
balance int,
primary key(wallet_id));
