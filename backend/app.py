import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
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

def create_tables():
    with app.app_context():
        db.create_all()

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

@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.json
    cust_id = data['cust_id']
    book_id = data['book_id']

    loan = Loan.query.filter_by(cust_id=cust_id, book_id=book_id).first()
    if loan:
        loan.return_date = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'}), 201
    else:
        return jsonify({'message': 'Loan not found'}), 404


@app.route('/display_books', methods=['GET'])
def display_books():
    books = Book.query.all()
    book_list = [{'name': book.name, 'author': book.author, 'year_published': book.year_published, 'book_type': book.book_type} for book in books]
    return jsonify({'books': book_list})

@app.route('/display_customers', methods=['GET'])
def display_customers():
    customers = Customer.query.all()
    customer_list = [{'name': customer.name, 'city': customer.city, 'age': customer.age} for customer in customers]
    return jsonify({'customers': customer_list})

@app.route('/display_loans', methods=['GET'])
def display_loans():
    loans = Loan.query.all()
    loan_list = [{'cust_id': loan.cust_id, 'book_id': loan.book_id, 'loan_date': loan.loan_date, 'return_date': loan.return_date} for loan in loans]
    return jsonify({'loans': loan_list})

@app.route('/display_late_loans', methods=['GET'])
def display_late_loans():
    current_date = datetime.datetime.now().date()
    late_loans = Loan.query.filter(Loan.return_date < current_date).all()
    late_loan_list = [{'cust_id': loan.cust_id, 'book_id': loan.book_id, 'loan_date': loan.loan_date, 'return_date': loan.return_date} for loan in late_loans]
    return jsonify({'late_loans': late_loan_list})


@app.route('/find_book', methods=['GET'])
def find_book():
    book_name = request.args.get('name')
    book = Book.query.filter_by(name=book_name).first()
    if book:
        return jsonify({'book': {'name': book.name, 'author': book.author, 'year_published': book.year_published, 'book_type': book.book_type}})
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/find_customer', methods=['GET'])
def find_customer():
    customer_name = request.args.get('name')
    customer = Customer.query.filter_by(name=customer_name).first()
    if customer:
        return jsonify({'customer': {'name': customer.name, 'city': customer.city, 'age': customer.age, }})
    else:
        return jsonify({'message': 'Customer not found'}), 404


@app.route('/remove_book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book removed successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404


@app.route('/remove_customer/<int:cust_id>', methods=['DELETE'])
def remove_customer(cust_id):
    customer = Customer.query.get(cust_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer removed successfully'}), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404
    

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=5000)
