# chopin-liszt
¸¸.•*¨*•♫♪¸¸.•*¨*•♫♪¸¸.•*¨*•♫♪¸¸.•*¨*•♫♪¸¸.•*¨*•♫♪¸¸.•*¨*•♫♪¸¸.•*¨*•♫♪

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/nelsontran/chopin-liszt
cd chopin-liszt/
```

### Install System Dependencies

Install [Python 3](https://www.python.org/) and [MySQL Server](https://www.mysql.com/).

```bash
sudo apt-get install python3 mysql-client mysql-server libmysqlclient-dev
```

### Install Python Dependencies

Install [Flask](http://flask.pocoo.org/), [SQLAlchemy](http://www.sqlalchemy.org/), and [PyMySQL](https://github.com/PyMySQL/PyMySQL).

```bash
pip3 install flask flask-sqlalchemy pymysql
```

### Configure MySQL

Connect to your MySQL server and create a database.

```bash
mysql -h localhost -P 3306 -u username -p

> CREATE DATABASE chopin-liszt;
> exit
```

Edit `./app/config.json` with the credentials to the database that you have just created.

Setup the database tables by navigating into the `app/` directory and executing the following Python code.

```python
python3

>>> from core.database import init_db
>>> init_db()
>>> exit()
```

### Run the Application

```bash
python3 __init__.py
```

In your browser, navigate to `localhost:5000`.
