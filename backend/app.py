from flask import Flask, jsonify, request

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import json
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong, unique secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong, unique JWT secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)  # Initialize JWTManager

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    is_super_user = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Loan(db.Model):
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong, unique secret key
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong, unique JWT secret key
    CORS(app)  # Enable CORS for all routes
    db.init_app(app)
    jwt.init_app(app)  # Initialize JWTManager
    return app

def create_tables():
    with app.app_context():
        db.create_all()

super_user_password = os.getenv("SUPER_USER_PASSWORD")

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if data.get('super_user_password') == super_user_password:
            is_super_user = True
        else:
            is_super_user = False

        new_customer = Customer(
            name=data['name'],
            city=data['city'],
            age=data['age'],
            username=data['username'],
            password=data['password'],
            is_super_user=is_super_user
        )
        db.session.add(new_customer)
        db.session.commit()

        # Generate JWT upon successful registration
        token = jwt.encode({'username': data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Registration successful', 'jwtToken': token.decode('UTF-8')}), 201
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Internal Server Error'}), 500

# Modify your login route in the backend
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Check if the username and password match a user in the database
        user = Customer.query.filter_by(username=username, password=password).first()

        if user:
            # Generate access token upon successful login
            access_token = create_access_token(identity=username)

            # Add a print statement to see the value of is_super_user in the terminal
            print('Is Super User:', user.is_super_user)

            return jsonify(access_token=access_token, is_super_user=user.is_super_user), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Internal Server Error'}), 500

# Add a new route for handling authenticated requests
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_user = jwt.get_jwt_identity()  # Use jwt.get_jwt_identity() instead of get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
    name=data['name'],
    city=data['city'],
    age=data['age'],
    username=data['username'],
    password=data['password'],
)

    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.form.to_dict()
    file = request.files.get('image')

    new_book = Book(
        name=data['name'],
        author=data['author'],
        year_published=data['year_published'],
        book_type=data['book_type']
    )

    if file:
        upload_folder = 'path/to/save/'
        os.makedirs(upload_folder, exist_ok=True)  # Create directory if it doesn't exist

        # Save the file to the specified location
        file.save(os.path.join(upload_folder, secure_filename(file.filename)))
        new_book.image_path = os.path.join(upload_folder, secure_filename(file.filename))

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
        db.session.delete(loan)  # Remove the loan entry from the database
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
    customer_list = [{'id': customer.id, 'name': customer.name, 'city': customer.city, 'age': customer.age} for customer in customers]
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
        return jsonify({'customer': {'name': customer.name, 'city': customer.city, 'age': customer.age}})
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
    create_app()
    create_tables()
    app.run(debug=True, port=5000)
