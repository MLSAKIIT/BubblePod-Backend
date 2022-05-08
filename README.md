# BubblePod-Backend
Backend for BubblePod on Flask

# Usable Functionalities
DBMS fully functional
Clustering fully functional
API functional

# Need to be Done
API sugar, WSGI

# Setup
Install Postgres 14

On Debian/Ubuntu:
$ sudo apt install postgresql postgresql-contrib postgresql-doc
$ sudo systemctl start postgresql
$ pip install requirements.txt

# Usage
$ sudo -u postgres psql
\password postgres
change password

quit the postgres cli

$ locate pg_hba.conf
change all peer authentication modes to md5

$ sudo systemctl restart postgresql
