from faker import Faker
import csv
import random
from pathlib import Path


def generate_employees(path: str, n_rows: int = 30):
    fake = Faker()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "age", "salary", "city"])
        for i in range(1, n_rows + 1):
            name = fake.name()
            age = random.randint(22, 60)
            salary = random.randint(30000, 120000)
            city = fake.city()
            writer.writerow([i, name, age, salary, city])


def generate_products(path: str, n_rows: int = 20):
    fake = Faker()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "product_name", "category", "price", "in_stock"])
        for i in range(1, n_rows + 1):
            product_name = fake.word().title()
            category = random.choice(["Electronics", "Books", "Clothing", "Home"])
            price = random.randint(100, 5000)
            in_stock = random.choice(["yes", "no"])
            writer.writerow([i, product_name, category, price, in_stock])


if __name__ == "__main__":
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    employees_path = data_dir / "employees.csv"
    products_path = data_dir / "products.csv"

    generate_employees(str(employees_path))
    generate_products(str(products_path))

    print(f"Generated: {employees_path}")
    print(f"Generated: {products_path}")
