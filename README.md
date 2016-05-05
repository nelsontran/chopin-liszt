# LilyTask

LilyTask is a project created for the Database Management class at Arizona State University. The goal of the project was to implement a database system application and demonstrate that we understand how to:

- Create a conceptual database design using entity-relationship modeling.
- Convert the entity-relationship model into a relational schema.
- Normalize the relational schema to reduce redundancy.
- Write SQL commands to perform CRUD operations on the database.
- Integrate our database system into a web application.

A running instance of this project is being hosted at [lily.ntt.io](http://lily.ntt.io).

# Table of Contents

- [LilyTask](#lilytask)
- [Table of Contents](#table-of-contents)
- [Setup Instructions](#setup-instructions)
	- [Clone the Repository](#clone-the-repository)
	- [Install System Dependencies](#install-system-dependencies)
	- [Install Python Dependencies](#install-python-dependencies)
	- [Configure MySQL](#configure-mysql)
	- [Run the Application](#run-the-application)
- [Deploying to a LAMP stack](#deploying-to-a-lamp-stack)
	- [Install and Enable `mod_wsgi`](#install-and-enable-mod_wsgi)
	- [Set up a Virtual Environment](#set-up-a-virtual-environment)
	- [Run the Deploy Script](#run-the-deploy-script)

# Setup Instructions

## Clone the Repository

```bash
git clone https://github.com/nelsontran/ser322-lilytask
cd ser322-lilytask/
```

## Install System Dependencies

Install [Python 3](https://www.python.org/) and [MySQL Server](https://www.mysql.com/).

```bash
sudo apt-get install python3 mysql-client mysql-server libmysqlclient-dev
```

## Install Python Dependencies

Install [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), and [PyMySQL](https://github.com/PyMySQL/PyMySQL).

```bash
sudo pip3 install flask flask-sqlalchemy flask-login pymysql
```

## Configure MySQL

Connect to your MySQL server and create a database.

```bash
mysql -h localhost -P 3306 -u username -p

> CREATE DATABASE lilytask;
> exit
```

Edit `config.json` with the credentials to the database that you have just created.

Setup the database tables by executing the following Python code.

```python
python3

>>> from app.database import init_db
>>> init_db()
>>> exit()
```

## Run the Application

```bash
python3 run_server.py
```

In your browser, navigate to `localhost:5000`.

# Deploying to a LAMP stack

You need to have a LAMP (Linux, Apache, MySQL, and Python) stack installed on your server.

## Install and Enable `mod_wsgi`

WSGI (Web Server Gateway Interface) is a specification for interface between web servers and web applications for Python. Install the `mod_wsgi` Apache HTTP server mod that allows Apache to serve Flask applications.

```bash
sudo apt-get install libapache2-mod-wsgi python-dev
```

Enable `mod_wsgi`.

```bash
sudo a2enmod wsgi
```

## Set up a Virtual Environment

`virtualenv` is a tool that will create sandboxed Python execution environments. This will keep the application dependencies separated from the main system.

It can be installed using `pip`.

```bash
sudo pip3 install virtualenv
```

Create the virtual environment and activate it. `venv` is the name of the virtual environment that will be created.

```bash
virtualenv venv
source venv/bin/activate
```

Next, install the Python dependencies listed in [Install Python Dependencies](#install-python-dependencies) while inside the virtual environment. When finished, deactivate the virtual environment with:

```bash
deactivate
```

## Run the Deploy Script

Navigate to the `deploy/` directory and edit the variables at the top of `deploy.sh`. Do **not** include a trailing `/` at the end of the path names.

- `VENV_DIR` is the absolute path to the directory of the virtual environment created.
- `INSTALL_DIR` is the absolute path to the directory where you want the application to be installed to.
- `SERVER_NAME` is the domain name that the application will be served to.
- `SECRET_KEY` is the key used to sign user session cookies. Keep this really secret.

Save and run the script to deploy the application. This will install `lilytask` to the specified deployment directory and configure the Apache server to run the application.

```bash
sudo bash deploy.sh
```

**Warning:** *This will remove everything in `INSTALL_DIR` if it exists. Double check that the variable values are correct before running the script.*
