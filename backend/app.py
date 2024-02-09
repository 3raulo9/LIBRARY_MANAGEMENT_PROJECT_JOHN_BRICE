import datetime
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class Loan(db.Model):
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], city=data['city'], age=data['age'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(name=data['name'], author=data['author'], year_published=data['year_published'], book_type=data['book_type'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/loan_book', methods=['POST'])
def loan_book():
    data = request.json
    cust_id = data['cust_id']
    book_id = data['book_id']
    book_type = Book.query.get(book_id).book_type

    loan_duration = {
        1: 10,
        2: 5,
        3: 2
    }

    return_date = datetime.datetime.now() + datetime.timedelta(days=loan_duration.get(book_type, 0))
    new_loan = Loan(cust_id=cust_id, book_id=book_id, loan_date=datetime.datetime.now(), return_date=return_date)
    db.session.add(new_loan)
    db.session.commit()
    return jsonify({'message': 'Book loaned successfully'}), 201

if __name__ == '__main__':
    create_app()
    create_tables()
    app.run(debug=True, port=5000)