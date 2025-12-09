# Mini SQL Database Engine in Python

## 📌 Overview

This project implements a simplified, **in-memory SQL query engine** using Python.  
It loads data from CSV files and allows users to run SQL-like queries through an interactive **command-line interface (CLI)**.

The goal of the project is to understand how a database internally processes a simple query by implementing:

- A **SQL Parser**  
- A **Query Execution Engine**  
- A **CLI interface**

This project also demonstrates skills in **data parsing**, **data management**, **CLI development**, and **modular programming**.

---

## 📂 Project Structure

mini-sql-engine/
│
├── cli.py # Command-line interface for user interaction
├── parser.py # SQL parsing logic (SELECT, WHERE, COUNT)
├── engine.py # Query execution: filtering, projection, aggregation
├── generate_data.py # Script using Faker to generate sample CSV files
│
├── data/
│ ├── employees.csv # Sample dataset for testing
│ └── products.csv # Additional dataset for testing
│
├── requirements.txt # Python dependencies
└── README.md # Project documentation

📘 Supported SQL Grammar

This engine supports a basic subset of SQL.
The grammar is intentionally limited but fully functional for learning purposes.

1️⃣ SELECT all columns
SELECT * FROM table_name;


Example:

SELECT * FROM employees;

2️⃣ SELECT specific columns
SELECT col1, col2 FROM table_name;


Example:

SELECT name, salary FROM employees;

3️⃣ WHERE Clause (Single Condition Only)

Supported operators:

=   !=   <   >   <=   >=


Examples:

SELECT name, age FROM employees WHERE age > 30;

SELECT product_name, price FROM products WHERE category = 'Books';


The engine supports one condition only (no AND/OR).

4️⃣ COUNT(*) Aggregation
SELECT COUNT(*) FROM table_name;
SELECT COUNT(*) FROM table_name WHERE column op value;


Examples:

SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM employees WHERE age >= 40;

🧪 Example Queries
✔ Show all products:
SELECT * FROM products;

✔ Show employees older than 30:
SELECT name, salary FROM employees WHERE age > 30;

✔ Count available products:
SELECT COUNT(*) FROM products WHERE in_stock = 'yes';

⚠️ Error Handling

The engine gracefully handles errors such as:

❌ Invalid SQL syntax
SELECT age employees;

❌ Unknown column
SELECT abc FROM employees;

❌ Wrong WHERE format
SELECT * FROM employees WHERE age >;


Instead of crashing, the CLI displays a clear error message and continues running.

🚫 Limitations

This project does not support:

ORDER BY

GROUP BY

JOIN

INSERT / UPDATE / DELETE

Multiple WHERE conditions (no AND/OR)

Aggregations other than COUNT(*)

The goal is simplicity and education, not full SQL compliance.

🎯 Conclusion

This project provides a foundational understanding of how SQL query processing works internally by manually implementing:

Query parsing

Row filtering

Column projection

Simple aggregation

Display formatting

It demonstrates clean modular code and core data engineering concepts.

## 👩‍💻 Author  
**Sravani Punnam**