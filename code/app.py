#!flask/bin/python

from flask import Flask, g, jsonify, request, abort, make_response, render_template, session, redirect, url_for
from DAO import HardwareDAO
import json


# initiate the Flask server
app = Flask(__name__, static_url_path='', static_folder='.')
app.secret_key = 'MySeCrEtKeY987123'

# How to create a simple Flask login @ https://youtu.be/2Zz97NVbH0U
# Storing credentials in the server. Would normally use a database table

# Create a user class
class User:
    def __init__(self, id, username, password):
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

# Used for sessions
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

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('home.html')

# get all stock entries
@app.route('/stockitem')
def getAll():
    if not 'username' in session:
        abort(401)

    results = HardwareDAO.getAll()
    return jsonify(results)

# find by Id
@app.route('/stockitem/<int:id>')
def findById(id):
    if not 'username' in session:
        abort(401)

    stockResult = HardwareDAO.findByID(id)

    # Check if id exists
    if not stockResult:
        return "Cannot find that product in the database"
        abort(404)

    return jsonify(stockResult)

# Create new stock item
@app.route('/stockitem', methods=['POST'])
def create():
    if not 'username' in session:
        abort(401)

    # check if exist
    if not request.json:
        return "Wrong request"
        abort(400)

    product = {
        "Name": request.json['name'],
        "Manufacturer": request.json['manufacturer'],
        "Supplier": request.json['supplier'],
        "SafetyStock": request.json['safety_stock'],
        "CurrentStock": request.json['current_stock'],
        "CostPrice" : request.json['cost_price'],
        "SellPrice" : request.json['sell_price']
    }
    # create values for insert into db
    values = (product['name'], product['manufacturer'],
              product['supplier'], product['price_eur'], 
              product['current_stock'],product['cost_price'],
              product['sell_price'])
    newId = HardwareDAO.create(values)
    product['id'] = newId
    return jsonify(product)


# sample test
# curl -i -H "Content-Type:application/json" -X POST -d '{"name":"Tier 2","name":"Elwirka","supplier":"Elwro","price_eur":30000.00}' http://localhost:5000/stockitem
# for windows use this one
# curl -i -H "Content-Type:application/json" -X POST -d "{\"category\":\"Tier 2\",\"name\":\"Elwirka\",\"supplier\":\"Elwro\",\"price_eur\":30000.00}" http://localhost:5000/stockitem

# App to update a stock item
@app.route('/stockitem/<int:id>', methods=['PUT'])
def update(id):
    if not 'username' in session:
        abort(401)

    returnedProduct = HardwareDAO.findByID(id)

    if not returnedProduct:
        return "That id does not exist in the database"
        abort(404)
    if not request.json:
        return "Request Error"
        abort(400)

    reqJson = request.json

    # checks for data integrity
    if ('cost_price' in reqJson) and (type(reqJson['cost_price']) is not float):
        abort(400)
        return "Data type is incorrect. Please provide decimal value for price"
    if ('sell_price' in reqJson) and (type(reqJson['sell_price']) is not float):
        abort(400)
        return "Data type is incorrect. Please provide decimal value for price"

    if 'name' in request.json:
        returnedProduct['name'] = reqJson['name']
    if 'manufacture' in request.json:
        returnedProduct['manufacturer'] = reqJson['manufacturer']
    if 'supplier' in request.json:
        returnedProduct['supplier'] = reqJson['supplier']
    if 'safety_stock' in request.json:
        returnedProduct['safety_stock'] = reqJson['safety_stock']
    if 'current_stock' in request.json:
        returnedProduct['current_stock'] = reqJson['current_stock']
    

    # Make the tuple for DB
    values = (returnedProduct['name'], returnedProduct['manufacturer'],
              returnedProduct['supplier'], returnedProduct['price_eur'], 
              returnedProduct['current_stock'],returnedProduct['cost_price'],
              returnedProduct['sell_price'])
    # Do the update on DB
    HardwareDAO.update(values)

    return jsonify(returnedProduct)

# for Linux
# curl -i -H "Content-Type:application/json" -X PUT -d '{"name":"Odra"}' http://localhost:5000/product/5
# for Windows use this one
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"Odra\"}" http://localhost:5000/productm/5


# ---- delete ----

@app.route('/stockitem/<int:id>', methods=['DELETE'])
def deleteStockItem(id):
    if not 'username' in session:
        abort(401)

    returnedProduct = HardwareDAO.findByID(id)
    if not returnedProduct:
        return "That id does not exist in the database"
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
    app.run(debug=False) # set for production