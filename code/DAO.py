import mysql.connector
# import dbconfig as cfg

# Create a Database Access Object Class
class HardwareDAO:
    db=""
    # Initiate the connection
    def __init__(self): 
        self.db = mysql.connector.connect(
        host=       cfg.mysql['host'],
        user=       cfg.mysql['user'],
        password=   cfg.mysql['password'],
        database=   cfg.mysql['database']
        )
    
    # Create function for creating entries        
    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into BLANK (title,author, price) values (%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    # Function for getting all entries from database
    def getAll(self):
        cursor = self.db.cursor()
        sql="select * from BLANK"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        return returnArray

    # Function to search by Product ID
    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select * from BLANK where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    # Function to update existing entries
    def update(self, values):
        cursor = self.db.cursor()
        sql="update BLANK set title= %s,author=%s, price=%s  where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
    
    #Function to delete entries for DB
    def delete(self, id):
        cursor = self.db.cursor()
        sql="delete from BLANK where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    # Function to convert SQL array to Python dict
    def convertToDictionary(self, result):
        colnames=['id','Title','Author', "Price"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
HardwareDAO = HardwareDAO()