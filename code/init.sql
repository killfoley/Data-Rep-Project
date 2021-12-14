--drop database if exists
drop database IF EXISTS datarepproject;

--create new database
create database datarepproject;

--initiate new database to add tables
use datarepproject;

--create table Product
create table Product(
Id int NOT NULL AUTO_INCREMENT,
Name varchar(100),
Manufacturer varchar(100),
Supplier varchar(100),
Primary Key(Id))
Engine=InnoDB DEFAULT CHARSET=utf8;

--Create table Stock
create table Stock(
Id INT NOT NULL AUTO_INCREMENT,
SafetyStock INT NULL,
Stock INT NULL,
Location varchar(20),
ProductId INT NULL,
Primary Key(Id),
Foreign Key(ProductId) References Product(Id) ON UPDATE CASCADE ON DELETE SET NULL
)Engine=InnoDB DEFAULT CHARSET=utf8;

--Set the auto increment stock Id
alter table Stock AUTO_INCREMENT=1001;

--Create table Price
create table Price(
Id INT NOT NULL AUTO_INCREMENT,
CostPrice DECIMAL(10,2),
SellPrice DECIMAL(10,2),
ProductId INT NULL,
StockId INT NULL,
Primary Key(Id),
Foreign Key(ProductId) References Product(Id) ON UPDATE CASCADE ON DELETE SET NULL,
Foreign Key(StockId) References Stock(Id) ON UPDATE CASCADE ON DELETE SET NULL
)Engine=InnoDB DEFAULT CHARSET=utf8;

--Set the auto increment Price Id 
alter table Price AUTO_INCREMENT=10001;

/* Insert Product (Name, Manufacturer, Supplier) VALUES ('Impact Driver', 'Makita', 'DrillMen');*/

