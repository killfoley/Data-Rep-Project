import mysql.connector
import dbconfig as cfg
from decimal import Decimal

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
        cursor = self.getCursor()
        sql=    ('BEGIN;'
                'Insert into Product (Name, Manufacturer, Supplier, SafetyStock, CurrentStock)'
		        'VALUES (%s, %s, %s, %s, %s);'
                'Insert into Price (CostPrice, SellPrice, ProductId)'
		        'VALUES (%s, %s, last_insert_id());'
                'COMMIT;')
        #values = ("Test", "Test", "Test", 9, 9, 2.50, 3.50)
        
        for result in cursor.execute(sql,values, multi=True):
            pass
        
        self.db.commit()
        cursor.execute("select max(ProdId) from Product;")
        ProdId = cursor.fetchone()
        db.close()
        return ProdId

    # Function for getting all entries from database
    def getAll(self):
        db = self.getConnection()
        cursor = self.getCursor()
        sql="select * from Product A inner join Price B on A.ProdId = B.ProductId"
        cursor.execute(sql)
        db_results = cursor.fetchall()
        # https://stackoverflow.com/questions/40802371/how-to-remove-decimal-from-the-query-result/40802526
        # convert to string items using list comprehension
        results = [tuple(str(item) for item in t) for t in db_results]
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
        sql="select * from Product A inner join Price B on A.ProdId = B.ProductId where A.ProdId = %s;"
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
        values = [product['Name'], product['Manufacturer'], product['Supplier'],
                product['SafetyStock'], product['CurrentStock'], product['CostPrice'],
                product['SellPrice'], product['ProdId']]
        cursor.execute(sql, values)
        self.db.commit()
        db.close()
    
    #Function to delete entries for DB
    def delete(self, id):
        db = self.getConnection()
        cursor = self.db.cursor()
        sql= "delete from Product where ProdId = %s;"
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