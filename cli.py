import sys

from parser import SQLParser, SQLParseError
from engine import MiniSQLEngine, Table, SQLEngineError


def print_table(headers, rows):
    """Print results in a simple table format."""
    if not rows:
        print("No rows.")
        return

    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * w for w in col_widths)
    print(header_line)
    print(sep_line)

    for row in rows:
        print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))


def main():
    if len(sys.argv) < 3:
        print("Usage: python cli.py <table_name> <csv_path>")
        print("Example: python cli.py employees data/employees.csv")
        sys.exit(1)

    table_name = sys.argv[1]
    csv_path = sys.argv[2]

    try:
        table = Table.from_csv(table_name, csv_path)
    except SQLEngineError as e:
        print(f"Failed to load CSV: {e}")
        sys.exit(1)

    engine = MiniSQLEngine()
    engine.register_table(table)

    parser = SQLParser()

    print(f"Loaded table '{table_name}' from '{csv_path}'.")
    print("Enter SQL queries like:")
    print(f"  SELECT * FROM {table_name};")
    print(f"  SELECT name, age FROM {table_name} WHERE age > 30;")
    print(f"  SELECT COUNT(*) FROM {table_name};")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            query = input("SQL> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not query:
            continue
        if query.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break

        try:
            ast = parser.parse(query)
            headers, rows = engine.execute(ast)
            print_table(headers, rows)
        except SQLParseError as e:
            print(f"Parse error: {e}")
        except SQLEngineError as e:
            print(f"Engine error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        print()


if __name__ == "__main__":
    main()
