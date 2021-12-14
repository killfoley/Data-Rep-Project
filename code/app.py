#!flask/bin/python

from flask import Flask, g, jsonify, request, abort, make_response, render_template, session, redirect, url_for
from DAO import HardwareDAO
# import json


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

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

'''

# ---- read ----

@app.route('/equipment')
def getAll():
    # session['username'] = "I dunno"
    if not 'username' in session:
        abort(401)

    results = HardwareDAO.getAll()
    return jsonify(results)


@app.route('/equipment/<int:id>')
def findById(id):
    if not 'username' in session:
        abort(401)

    foundEquipment = HardwareDAO.findByID(id)

    # Check if id exists
    if not foundEquipment:
        return "That id has not been found in the equipment database."
        abort(404)

    return jsonify(foundEquipment)


# ---- create ----

@app.route('/equipment', methods=['POST'])
def create():
    if not 'username' in session:
        abort(401)

    # check if exist
    if not request.json:
        return "Wrong request"
        abort(400)
    # if not 'id' in request.json:
    #     return "Wrong request (id)"
    #     abort(400)

    equip = {
        "category": request.json['category'],
        "name": request.json['name'],
        "supplier": request.json['supplier'],
        "price_eur": request.json['price_eur']
    }
    # Make the tuple for DB
    values = (equip['category'], equip['name'],
              equip['supplier'], equip['price_eur'])
    newId = HardwareDAO.create(values)
    equip['id'] = newId
    return jsonify(equip)


# sample test
# curl -i -H "Content-Type:application/json" -X POST -d '{"category":"Tier 2","name":"Elwirka","supplier":"Elwro","price_eur":30000.00}' http://localhost:5000/equipment
# for windows use this one
# curl -i -H "Content-Type:application/json" -X POST -d "{\"category\":\"Tier 2\",\"name\":\"Elwirka\",\"supplier\":\"Elwro\",\"price_eur\":30000.00}" http://localhost:5000/equipment

# ---- update ----

@app.route('/equipment/<int:id>', methods=['PUT'])
def update(id):
    if not 'username' in session:
        abort(401)

    foundEquipment = HardwareDAO.findByID(id)

    if not foundEquipment:
        return "That id does not exist in the database"
        abort(404)
    if not request.json:
        return "Wrong request"
        abort(400)

    reqJson = request.json

    # checks for data integrity
    if ('price_eur' in reqJson) and (type(reqJson['price_eur']) is not float):
        abort(400)
        return "Wrong request or data type (should be float)"

    if 'category' in request.json:
        foundEquipment['category'] = reqJson['category']
    if 'name' in request.json:
        foundEquipment['name'] = reqJson['name']
    if 'supplier' in request.json:
        foundEquipment['supplier'] = reqJson['supplier']
    if 'price_eur' in request.json:
        foundEquipment['price_eur'] = reqJson['price_eur']

    # Make the tuple for DB
    values = (foundEquipment['category'], foundEquipment['name'],
              foundEquipment['supplier'], foundEquipment['price_eur'], foundEquipment['id'])
    # Do the update on DB
    HardwareDAO.update(values)

    return jsonify(foundEquipment)

# for Linux
# curl -i -H "Content-Type:application/json" -X PUT -d '{"name":"Odra"}' http://localhost:5000/equipment/5
# for Windows use this one
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"Odra\"}" http://localhost:5000/equipment/5


# ---- delete ----

@app.route('/equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    if not 'username' in session:
        abort(401)

    foundEquipment = HardwareDAO.findByID(id)
    if not foundEquipment:
        return "That id does not exist in the database"
        abort(404)
    HardwareDAO.delete(id)
    return jsonify({"done": True})


# --------------------------------
# Getting static pages
# --------------------------------

@app.route('/about')
def about():
    # return "inside about()1" # test ok
    # if not 'username' in session:
    #     return render_template('index.html')

    return render_template('about.html')


# --------------------------------
# Error handling with Flask routes
# --------------------------------

@app.errorhandler(404)
def not_found404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found400(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


# ------------------
# Check dependencies
# ------------------

if __name__ == '__main__':
    app.run(debug=False) # set for production
    '''