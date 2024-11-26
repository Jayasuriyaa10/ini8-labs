# CRUD Operations Using Flask and MySQL

This is a simple web application built using Flask that allows users to perform CRUD (Create, Read, Update, Delete) operations on a database of registrations.

## Prerequisites

- Python (version 3.6 or higher).
- Flask (install via `pip install Flask`).
- MySQL database server.

## Installation

- `git clone https://github.com/Jayasuriyaa10/ini8-labs.git`
    
- `cd IniLAbs`

Now install Flask and MySQL connector using:
   - `pip install Flask`
   - `pip install mysql-connector-python`

Create a database and Create a new table with given query below:
    `create table registration(
        id int primary key auto_increment, 
        name varchar(255) not null, 
        email varchar(255) not null, 
        DOB date, 
        contactnum varchar(255) unique
    )`

Now update the database connection details in app.py file

After updating, run the webapp using the command 
    `python app.py` in the terminal.

Access the application in your web browser at http://localhost:5000.

## Features
- Create Entry: Allows users to create a new registration entry by providing name, email, date of birth, and contact number.
- View Entries: Displays a table of all existing registration entries.
- Update Entry: Enables users to update existing registration entries by providing the entry ID and modifying the details.
- Delete Entry: Allows users to delete existing registration entries by providing the entry ID.

## Error Handling
- Email Validation: Ensures that a valid email address is provided during registration.
- Phone Number Validation: Validates that the phone number, if provided, is a 10-digit number.
- Date of Birth Validation: Verifies that the date of birth is in the past.

## Framework Implementation
- Flask: Utilizes the Flask micro-framework for handling HTTP requests, routing, and rendering HTML templates.
- MySQL: Integrates with MySQL database for storing and managing registration data.

if you have any questions or encounter any problems, please let me know. Thanks!
