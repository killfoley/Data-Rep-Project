# file used to test sql functions

from hardwareDAO import HardwareDAO


find_by_id = HardwareDAO.findByID(1)
print(find_by_id)

#get_all = HardwareDAO.getAll()
#print(get_all)

#product = {'Name':'ScrewDriver','Manufacturer':'DeWalt', 'Supplier':'Screwfix', 'SafetyStock':10, 'CurrentStock':25,'CostPrice':4.95, 'SellPrice':6.95,'ProdId':1}

'''
values = [product['Name'], product['Manufacturer'], product['Supplier'],
                product['SafetyStock'], product['CurrentStock'], product['CostPrice'],
                product['SellPrice'], product['ProdId']]
                '''
#HardwareDAO.update(product)


#create_values = ("7mm Drill Bit", "Stanley", "Screwfix", 15, 21, 5.45, 6.99)
#last_row_id = HardwareDAO.create(create_values)
#print(last_row_id)

#delete_by_id = HardwareDAO.delete(4)
#print(delete_by_id)


