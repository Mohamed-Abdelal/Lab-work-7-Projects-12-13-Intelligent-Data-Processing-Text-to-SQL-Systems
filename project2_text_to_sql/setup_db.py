import sqlite3
import os

DB_PATH = "retail.db"

def setup_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE Customers (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        JoinDate DATE
    )
    ''')

    cursor.execute('''
    CREATE TABLE Products (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        ProductName TEXT NOT NULL,
        Category TEXT NOT NULL,
        Price REAL NOT NULL,
        StockQuantity INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerID INTEGER,
        OrderDate DATE NOT NULL,
        TotalAmount REAL NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE OrderItems (
        OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INTEGER,
        ProductID INTEGER,
        Quantity INTEGER NOT NULL,
        UnitPrice REAL NOT NULL,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
    ''')

    # Insert Dummy Data - Customers
    customers = [
        ("Alice", "Smith", "alice@example.com", "2023-01-15"),
        ("Bob", "Johnson", "bob@example.com", "2023-02-20"),
        ("Charlie", "Brown", "charlie@example.com", "2023-03-10"),
        ("Diana", "Evans", "diana@example.com", "2023-04-05")
    ]
    cursor.executemany("INSERT INTO Customers (FirstName, LastName, Email, JoinDate) VALUES (?, ?, ?, ?)", customers)

    # Insert Dummy Data - Products
    products = [
        ("Laptop", "Electronics", 999.99, 50),
        ("Smartphone", "Electronics", 699.99, 100),
        ("Headphones", "Accessories", 149.99, 200),
        ("Desk Chair", "Furniture", 199.50, 20),
        ("Coffee Maker", "Appliances", 89.99, 30)
    ]
    cursor.executemany("INSERT INTO Products (ProductName, Category, Price, StockQuantity) VALUES (?, ?, ?, ?)", products)

    # Insert Dummy Data - Orders
    orders = [
        (1, "2023-10-01", 1149.98),
        (2, "2023-10-05", 699.99),
        (1, "2023-10-10", 199.50),
        (3, "2023-10-15", 239.98),
        (4, "2023-10-20", 89.99)
    ]
    cursor.executemany("INSERT INTO Orders (CustomerID, OrderDate, TotalAmount) VALUES (?, ?, ?)", orders)

    # Insert Dummy Data - Order Items
    order_items = [
        (1, 1, 1, 999.99),
        (1, 3, 1, 149.99),
        (2, 2, 1, 699.99),
        (3, 4, 1, 199.50),
        (4, 3, 1, 149.99),
        (4, 5, 1, 89.99),
        (5, 5, 1, 89.99)
    ]
    cursor.executemany("INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?)", order_items)

    conn.commit()
    conn.close()
    print(f"Database ({DB_PATH}) created and populated with sample data successfully.")

if __name__ == "__main__":
    setup_database()
