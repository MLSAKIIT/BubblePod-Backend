# BubblePod-Backend
Backend for BubblePod on Flask

# Usable Functionalities
/bin/data/db.py can create required database successfully
/bin/models/dbsscan.py can run DBSCAN on the test.py succesfully

# Need to be Done
API, Implement Python Package system for each view (page).
Databse I/O from API
WSGI

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