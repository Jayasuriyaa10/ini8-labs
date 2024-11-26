from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
app = Flask(__name__)
import re
import datetime
import hashlib
import os

app.secret_key = os.urandom(24)

mysql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jaiprasanth", # Change the Mysql connection details
    database="regs"
)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        dob = request.form['DateOfBirth']
        phone = request.form.get('PhoneNumber', '') 

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            error_msg = "Invalid email address. Please enter a valid email address."
            return render_template('error.html', error_msg=error_msg)

        if phone and not re.match(r'^\d{10}$', phone): 
            error_msg = "Invalid phone number. Please enter a 10-digit phone number."
            return render_template('error.html', error_msg=error_msg)


        today = datetime.date.today()
        dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
        if dob_date > today:
            error_msg = "Invalid Date of Birth. Please enter a date in the past."
            return render_template('error.html', error_msg=error_msg)

        cursor = mysql_connection.cursor()
        cursor.execute("INSERT INTO Registration (Name, Email, Dob, Contactnum) VALUES (%s, %s, %s, %s)", (name, email, dob, phone))
        mysql_connection.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        last_insert_id = cursor.fetchone()[0]
        cursor.close()

        return redirect(url_for('success', id=last_insert_id))
    else:
        return render_template('create.html')

@app.route('/success/<int:id>')
def success(id):
    return render_template('success.html', id=id)

@app.route('/view')
def view_entries():
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT * FROM Registration")
    entries = cursor.fetchall()
    cursor.close()
    return render_template('view.html', entries=entries)

@app.route('/update', methods=['GET', 'POST'])
def update_entry():
    if request.method == 'POST':
        entry_id = request.form['ID']
        name = request.form['Name']
        email = request.form['Email']
        dob = request.form['DateOfBirth']
        phone = request.form.get('PhoneNumber', '')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            error_msg = "Invalid email address. Please enter a valid email address."
            return render_template('error.html', error_msg=error_msg)


        if phone and not re.match(r'^\d{10}$', phone): 
            error_msg = "Invalid phone number. Please enter a 10-digit phone number."
            return render_template('error.html', error_msg=error_msg)

        today = datetime.date.today()
        dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
        if dob_date > today:
            error_msg = "Invalid Date of Birth. Please enter a date in the past."
            return render_template('error.html', error_msg=error_msg)

        cursor = mysql_connection.cursor()

        cursor.execute("SELECT * FROM Registration WHERE ID=%s", (entry_id,))
        existing_entry = cursor.fetchone()
        if not existing_entry:
            error_msg = "Entry with ID {} does not exist.".format(entry_id)
            return render_template('error.html', error_msg=error_msg)

        cursor.execute("UPDATE Registration SET Name=%s, Email=%s, Dob=%s, Contactnum=%s WHERE ID=%s",
                       (name, email, dob, phone, entry_id))
        mysql_connection.commit()
        cursor.close()

        return redirect(url_for('succesp'))
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    if request.method == 'POST':
        entry_id = request.form['ID']

        cursor = mysql_connection.cursor()
        cursor.execute("SELECT * FROM Registration WHERE ID=%s", (entry_id,))
        entry = cursor.fetchone()

        if entry:
            cursor.execute("DELETE FROM Registration WHERE ID=%s", (entry_id,))
            mysql_connection.commit()
            cursor.close()
            return redirect(url_for('succesp')) 

        else:
            error_msg = "Entry with ID {} not found.".format(entry_id)
            return render_template('error.html', error_msg=error_msg)

    else:
        return render_template('delete.html')
@app.route('/succesp')
def succesp():
    return render_template('succesp.html')
if __name__ == '__main__':
    app.run(debug=True)
