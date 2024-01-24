from flask import Flask
from dotenv import load_dotenv
import mysql.connector

import json
import os

app = Flask(__name__)

load_dotenv()

db_of_users = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="users_db",
)
cursor = db_of_users.cursor()


@app.route("/")
def main():
    # Adding Bootstrap CDN link to the response
    bootstrap_link = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'

    # Your HTML content
    html_content = "<p>Hello, World!</p>"

    # Combining Bootstrap CDN link and your HTML content
    complete_html = bootstrap_link + html_content

    return complete_html


if __name__ == "__main__":
    app.run(debug=True)
