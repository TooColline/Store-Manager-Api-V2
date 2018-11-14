# Store-Manager-Api-V2

[![Build Status](https://travis-ci.com/TooColline/Store-Manager-Api-V2.svg?branch=develop)](https://travis-ci.com/TooColline/Store-Manager-Api-V2) [![Coverage Status](https://coveralls.io/repos/github/TooColline/Store-Manager-Api-V2/badge.svg?branch=develop)](https://coveralls.io/github/TooColline/Store-Manager-Api-V2?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/96abc75160af4cdfc65c/maintainability)](https://codeclimate.com/github/TooColline/Store-Manager-Api-V2/maintainability)

## Project Overview
Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store. This repository contains the API endpoints for the application and has data persisted using a database.

### Endpoints

#### Auth Endpoints
Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v2/auth/signup` | Create a new user
POST | `/api/v2/auth/login` | Login a registered user
POST | `/api/v2/auth/logout` | Logout a logged in user

#### Admin Endpoints
Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v2/products` | Add a new product
GET | `/api/v2/products` | Get all products
GET | `/api/v2/products/<int:product_id>` | Get specific product
GET | `/api/v2/sales` | Get all sale orders
GET | `/api/v2/sales/<int:sale_id>` | Get specific sale order
PUT | `/api/v2/products/<int:product_id>` | Update specific product fields
DELETE | `/api/v2/products/<int:product_id>` | Delete specific product

#### Store Attendant Endpoints
Method | Endpoint | Functionality
--- | --- | ---
GET | `/api/v2/products` | Get all products
GET | `/api/v2/products/<int:product_id>` | Get specific product
POST | `/api/v2/sales` | Add sale order

### Installing the application
1. Clone repo using `https://github.com/TooColline/Store-Manager-Api-V2.git`
2. `cd Store-Manager-Api-V2`
3. Create a virtual environment `virtualenv venv` and activate it `source venv/bin/activate` 
4. Install dependencies of the application using `pip3 install -r requirements.txt`
5. Export these environment variables ```export FLASK_APP="run.py"``` for your app and ```export JWT_SECRET_KEY=yourkey```
6. Run the application `python3 run.py` or `flask run`

### Tests
Run this command inside your virtual environment: `coverage run --source=app.api.v2.views -m pytest /tests/v2 -v -W error::UserWarning && coverage report`

#### Technologies used
1. Python flask framework
2. `pytest` for running tests
3. `flask JWT` for auth
4. `pylint` for python linting library

## Credits
This was challenge 3 as part of the Bootcamp 33 NBO Andela.

## Author
[Too Collins](https://github.com/TooColline)

## Documentation
[API End points documentation](https://documenter.getpostman.com/view/5601454/RzZ4q25y)

## Deployment
[Heroku](https://a-store-manager-app-api-v2.herokuapp.com/)
