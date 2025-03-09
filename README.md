# login information for different types of users. 

| Role  | Username  | Password  |
|--------|--------|--------|
| Admin  | junwen1  | junwen11  |
| Helper  | junwen2  | junwen22  |
| Visitor  | junwen3  | junwen33  |

# short description of the system 

LCC Issue Tracker is a web-based issue tracking system designed to help users manage and track project issues efficiently. Users can log in with different roles (admin, helper, or visitor) to create, update, and monitor issues.
Reporting issues and comments, profile editing, and password updating are three basic features available to all roles.
Admins and helpers have full control over issue management. They can view all issues and manually change their status. Visitors are only allowed to view and comment on their own reported issues.
User management is an advanced feature available only to admins, Admins can manually change the role and activation status of all registered users. 

# Setup Instructions

This guide will help you set up and run the LCC Issue Tracker on your local machine.

## 1）Clone the repository
First, clone the GitHub repository to your local machine:
git clone https://github.com/Junwen-Qiu-1162541/LCC_Issue_Tracker.git
cd LCC_Issue_Tracker

## 2）Install dependencies
Ensure that Python is installed (check with python --version, which should return Python 3.8+).
Then, install the required dependencies:
pip install -r requirements.txt

## 3）Set up the database:
Make sure MySQL is installed and running. Then, create the database and import the required SQL files:
mysql -u <your_mysql_username> -p <your_database_name> < create_database.sql
mysql -u <your_mysql_username> -p <your_database_name> < popular_database.sql

Replace the placeholders:
<your_mysql_username> → Your MySQL username
<your_database_name> → Your MySQL database name

Ensure you run both SQL files:
create_database.sql → Creates the necessary database schema.
popular_database.sql → Populates the database with initial data.

## 4）Create connect.py to connect the database:

Create a file named connect.py in the project folder and add the following code(Database connection settings):

import pymysql


connection = pymysql.connect(
    host="your_database_host",
    user="your_mysql_username",
    password="your_mysql_password",
    database="your_database_name"
)

print("✅ Database connected successfully!")

Replace the placeholders:

"your_database_host" → e.g., localhost or your PythonAnywhere MySQL host
"your_mysql_username" → Your MySQL username
"your_mysql_password" → Your MySQL password
"your_database_name" → Your MySQL database name

To test the connection, run:

python connect.py


## 5）Run application

Once the database is connected, start the application by running:
python app.py


## 6）Open in browser:

Open your browser and go to:

http://localhost:5000





