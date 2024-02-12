const BASE_URL = "http://localhost:5000";

async function addCustomer() {
  const formData = new FormData(document.getElementById("addCustomerForm"));
  const response = await axios.post(
    `${BASE_URL}/add_customer`,
    Object.fromEntries(formData)
  );
  alert(response.data.message);
}
async function addBook() {
  const formData = new FormData(document.getElementById("addBookForm"));
  const imageInput = document.getElementById("bookImage");
  
  if (imageInput.files.length > 0) {
    formData.append("image", imageInput.files[0]);
  }

  const response = await axios.post(
    `${BASE_URL}/add_book`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
  );
  alert(response.data.message);
}

async function loanBook() {
  const formData = new FormData(document.getElementById("loanBookForm"));
  const response = await axios.post(
    `${BASE_URL}/loan_book`,
    Object.fromEntries(formData)
  );
  alert(response.data.message);
}
async function returnBook() {
  const formData = new FormData(document.getElementById("returnBookForm"));
  const response = await axios.post(
    `${BASE_URL}/return_book`,
    Object.fromEntries(formData)
  );
  alert(response.data.message);
}
async function showAllBooks() {
  const response = await axios.get(`${BASE_URL}/display_books`);
  const books = response.data.books;

  // Create a temporary div to extract text content
  const tempDiv = document.createElement("div");

  // Set the HTML content with book information
  tempDiv.innerHTML = `<h3>All Books: 
</h3><ul></ul>`;

  const ulElement = tempDiv.querySelector("ul");

  books.forEach((book) => {
    const liElement = document.createElement("li");
    liElement.textContent = `${book.name} by ${book.author} (${book.year_published}) - Type ${book.book_type}`;
    ulElement.appendChild(liElement);
  });

  // Extract text content without HTML tags
  const textContent = tempDiv.textContent;

  // Display the text content in the alert popup
  alert(textContent);
}
async function showAllCustomers() {
  const response = await axios.get(`${BASE_URL}/display_customers`);
  const customers = response.data.customers;

  // Create a temporary div to extract text content
  const tempDiv = document.createElement("div");

  // Set the HTML content with customer information
  tempDiv.innerHTML = `<h3>All Customers:
</h3><ul></ul>`;

  const ulElement = tempDiv.querySelector("ul");

  customers.forEach((customer) => {
    const liElement = document.createElement("li");
    liElement.textContent = `ID ${customer.id}: ${customer.name} from ${customer.city}, Age ${customer.age}\n`;
    ulElement.appendChild(liElement);
  });

  // Extract text content without HTML tags
  const textContent = tempDiv.textContent;

  // Display the text content in the alert popup
  alert(textContent);
}

async function showAllLoans() {
  const response = await axios.get(`${BASE_URL}/display_loans`);
  const loans = response.data.loans;

  // Create a temporary div to extract text content
  const tempDiv = document.createElement("div");

  // Set the HTML content with loan information
  tempDiv.innerHTML = `<h3>All Loans:
</h3><ul></ul>`;

  const ulElement = tempDiv.querySelector("ul");

  loans.forEach((loan) => {
    const liElement = document.createElement("li");
    liElement.textContent = `Customer ID: ${loan.cust_id}, Book ID: ${loan.book_id}, Loan Date: ${loan.loan_date}, Return Date: ${loan.return_date}`;
    ulElement.appendChild(liElement);
  });

  // Extract text content without HTML tags
  const textContent = tempDiv.textContent;

  // Display the text content in the alert popup
  alert(textContent);
}
async function showLateLoans() {
  const response = await axios.get(`${BASE_URL}/display_late_loans`);
  const lateLoans = response.data.late_loans;

  // Create a temporary div to extract text content
  const tempDiv = document.createElement("div");

  // Set the HTML content with late loan information
  tempDiv.innerHTML = `<h3>Late Loans:
</h3><ul></ul>`;

  const ulElement = tempDiv.querySelector("ul");

  lateLoans.forEach((loan) => {
    const liElement = document.createElement("li");
    liElement.textContent = `Customer ID: ${loan.cust_id}, Book ID: ${loan.book_id}, Loan Date: ${loan.loan_date}, Return Date: ${loan.return_date}`;
    ulElement.appendChild(liElement);
  });

  // Extract text content without HTML tags
  const textContent = tempDiv.textContent;

  // Display the text content in the alert popup
  alert(textContent);
}
async function findCustomer() {
  const customerName = document.getElementById("findCustomerName").value.trim();

  if (!customerName) {
    alert("Please enter a customer name");
    return;
  }

  try {
    const response = await axios.get(
      `${BASE_URL}/find_customer?name=${encodeURIComponent(customerName)}`
    );

    if (response.status === 200) {
      const customer = response.data.customer;
      alert(
        `Customer Found!\nName: ${customer.name}\nCity: ${customer.city}\nAge: ${customer.age}`
      );
    } else {
      alert("Customer not found");
    }
  } catch (error) {
    if (error.response && error.response.status === 404) {
      alert("Customer not found");
    } else {
      console.error("Error fetching customer:", error);
      alert(
        "An unexpected error occurred while fetching customer information. Please try again later."
      );
    }
  }
}
async function findBook() {
  const bookName = document.getElementById("findBookName").value.trim();

  if (!bookName) {
    alert("Please enter a book name");
    return;
  }

  try {
    const response = await axios.get(
      `${BASE_URL}/find_book?name=${encodeURIComponent(bookName)}`
    );

    if (response.status === 200) {
      const book = response.data.book;
      alert(
        `Book Found!\nName: ${book.name}\nAuthor: ${book.author}\nYear Published: ${book.year_published}\nType: ${book.book_type}`
      );
    } else {
      alert("Book not found");
    }
  } catch (error) {
    if (error.response && error.response.status === 404) {
      alert("Book not found");
    } else {
      console.error("Error fetching book:", error);
      alert(
        "An unexpected error occurred while fetching book information. Please try again later."
      );
    }
  }
}
async function removeBook() {
  const bookId = document.getElementById("removeBookId").value;

  try {
    const response = await axios.delete(`${BASE_URL}/remove_book/${bookId}`);
    alert(response.data.message);
  } catch (error) {
    alert("Error removing book: " + error.response.data.message);
  }
}
async function removeCustomer() {
  const custId = document.getElementById("removeCustomerId").value;

  try {
    const response = await axios.delete(
      `${BASE_URL}/remove_customer/${custId}`
    );
    alert(response.data.message);
  } catch (error) {
    alert("Error removing customer: " + error.response.data.message);
  }
}
