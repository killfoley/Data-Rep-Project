import mysql.connector
import dbconfig as cfg

# Create a Database Access Object Class
class HardwareDAO:
    db = ""

    # Call the connection function
    def __init__(self): 
        self.db = self.initconnectToDB()
        self.db.close()
    
    # Function to connect to the database with the local host config file.
    def initconnectToDB(self):
        self.db = mysql.connector.connect(
            host=cfg.mysql['host'],
            user=cfg.mysql['username'],
            password=cfg.mysql['password'],
            database=cfg.mysql['database'],
            pool_name='my_connection_pool',
            pool_size=5
        )
        return self.db

    def getConnection(self):
        self.db = mysql.connector.connect(
            pool_name = 'my_connection_pool',
        )
        return self.db

    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor()

    
    # Function for creating entries        
    def create(self, values):
        db = self.getConnection()
        cursor = db.getCursor()
        sql='''
                BEGIN;
                Insert into Product (ProdId, Name, Manufacturer, Supplier, SafetyStock, CurrentStock)
		            VALUES (default, %s, %s, %s, %s, %s);
                Insert into Price (PriceId, CostPrice, SellPrice, ProductId)
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
        sql="select * from Product A inner join Price B on A.ProdId = B.ProductId"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        db.close()
        return returnArray

    # Function to search by Product ID
    def findByID(self, id):
        db = self.getConnection()
        cursor = self.getCursor()
        sql="select * from Product A inner join Price B on A.ProdId = B.ProductId where A.ProdId = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        find_product = self.convertToDictionary(result)
        db.close()
        return find_product

    # Function to update existing entries
    def update(self, product):
        db = self.getConnection()
        cursor = self.getCursor()
        sql='''
        UPDATE Product A, Price B
        SET A.Name = %s, A.Manufacturer = %s, A.Supplier = %s, A.SafetyStock = %s, A.CurrentStock = %s,
        B.CostPrice = %s, B.SellPrice = %s
        where A.ProdId = B.ProductId AND A.ProdId = %s;     
        '''
        values = [product['name'], product['manufacturer'], product['supplier'],
                product['safetystock'], product['currentstock'], product['costprice'],
                product['sellprice']]
        cursor.execute(sql, values)
        self.db.commit()
        db.close()
    
    #Function to delete entries for DB
    def delete(self, id):
        db = self.getConnection()
        cursor = self.db.cursor()
        sql= "delete from Product where ProdId = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        db.close()

    # Function to convert SQL array to Python dict
    def convertToDictionary(self, result):
        colnames=['ProdId', 'Name', 'Manufacturer', 'Supplier', 'SafetyStock', 'CurrentStock', 'PriceId', 'CostPrice', 'SellPrice', 'ProductId']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
HardwareDAO = HardwareDAO()