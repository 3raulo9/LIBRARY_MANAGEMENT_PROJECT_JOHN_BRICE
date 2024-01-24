from flask import Flask, request, redirect
from pages.home_page import app as home_app
from dotenv import load_dotenv
import mysql.connector

import json
import os

app = Flask(__name__)

# Mock user database for demonstration purposes
users = [{'username': 'admin', 'password': 'admin123'}]

app = home_app 

load_dotenv()

db_of_users = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="users_db",
)
cursor = db_of_users.cursor()




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username is not already taken
        if any(user['username'] == username for user in users):
            return 'Username already taken. Please choose another username.'
        
        # Add the new user to the database (in-memory for simplicity)
        users.append({'username': username, 'password': password})
        
        return 'Registration successful! You can now <a href="/login">login</a>.'
    
    # Display the registration form
    return '''
        <form method="post" action="/register">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <input type="submit" value="Register">
        </form>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the provided credentials are valid
        if any(user['username'] == username and user['password'] == password for user in users):
            return f'Hello, {username}! You are now logged in.'
        else:
            return 'Invalid username or password. Please try again.'
    
    # Display the login form
    return '''
        <form method="post" action="/login">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
