-- drop database if exists
drop database IF EXISTS datarepproject;

-- create new database
create database datarepproject;

-- initiate new database to add tables
use datarepproject;

-- create table Product
create table Product(
Id int NOT NULL AUTO_INCREMENT,
Name varchar(100),
Manufacturer varchar(100),
Supplier varchar(100),
SafetyStock INT NULL,
CurrentStock INT NULL,
Primary Key(Id))
Engine=InnoDB DEFAULT CHARSET=utf8;

-- Create table Price
create table Price(
Id INT NOT NULL AUTO_INCREMENT,
CostPrice DECIMAL(10,2),
SellPrice DECIMAL(10,2),
ProductId INT NULL,
Primary Key(Id),
Foreign Key(ProductId) References Product(Id) ON UPDATE CASCADE ON DELETE SET NULL
)Engine=InnoDB DEFAULT CHARSET=utf8;

-- Set the auto increment Price Id 
alter table Price AUTO_INCREMENT=1001;

-- Insert a row into both tables
BEGIN;
Insert into Product (Id, Name, Manufacturer, Supplier, SafetyStock, CurrentStock)
		VALUES (default, "Hammer", "Stanley", "Screwfix", 8, 15);
Insert into Price (Id, CostPrice, SellPrice, ProductId)
		VALUES (default, 9.50, 12.95, last_insert_id());
COMMIT;