#Overview#

This API represents a simple e-commerce backend that allow to
manage products, it only created as sample backend using Python 2.7 - Django 1.9.7 and Django Rest Framework 3.3.3

##Setup the Development Environment##

1- Clone the repository

`$ git clone https://github.com/hshafy/ecomapi.git`

`$ cd ecomapi`

2- Create and activate virtual environment

`$ virtualenv env`

`$ source env/bin/activate`

3- Install dependencies

`$ pip install -r requirements.txt`

4- Create Database

`cd src`

`$ python manage.py migrate`

4- Run local server

`$ python manage.py runserver`

##Run Tests##

`$ cd src`

`$ python manage.py test`

##Current Version##

Current api version is: v1

##Schema##

All data is sent and received as JSON.

`curl -i -H 'Accept: application/json; indent=4' -X GET http://127.0.0.1:8000/v1/productgroups/`

* HTTP/1.0 200 OK
* Date: Tue, 05 Jul 2016 19:38:53 GMT
* Server: WSGIServer/0.1 Python/2.7.6
* Vary: Accept, Cookie
* X-Frame-Options: SAMEORIGIN
* ETAG: 2900678b863baba75963abb752a85525
* Content-Type: application/json; indent=4
* Allow: GET, POST, HEAD, OPTIONS


##Root Endpoint##
You can issue a `GET` request to the root endpoint to get all the endpoints that the API supports:

`curl -H 'Accept: application/json; indent=4' -X GET http://127.0.0.1:8000/`

##HTTP Verbs##

* GET    --> retrieving resources.
* POST   --> creating resources.
* PATCH  --> Partial updates.
* PUT    --> replacing resources.
* DELETE --> deleting resources.

##Authentication##

No authentication applied, all resources are public.

##Conditional requests##

Most responses return an ETag header. You can use the values of these headers to make subsequent requests to those resources using the If-None-Match. If the resource has not changed, the server will return a 304 Not Modified.

##Usage and Data types##

For usage and valid data types please check test cases.
