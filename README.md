# Annual Leave Booking System

A web-based application to manage and track annual leave for employees and administrators.

### TL:DR

Clone the repository `git@github.com:lsblackburn/Annual-Leave-Booker.git`

Install the dependencies `python pip install -r requirements.txt`

Setup MySQL database through docker ```docker run --name annual_leave_db -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e MYSQL_DATABASE=annual_leave_db -p 3306:3306 -d mysql:8.0```

Run the command in the project directory `python app.py` to create the database tables and start the local server.

`python admin_seeder.py` will create the initial Admin user

`python test_seeder.py` will create the testing data

## Running the application locally

### Cloning the repository

Github Repository: https://github.com/lsblackburn/Annual-Leave-Booker

Start  by cloning the repository through the following options:

- HTTPS - https://github.com/lsblackburn/Annual-Leave-Booker.git

- SSH - `git@github.com:lsblackburn/Annual-Leave-Booker.git`

- GitHub CLI - `gh repo clone lsblackburn/Annual-Leave-Booker`

### Install the dependencies

Then open a terminal in the project directory and install the necessary dependencies using the following command:

**DISCLAIMER: Ensure Python is installed before running the next command**

`python pip install -r requirements.txt`

### Setting up the MySQL database

From there you will need to setup a mySQL database server. This can be done using Docker and using the command below to create the database:

```docker run --name annual_leave_db -e MYSQL_ALLOW_EMPTY_PASSWORD=true -e MYSQL_DATABASE=annual_leave_db -p 3306:3306 -d mysql:8.0```

### Starting the application locally

The following command will start the application and generate the database tables:

`python app.py`

### Create the initial Admin user

An initial Admin user is required, as the only method of creating an Admin user is through promotion from another Admin. Running the admin seeder using the following command will ensure the Admin is created. The credentials for the Admin can be found in the `admin_seeder.py` file itself.

`python admin_seeder.py`

### Seeding test data

To populate the tables with test users and annual leave entries, run the following command:

`python test_seeder.py`

## Features

### Authentication System

The application is protected through an authentication system which requires a valid login session to access the dashboard and other features.

#### **Registering a user**

When registering for an account, you must fill in the following fields: Name, Email and Password.

- You must not name the user 'Admin'

- You cannot use an email that is already registered to an account

- Your password must be at least 8 characters and include an uppercase letter, a lowercase letter, a number, and a special character.

Once you have successfully created an account you will redirected to the login page.

#### **Logging in**

To login to your account, simply fill in your credentials as specified:

- Email

- Password

This will then forward you to the user dashboard, allowing you to:

- View all upcoming approved annual leave within the next 4 week

- Request annual leave

#### Logging out

The user can also log out of their account, which will redirect the user back to the login page and destroy the session by going to Account in the header and then Sign out.

### Booking Annual Leave

To book annual leave click on the button at the top of the dashboard page with the text **Request Leave**. This will direct you to the page with the form to fill out.

In this form you must fill out the start date of your annual leave, and your end date.

You will be unable to request annual leave where your end date is before your start date. This will result in an error.

#### **Annual Leave Approval/Rejection**

Once annual leave has been requested by a user, admin users can approve or reject the request.

- On rejection, the request is deleted from the database.

- On approval, the request has its state change to **approved** and saved to the database. This is then viewable when users want to view their own annual leave, or on the dashboard when the annual leave is within the next 4 weeks.

#### **Editing Annual Leave**

Once an request has been submitted, regardless of if it is approved users who the request belong to can edit the dates of the leave. However, on updating the dates it will then be submitted for approval again ensuring that users cannot change the dates without approval of admins.

### Admin Specific

Specific functions are only actionable to Admin users, including the approval and rejection of annual leave Annual Leave Approval/Rejection.

Other functionality consist of:

- **Access to the Admin Control Panel** - Only Admins can have access to the control panel which will enable the functionality below.

- **Updating user credentials** - Admins can change the name, email, and password of users.

- **Making another user an Admin** - This can be actioned in the control panel by clicking on the button 'Make Admin'.

- **Revoking Admin status** - An Admin can revoke admin status from another Admin. Except from the main admin account which is created from the `admin_seeder.py` file.

- **Deleting users** - An admin can also delete a user from the database through the control panel. Deleting a user will delete all annual leave requests relating to the user through a on cascade.

### Upcoming future features

Currently this project is in a prototype state which means that is usable in a small scale state. In future releases more advanced pagination and filtering options will be available to ensure future scalability for organisations.