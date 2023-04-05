# Project to manage Helsinki Bike Trips

Welcome to the project! This project is made with Django and includes a MySQL database.

The project was made based on Solita company exercise made for [Dev Academy pre-assignment](https://github.com/solita/dev-academy-2023-exercise)

The project contains 2 apps (the API app which uses djangorestframework, and the front end app)

## Dependencies

To run this project, you need to install the following dependencies:

- Python 3.7 or higher
- Django 3.2.18 or higher
- MySQL 5.7 or higher
- mysqlclient

You can install other dependencies using pip. Run the following command in your terminal:

```Bash
pip install -r requirements.txt
```


## Creating the database and connecting to it

Create a new database by running the following command:

```Bash
mysql -u <username> -p -e "CREATE DATABASE <database_name>"
```

Replace `<username>` with your MySQL username and `<database_name>` with the name of the database you want to create.

Rename the file `.env.example` to `.env` and replace `<your_mysql_password>` with your database password 


## Set the server URL

If you are running the project using django built-in web server, you do not need to update anything
Otherwise, open `frontend/constrants.py` and change the following `SERVER_URL` to your own server address

```Python
SERVER_URL = 'http://127.0.0.1:8000/'
```



## Loading the data





## Running the Project

To run the project, follow these steps:

1. Open your terminal and navigate to the project directory.
2. Activate your virtual environment if you are using one.
3. Run the following command to start the development server:

```Bash
python manage.py runserver
```

4. Open a web browser and navigate to the URL shown in the terminal output.



## Loading the data

1. In a web browser open the following link to load the stations to database

   `http://127.0.0.1:8000/api/import_stations/`

2. And open the following link to load trips
   `http://127.0.0.1:8000/api/import_trips/`

   NOTE: 1. Loading trips will take several minutes as there are more than 2 millions of record
         2. Also, please ignore the warnings
         3. If you are not using the django build-in server, consider changing the server in the URL


3. If you want to check only sample of data, use the following endpoint instead
   `http://127.0.0.1:8000/api/import_sample_trips/`


## Using the app

After starting the server use the server URL in the browser and navigate between menu links

That's it! You should now be able to view and interact with the project.