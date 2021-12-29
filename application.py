#!flask/bin/python

from flask import Flask, g, jsonify, request, abort, make_response, render_template, session, redirect, url_for
from flask_cors import CORS
from static.hardwareDAO import HardwareDAO
import json
from decimal import Decimal

#https://stackoverflow.com/questions/63278737/object-of-type-decimal-is-not-json-serializable
# convert python 'Decimal' format for output in json. call with json.dumps()

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

# initiate the Flask server
app = Flask(__name__, static_url_path='', template_folder='staticpages', static_folder='staticpages')
CORS(app)
# unsort json. Remove for using with browser.
# app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'secret_key'

# How to create a simple Flask login @ https://youtu.be/2Zz97NVbH0U
# Storing credentials in the server. Would normally use a database table

# Create a user class
class User:
    def __init__(self,id, username, password):
        self.id = id
        self.username = username
        self.password = password

    # Return username to the command line for checking
    def __repr__(self):
        return f'<User: {self.username}>'

# Create the users list. Append users to it
users = []
users.append(User(id=1, username='admin', password='admin'))
users.append(User(id=2, username='user1', password='password1'))
users.append(User(id=3, username='user2', password='password2'))

# check before_request app route
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))

        return redirect(url_for('login'))

    return render_template('login.html')

# app route for home page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('home.html')

# app route for logout
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))

# get all stock entries
# curl http://127.0.0.1:5000/inventory
@app.route('/inventory')
def getAll():
    if not 'user_id' in session:
        abort(401)

    results = HardwareDAO.getAll()
    return jsonify(results)


# find by Id
# curl http://localhost:5000/inventory/3
@app.route('/inventory/<int:id>')
def findById(id):
    if not 'user_id' in session:
        abort(401)

    stockResult = HardwareDAO.findByID(id)

    # Check if id exists
    if not stockResult:
        return "Cannot find that product in the database\n"
        abort(404)
    stockResult = json.dumps(stockResult, cls=DecimalEncoder)
    return json.loads(stockResult)


# Create new stock item
# for Mac
# curl -i -H "Content-Type:application/json" -X POST -d '{"name":"Pliers 3 piece","manufacturer":"Magnusson","supplier":"Screwfix","safetystock":5, "currentstock":8, "costprice":12.50, "sellprice":16.45}' http://localhost:5000/inventory
# for Windows
# curl -i -H "Content-Type:application/json" -X POST -d "{\"name\":\"Pliers 3 piece\",\"manufacturer\":\"Magnusson\",\"supplier\":\"Screwfix\",\"safetystock\":5, \"currentstock\":8, \"costprice\":12.50, \"sellprice\":16.45}" http://localhost:5000/inventory
@app.route('/inventory', methods=['POST'])
def create():
    if not 'user_id' in session:
        abort(401)

    # check if exists
    if not request.json:
        return "Wrong request\n"
        abort(400)

    product = {
        "name": request.json['name'],
        "manufacturer": request.json['manufacturer'],
        "supplier": request.json['supplier'],
        "safetystock": request.json['safetystock'],
        "currentstock": request.json['currentstock'],
        "costprice" : request.json['costprice'],
        "sellprice" : request.json['sellprice']
    }
    # create values for insert into db
    values = (product['name'], product['manufacturer'],
              product['supplier'], product['safetystock'], 
              product['currentstock'],product['costprice'],
              product['sellprice'])
    newId = HardwareDAO.create(values)
    product['ProdId'] = newId
    return jsonify(product)


# App to update a stock item
# for Mac
# curl -i -H "Content-Type:application/json" -X PUT -d '{"name":"M8x25mm countersunk screw 50 pack","manufacturer":"Easyfix","supplier":"Screwfix","safetystock":50, "currentstock":80, "costprice":6.00, "sellprice":8.95, "ProdId":4}' http://localhost:5000/inventory/4
# for Windows
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"M8x25mm countersunk screw 50 pack\",\"manufacturer\":\"Easyfix\",\"supplier\":\"Screwfix\",\"safetystock\":50, \"currentstock\":80, \"costprice\":6.00, \"sellprice\":8.95, \"ProdId\":4}" http://localhost:5000/inventory/4
@app.route('/inventory/<int:id>', methods=['PUT'])
def update(id):
    if not 'user_id' in session:
        abort(401)

    returnedProduct = HardwareDAO.findByID(id)
    # Convert to string object to get rid of Python Decimal object
    returnedProduct = json.dumps(returnedProduct, cls=DecimalEncoder)
    # Convert back to JSON
    returnedProduct = json.loads(returnedProduct)

    if not returnedProduct:
        return "That id does not exist in the database\n"
        abort(404)
    
    if not request.json:
        return "Request Error\n"
        abort(400)

    reqJson = request.json

    # checks for data integrity
    if ('costprice' in reqJson) and (type(reqJson['costprice']) is not float):
        abort(400)
        return "Data type is incorrect. Please provide decimal value for price\n"
    if ('sellprice' in reqJson) and (type(reqJson['sellprice']) is not float):
        abort(400)
        return "Data type is incorrect. Please provide decimal value for price\n"

    if 'name' in request.json:
        returnedProduct['Name'] = reqJson['name']
    if 'manufacturer' in request.json:
        returnedProduct['Manufacturer'] = reqJson['manufacturer']
    if 'supplier' in request.json:
        returnedProduct['Supplier'] = reqJson['supplier']
    if 'safety_stock' in request.json:
        returnedProduct['SafetyStock'] = reqJson['safety_stock']
    if 'CurrentStock' in request.json:
        returnedProduct['CurrentStock'] = reqJson['CurrentStock']

    # Make the tuple for DB
    values = (returnedProduct["Name"],returnedProduct["Manufacturer"],
              returnedProduct["Supplier"], returnedProduct["SafetyStock"], 
              returnedProduct["CurrentStock"],returnedProduct["CostPrice"],
              returnedProduct["SellPrice"], returnedProduct["ProdId"])
    # Do the update on DB
    HardwareDAO.update(values)

    return jsonify(returnedProduct)

# Delete
# curl -
@app.route('/inventory/<int:id>', methods=['DELETE'])
def deleteStockItem(id):
    if not 'user_id' in session:
        abort(401)

    returnedProduct = HardwareDAO.findByID(id)
    if not returnedProduct:
        return "That id does not exist in the database\n"
        abort(404)
    HardwareDAO.delete(id)
    return jsonify({"done": True})


# Getting static pages
@app.route('/about')
def about():
    return render_template('about.html')


# Error handling 

@app.errorhandler(404)
def not_found404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found400(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=True) # set for testing