# Food Ordering System

## Overview
The **Food Ordering System** is a web-based application that allows users to browse, select, and order food items online. The system includes user authentication, a shopping cart, and order management functionalities. This project is built using Flask, SQL, and HTML with a responsive UI.

## Features
- **User Authentication:** Register/Login with secure credentials.
- **Food Categories:** Browse food items categorized as Drinks, Foods (Indian, Western, French), Beverages, Snacks, and Refreshments.
- **Add to Cart:** Users can add food items to their cart before checkout.
- **Order Management:** Place orders with address confirmation.
- **Responsive UI:** Optimized for various devices.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript (Bootstrap for styling)
- **Backend:** Flask (Python-based web framework)
- **Database:** SQLite (SQL for database management)

## Installation Guide
Follow the steps below to set up the project on your local machine.

### 1. Clone the Repository
```sh
 git clone https://github.com/Shankesh05/Food_order.git
 cd Food_order
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
 python -m venv venv
 source venv/bin/activate   # For Linux/Mac
 venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
```sh
   pip install flask
   pip install flask_sqlalchemy
   pip install flask_login
   pip install flask_wtf
   pip install wtforms
   pip install sqlite3
```


### 4. Run the Application
```sh
 python app.py
```
The application will run on **http://127.0.0.1:5000/**

## Sample Login Credentials
Use the following credentials to test the login functionality:

### User Login:
- **Username:** user1
- **Password:** password1

## Contributing
Feel free to fork this repository and submit pull requests with improvements!

## Contact
For any queries, reach out to **Shankesh05** on GitHub.

