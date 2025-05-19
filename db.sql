create database lms;
use lms;
create table authors (authorid varchar(40) primary key, name varchar(55) not null, dob date not null, email varchar(75) not null);
create table books (bookid varchar(40) primary key, title varchar(256) not null, isbn varchar(20) not null, publishedYear int not null, authorid VARCHAR(55) NOT NULL, availableCopies int not null, image varchar(70) not null, foreign key(authorid) references authors(authorid)); 

show tables;
desc authors;
desc books;

insert into authors values(1, "Richard Bruce Wright", "1980-05-03", "richard@yahoo.com");
insert into books values(0002005018, "Clara Callan", 0002005018, "Actresses", 2001, 1, 1, "In a small town in Canada, Clara Callan reluctantly takes leave of her sister, Nora, who is bound for New York.");

select title from books limit 20;
delete from books where (not bookid="") and title="A Rose in Winter";

select name from authors limit 20;

alter table books modify title varchar(256) not null;
alter table books drop column summary;

DELETE FROM books where not bookid = "";
DELETE FROM authors where not authorid = "";
drop table login;


create table admins (adminid int primary key auto_increment, name varchar(30) not null, email varchar(50) not null, password varchar(50) not null);
create table members (memberid int primary key auto_increment, name varchar(30) not null, email varchar(50) not null, password varchar(50) not null, phone bigint, address varchar(100), datejoined timestamp not null default current_timestamp);

insert into admins (name, email, password) values ("Tejas Nayak", "tejas@xyz.com", "abcde");
insert into members (name, email, password) values ("Swasthik Yesh", "syesh@xyz.com", "12345");
select * from admins where email="tejas@xyz.com" and password="abcde";

drop table transactions;

create table transactions (transactionid int primary key auto_increment, bookid varchar(40) not null, memberid int not null, issuedate timestamp, duedate timestamp, returndate timestamp, issuedby int, status varchar(20) not null);
create table login (loginid int not null, usertype varchar(10) not null, logintime time not null, logouttime time not null, date date not null);

select * from transactions;
delete from transactions where transactionid > 0;
update transactions set status = "borrowed", duedate = current_timestamp where transactionid = 1;