# Python FS - 7732/13 Project

## Project Overview
This project involves the implementation of a simple system for managing a book library using Python.
Sure, here is the markdown format for the instructions you provided:

```markdown
## How to use

To start off, you have to create a virtual environment. You can do it by following the next steps:

1. Install the virtual environment package:
   ```
   pip install virtualenv
   ```

2. Navigate to your project directory:
   ```
   cd /path/to/your/project
   ```

3. Create a new virtual environment in your project directory:
   ```
   virtualenv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```

Now, you are in your virtual environment and can start installing packages for your project.
```
Please replace `/path/to/your/project` with the actual path to your project directory. The name `venv` is just an example, you can name your virtual environment as you wish.


Sure, here is the instruction to install the packages listed in the `requirements.txt` file:

```markdown
## Installing Packages

After activating your virtual environment, you can install the required packages using the `requirements.txt` file. Here are the steps:

1. Ensure that you are in the project directory where `requirements.txt` is located.
   ```shell
   cd /path/to/your/project
   ```

2. Use pip to install the packages:
   ```shell
   pip install -r requirements.txt
   ```

This command will install all the packages listed in the `requirements.txt` file.

Please replace `/path/to/your/project` with the actual path to your project directory. Make sure your `requirements.txt` file is in the project directory.



## Project Description
mySQL tables:
1. Books
   - Id (PK)
   - Name
   - Author
   - Year Published
   - Type (1/2/3)
2. Customers
   - Id (PK)
   - Name
   - City
   - Age
3. Loans
   - CustID
   - BookID
   - Loan date
   - Return date

### Loan Duration
The book type determines the maximum loan time:
- Type 1: up to 10 days
- Type 2: up to 5 days
- Type 3: up to 2 days

### DAL (Data Access Layer)
1. Build a class for each entity (Books, Customers, Loans).
2. Create a separate module for each class.
3. Develop unit tests for the DAL.

### Client Application
Build a client application to interact with the DAL. Implement the following operations and display them in a simple menu:
1. Add a new customer
2. Add a new book
3. Loan a book
4. Return a book
5. Display all books
6. Display all customers
7. Display all loans
8. Display late loans
9. Find book by name
10. Find customer by name
11. Remove book
12. Remove customer




# Testing Endpoints in Your Application

## Add a new customer:

- **Endpoint:** POST http://localhost:5000/add_customer
- **Body (raw JSON):**
    ```json
    {
        "name": "John Doe",
        "city": "New York",
        "age": 25
    }
    ```
  
## Add a new book:

- **Endpoint:** POST http://localhost:5000/add_book
- **Body (raw JSON):**
    ```json
    {
        "name": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year_published": 1925,
        "book_type": 1
    }
    ```

## Loan a book:

- **Endpoint:** POST http://localhost:5000/loan_book
- **Body (raw JSON):**
    ```json
    {
        "cust_id": 1,
        "book_id": 1
    }
    ```

## Return a book:

- **Endpoint:** POST http://localhost:5000/return_book
- **Body (raw JSON):**
    ```json
    {
        "cust_id": 1,
        "book_id": 1
    }
    ```

## Display all books:

- **Endpoint:** GET http://localhost:5000/display_books
-WORKS!

## Display all customers:

- **Endpoint:** GET http://localhost:5000/display_customers
-WORKS!

## Display all loans:

- **Endpoint:** GET http://localhost:5000/display_loans
-WORKS

## Display late loans:

- **Endpoint:** GET http://localhost:5000/display_late_loans
-WORKS!

## Find book by name:

- **Endpoint:** GET http://localhost:5000/find_book?name=The%20Great%20Gatsby
-WORKS!

## Find customer by name:

- **Endpoint:** GET http://localhost:5000/find_customer?name=John%20Doe
-WORKS!

## Remove book:

- **Endpoint:** DELETE http://localhost:5000/remove_book/1
-WORKS!
## Remove customer: 

- **Endpoint:** DELETE http://localhost:5000/remove_customer/1
-WORKS!

Make sure your Flask server is running while testing these requests in Postman. Adjust the URLs and parameters based on your actual setup.
