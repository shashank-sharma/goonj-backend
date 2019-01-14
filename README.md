[![Build Status](https://travis-ci.com/shashank-sharma/goonj-backend.svg?token=avBnQmAu2uKCMqEGwpmq&branch=master)](https://travis-ci.com/shashank-sharma/goonj-backend)

# Introduction

Backend for Goonj API using DRF with Django 1.11.6 using PostgreSQL.<br>
Project will be deployed in Digital Ocean server and will be served over there rather than using Heroku. (Note there is no automatic deployment, it will be deployed by me once major updates has been done and tested successfully)

Live version: [Site](http://139.59.37.82/docs/)

### Installation

1. Clone the repository by:<br />
`git clone https://github.com/shashank-sharma/goonj-backend`

2. Create Virtual Environment named as `env` by doing<br />
`python3 -m venv env`

   Now activate it by:<br />
`source env/bin/activate` (Linux)<br>
`myvenv\Scripts\activate` (Windows)

3. Install dependencies<br />
`pip install -r requirements.txt`

3.1. Life is tough, so is Django with Websockets, right now you need to install
redis so that you can use django channels easily. Not sure but docker will also be used.
Install when it will be asked else do redis, that is important

4. Database configuration

   Using psql:<br />
`CREATE ROLE admin WITH LOGIN PASSWORD 'password';`<br />
`create database goonj;`<br />
`GRANT ALL PRIVILEGES ON DATABASE goonj TO admin;`

   databaseurl: postgresql://admin:password@localhost/goonj

5. Set up Virtual Environment values (As mentioned in .env.example)<br />
a. Secret Key: `SECRET_KEY=RANDOMTEXT`<br />
b. Database Url: `DATABASE_URL=<databaseurl>`

6. Migration: <br />
`python manage.py makemigrations`<br />
`python manage.py migrate`


### Documentation

Documentation will be found at:<br>
http://139.59.37.82/docs/
