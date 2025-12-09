# Mini SQL Database Engine in Python

## Overview

This project is a simplified, in-memory SQL query engine built in Python.  
It loads data from a CSV file and allows you to run basic SQL queries from a command-line interface (CLI).

The goal is to demystify how a database processes a simple query by implementing:
- A tiny SQL parser
- An execution engine
- A CLI layer

## Project Structure

```text
mini-sql-engine/
  cli.py          # Command-line interface
  engine.py       # Query execution engine and Table model
  parser.py       # SQL parser
  generate_data.py# Script using Faker to generate sample CSVs
  data/
    employees.csv # Sample employee data
    products.csv  # Sample product data
  requirements.txt
  README.md
