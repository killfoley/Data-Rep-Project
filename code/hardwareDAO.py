import mysql.connector
import dbconfig as cfg

# Create a Database Access Object Class
class HardwareDAO:
    
    # Function to connect to the database with the local host config file.
    def initconnectToDB(self):
        db = mysql.connector.connect(
        host        =   cfg.mysql['host'],
        user        =   cfg.mysql['user'],
        password    =   cfg.mysql['password'],
        database    =   cfg.mysql['database'],
        pool_name   =   'my_connection_pool',
        pool_size   =   5
        )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name = 'my_connection_pool',
        )
        return db

    # Call the connection function
    def __init__(self): 
        db = self.initconnectToDB()
        db.close()
    
    # Function for creating entries        
    def create(self, values):
        db = self.getConnection()
        cursor = db.getCursor()
        sql='''
                BEGIN;
                Insert into Product (Id, Name, Manufacturer, Supplier, SafetyStock, CurrentStock)
		            VALUES (default, %s, %s, %s, %s, %s);
                Insert into Price (Id, CostPrice, SellPrice, ProductId)
		            VALUES (%s, %s, %s, last_insert_id());
                COMMIT; 
            '''
        cursor.execute(sql, values)

        self.db.commit()
        lastrowID = cursor.lastrowid
        db.close()
        return lastrowID

    # Function for getting all entries from database
    def getAll(self):
        db = self.getConnection()
        cursor = self.getCursor()
        sql="select * from Product A inner join Price B on A.Id = B.ProductId"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        db.close()
        return returnArray

    # Function to search by Product ID
    def findByID(self, id):
        db = self.getConnection()
        cursor = self.getCursor()
        sql="select * from BLANK where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        product = self.convertToDictionary(result)
        db.close()
        return product

    # Function to update existing entries
    def update(self, values):
        db = self.getConnection()
        cursor = self.getCursor()
        sql="update BLANK set title= %s,author=%s, price=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
        db.close()
    
    #Function to delete entries for DB
    def delete(self, id):
        db = self.getConnection()
        cursor = self.db.cursor()
        sql="delete from BLANK where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        db.close()

    # Function to convert SQL array to Python dict
    def convertToDictionary(self, result):
        colnames=['Id', 'Name', 'Manufacturer', 'Supplier', 'SafetyStock', 'CurrentStock', 'Id', 'CostPrice', 'SellPrice', 'ProductId']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
HardwareDAO = HardwareDAO()