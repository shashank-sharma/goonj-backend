Introduction

[![Heroku](http://heroku-badges.herokuapp.com/?app=acro-elibrary&style=flat)](http://goonj-api.herokuapp.com/)
[![Build Status](https://travis-ci.com/shashank-sharma/goonj-backend.svg?token=avBnQmAu2uKCMqEGwpmq&branch=master)](https://travis-ci.com/shashank-sharma/goonj-backend)

Backend for Goonj API using DRF with Django 1.11 using PostgreSQL.

Live version: [Site](http://goonj-api.herokuapp.com)

### Getting Started

1. Clone

2. Create Virtual Environments

3. Install dependencies

`pip install -r requirements.txt`

4. Database configuration

Using psql:

`CREATE ROLE admin WITH LOGIN PASSWORD 'password';`

`create database goonj;`

`GRANT ALL PRIVILEGES ON DATABASE goonj TO admin;`

databaseurl: postgresql://admin:password@localhost/goonj

5. Set up Virtual Environment values

a. Secret Key: `SECRET_KEY=RANDOMTEXT`

b. Database Url: `DATABASE_URL=<databaseurl>`

6. Migration

`python manage.py makemigrations`

`python manage.py migrate`


You have done it
