# Closure() #
[![CodeFactor](https://www.codefactor.io/repository/github/scdor/closure/badge)](https://www.codefactor.io/repository/github/scdor/closure)
![Backend CI](https://github.com/ScDor/Closure/actions/workflows/backend.yml/badge.svg?branch=master)
![Backend CI](https://github.com/ScDor/Closure/actions/workflows/frontend.yml/badge.svg?branch=master)

Planning your next courses easily.

## About ##

This project is part of
the [Open Source Software Workshop](https://shnaton.huji.ac.il/index.php/NewSyl/67118/2/) at
the Hebrew University of Jerusalem.


## Table of Contents

- [Setting up django](#instructions)
- [Polulating the DB](#HUJIex)
- [Authenticating](#generatingAuth)
- [API Usage](#usetheapi)
- [Contributions](#contribute)


<a name="instructions"/>

## Getting Started with local development ##

1. Clone this repo.
2. Run `python3 -m venv venv` to install a new Python virtual environment.
3. Activate the virtual environment so your commands will be executed inside a virtual environment: 
    - Windows: run `venv\Scripts\activate.bat`. 
    - Mac OS/Linux: run `source venv/bin/activate`. <br> 
4.  Run `pip install --upgrade pip` 
5. Run `pip install -r requirements.txt` to install the project's dependencies.
6. Run `python Closure_Project/manage.py makemigrations rest_api`
7. Run `python Closure_Project/manage.py migrate`
8. On PyCharm, right-click the outer `Closure_Project` directory, choose `Mark Directory as` and click `Sources Root` _(its icon will be colored cyan afterwards)_.
9. Start the Django server with `python Closure_Project/manage.py runserver`

You now have a django instance with the database configured (yet blank).

The next step would be populating the database with `Course` information, so the whole ordeal
can work.

See the `Parser` folder, or read the following subsection to learn more about the data
structures used.

<a name="HUJIex"/>

#### Loading data offline ####

Upon migrating the database, a data dump containing all parsed course and track data will be
downloaded from the internet and inserted into the database.

<a name="generatingAuth"/>

### Generating auth ###
1. If you don't have admin superuser, creat one with `python Closure_Project/manage.py createsuperuser`
2. Use basic authentication with your username and password created, or generate token with `python Closure_Project/manage.py drf_create_token` and add `{Autharization: Token <key>}` to request headers.

<a name="usetheapi"/>

### Using the API ###
- To use the API, start the server with `python Closure_Project/manage.py runserver`.

- The base API url is `https://<host>/api/v1`.
- API documentation is available in `https://<host>/redoc/`
- Try to use API with: `https://<host>/swagger/`
- When making real requests, always remember to add the Authorization header to the request.

<a name="contribute"/>

## Contributions ##

Feel free to PR or open issues.
