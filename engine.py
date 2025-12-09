import csv
from dataclasses import dataclass
from typing import List, Dict, Any, Iterable, Tuple, Optional


class SQLEngineError(Exception):
    """Custom exception for engine / execution errors."""
    pass


@dataclass
class Table:
    name: str
    columns: List[str]
    rows: List[Dict[str, Any]]

    @classmethod
    def from_csv(cls, name: str, path: str) -> "Table":
        """Load a CSV file into a Table object."""
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                cols = reader.fieldnames
                if cols is None:
                    raise SQLEngineError(f"CSV file '{path}' has no header row.")

                rows: List[Dict[str, Any]] = []
                for row in reader:
                    parsed: Dict[str, Any] = {}
                    for col, value in row.items():
                        parsed[col] = _auto_convert(value)
                    rows.append(parsed)
        except FileNotFoundError:
            raise SQLEngineError(f"CSV file '{path}' not found.")
        except Exception as e:
            raise SQLEngineError(f"Error reading CSV '{path}': {e}")

        return cls(name=name, columns=cols, rows=rows)


def _auto_convert(value: Optional[str]) -> Any:
    """Convert strings to int/float if possible, else keep as string."""
    if value is None:
        return None
    s = value.strip()
    if s == "":
        return s

    try:
        return int(s)
    except ValueError:
        pass

    try:
        return float(s)
    except ValueError:
        pass

    return s


class MiniSQLEngine:
    """
    Small in-memory SQL engine.
    Supports:
      - SELECT * / SELECT col1, col2
      - WHERE with a single condition
      - COUNT(*) with optional WHERE
    """

    def __init__(self) -> None:
        self.tables: Dict[str, Table] = {}

    def register_table(self, table: Table) -> None:
        self.tables[table.name.lower()] = table

    def get_table(self, name: str) -> Table:
        key = name.lower()
        if key not in self.tables:
            raise SQLEngineError(
                f"Unknown table '{name}'. Loaded tables: {list(self.tables.keys())}"
            )
        return self.tables[key]

    def execute(self, ast: Dict[str, Any]) -> Tuple[List[str], List[List[Any]]]:
        """Execute a parsed query AST and return (headers, rows)."""
        qtype = ast["type"]
        if qtype == "select":
            return self._execute_select(ast)
        elif qtype == "count":
            return self._execute_count(ast)
        else:
            raise SQLEngineError(f"Unsupported query type: {qtype}")

    # ---------------- Internal helpers ----------------

    def _apply_where(
        self,
        rows: Iterable[Dict[str, Any]],
        table: Table,
        where_ast: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Apply WHERE filter (if any) to rows."""
        if where_ast is None:
            return list(rows)

        col = where_ast["column"]
        op = where_ast["op"]
        value = where_ast["value"]

        if col not in table.columns:
            raise SQLEngineError(
                f"Column '{col}' does not exist in table '{table.name}'."
            )

        def match(row: Dict[str, Any]) -> bool:
            left = row.get(col)
            right = value
            try:
                if op == "=":
                    return left == right
                elif op == "!=":
                    return left != right
                elif op == "<":
                    return left < right
                elif op == ">":
                    return left > right
                elif op == "<=":
                    return left <= right
                elif op == ">=":
                    return left >= right
                else:
                    return False
            except TypeError:
                # E.g., comparing str with int – treat as no match
                return False

        return [r for r in rows if match(r)]

    def _execute_select(self, ast: Dict[str, Any]) -> Tuple[List[str], List[List[Any]]]:
        table = self.get_table(ast["table"])
        filtered = self._apply_where(table.rows, table, ast["where"])

        # Determine columns to project
        if ast["columns"] == ["*"]:
            headers = table.columns
        else:
            for col in ast["columns"]:
                if col not in table.columns:
                    raise SQLEngineError(
                        f"Column '{col}' does not exist in table '{table.name}'."
                    )
            headers = ast["columns"]

        rows_out: List[List[Any]] = []
        for row in filtered:
            rows_out.append([row.get(col, "") for col in headers])

        return headers, rows_out

    def _execute_count(self, ast: Dict[str, Any]) -> Tuple[List[str], List[List[Any]]]:
        table = self.get_table(ast["table"])
        filtered = self._apply_where(table.rows, table, ast["where"])
        count_value = len(filtered)
        return ["COUNT"], [[count_value]]
