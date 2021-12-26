-- drop database if exists
drop database IF EXISTS datarepproject;

-- create new database
create database datarepproject;

-- initiate new database to add tables
use datarepproject;

-- create table Product
create table Product(
ProdId int NOT NULL AUTO_INCREMENT,
Name varchar(100),
Manufacturer varchar(100),
Supplier varchar(100),
SafetyStock INT NULL,
CurrentStock INT NULL,
Primary Key(ProdId))
Engine=InnoDB DEFAULT CHARSET=utf8MB4;

-- Create table Price
create table Price(
PriceId INT NOT NULL AUTO_INCREMENT,
CostPrice DECIMAL(10,2),
SellPrice DECIMAL(10,2),
ProductId INT NULL,
Primary Key(PriceId),
CONSTRAINT fk_product_id
Foreign Key (ProductId) References Product(ProdId) ON DELETE CASCADE ON UPDATE CASCADE
)Engine=InnoDB DEFAULT CHARSET=utf8MB4;

-- Set the auto increment Price Id 
alter table Price AUTO_INCREMENT=1001;

-- Insert a row into both tables
BEGIN;
Insert into Product (ProdId, Name, Manufacturer, Supplier, SafetyStock, CurrentStock)
		VALUES (default, "Hammer", "Stanley", "Screwfix", 8, 15);
Insert into Price (PriceId, CostPrice, SellPrice, ProductId)
		VALUES (default, 9.50, 12.95, last_insert_id());
COMMIT;

-- Insert a row into both tables
BEGIN;
Insert into Product (ProdId, Name, Manufacturer, Supplier, SafetyStock, CurrentStock)
		VALUES (default, "Stanley Knife", "Stanley", "Screwfix", 5, 12);
Insert into Price (PriceId, CostPrice, SellPrice, ProductId)
		VALUES (default, 4.75, 6.50, last_insert_id());
COMMIT;

-- Insert a row into both tables
BEGIN;
Insert into Product (ProdId, Name, Manufacturer, Supplier, SafetyStock, CurrentStock)
		VALUES (default, "DeWalt 18V Cordless Drill", "DeWalt", "DrillMen", 5, 8);
Insert into Price (PriceId, CostPrice, SellPrice, ProductId)
		VALUES (default, 85.95, 120.95, last_insert_id());
COMMIT;