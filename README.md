# Annual Leave System Setup

## Running the application locally

Start by cloning the repository from Github from the following link https://github.com/lsblackburn/Annual-Leave-Booker

Then open a terminal in the project directory and install the necessary dependencies using the following command:

`python pip install -r requirements.txt`

From there you will need to setup a mySQL database server. This can be done using Docker and using the command below to create the database:

```docker run --name annual_leave_db -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e MYSQL_DATABASE=annual_leave_db -p 3306:3306 -d mysql:8.0```

Next you will need to run the following command to start a local server, this will also create the database tables in the database:

`python app.py`

It is necessary to populate the application with the Admin user, using the command:

`python admin_seeder.py`

Then you populate the tables with testing data, run the following command:

`python test_seeder.py`
