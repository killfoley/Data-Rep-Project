# Data Representation 2021
# Creating and Consuming RESTful APIs
## Project Description
This repository contains all the files required to run a web application which can access a database and perform CRUD operations. The server `application.py` for the API is created using Flask a module in Python. <br>
The project is an example of an inventory managment system for a simple hardware store for exampe. The web application can access the database and it can create update and delete Products. 

## Installation
* First clone the repository locally

### Setting up the datbase
* Start the MYSQL command line
* Run command 
```mysql
mysql> use datarepproject;
```
* Next initiate the database by running 
```mysql
mysql> source /path/to/file/init.sql;
```
* Note the path to the file must be correct. If there are too many escape characters it might fail so it might be best to move the file to the desktop if there are any issues

### Setting Up A Virtual Environment
* Using a virtual environment is a good idea so as not to disrupt your current system configuration.
* To do this run `pip install virtualenv` virtualenv package will download
* Navigate to the folder directory in terminal and run `virtualenv venv`
* To activate the virtual environment run `source venv/bin/activate`
* Therei s a file called requirements.txt which contains everything required to run the project.
* Install this in the venv by running `pip install -r requirements.txt`
* All the required packages should now be installed in the venv.
* You can run `pip freeze` to confirm.
* Run the command `deactivate` when you are finished with your venv

### Running the server
  On Linux or Mac, run the following commands:
  ```bash
  export FLASK_APP=app.py
  python3 -m flask run
  ```
  On Windows run the following commands:
  ```bash
  set FLASK_APP=app.py
  python -m flask run
  ```
Keep the virtual environment running. You can terminate the server using control+c.

### Test The Server
On a new terminal window  test the connection by checking the http responses with Curl. The main app routes have authentication so there is a basic stockcheck app route at the below address

```bash
curl http://localhost:5000/stockcheck
```
### Run The Web App
* To run the web app open a browser and enter http://localhost:5000/login.
Use the credentials 
```
username: admin
password: admin
```
And follow through the various sites.

## PythonAnywhere
The web application is also hosted on Pythonanywhere. It can be accessed at [pythonanywhere](https://killfoley.pythonanywhere.com/login)
or via curl
```bash
curl https://killfoley.pythonanywhere.com/stockcheck
```
###### Submitted for marking by
Killian Foley<br>
G00387875<br>
<G00387875@GMIT.ie>