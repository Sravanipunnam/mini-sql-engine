import re


class SQLParseError(Exception):
    """Custom exception for SQL parsing errors."""
    pass


class SQLParser:
    """
    Very small SQL parser.
    Supports:
      - SELECT * FROM table;
      - SELECT col1, col2 FROM table;
      - Optional WHERE: WHERE column op value
      - COUNT: SELECT COUNT(*) FROM table [WHERE ...];
    """

    def parse(self, query: str) -> dict:
        q = query.strip()
        if not q:
            raise SQLParseError("Empty query.")
        if q.endswith(";"):
            q = q[:-1].strip()

        # Pattern for COUNT(*)
        m = re.match(
            r"(?i)^select\s+count\s*\(\s*\*\s*\)\s+from\s+([a-zA-Z_][\w]*)\s*(where\s+(.+))?$",
            q,
        )
        if m:
            table = m.group(1)
            where_text = m.group(3)
            where_ast = self._parse_where(where_text) if where_text else None
            return {
                "type": "count",
                "table": table,
                "where": where_ast,
            }

        # Pattern for normal SELECT
        m = re.match(
            r"(?i)^select\s+(.+)\s+from\s+([a-zA-Z_][\w]*)\s*(where\s+(.+))?$",
            q,
        )
        if not m:
            raise SQLParseError(
                "Only queries of the form: "
                "SELECT ... FROM table [WHERE column op value] are supported."
            )

        select_list = m.group(1).strip()
        table = m.group(2)
        where_text = m.group(4)
        where_ast = self._parse_where(where_text) if where_text else None

        if select_list == "*":
            columns = ["*"]
        else:
            columns = [c.strip() for c in select_list.split(",") if c.strip()]
            if not columns:
                raise SQLParseError("SELECT list is empty.")

        return {
            "type": "select",
            "table": table,
            "columns": columns,
            "where": where_ast,
        }

    def _parse_where(self, where: str) -> dict:
        where = where.strip()
        # column op value  (no AND/OR)
        m = re.match(
            r"(?i)^([a-zA-Z_][\w]*)\s*(=|!=|<=|>=|<|>)\s*(.+)$",
            where,
        )
        if not m:
            raise SQLParseError(
                "WHERE clause must be: column op value "
                "(e.g., age > 30 or city = 'Hyderabad')."
            )
        col, op, raw_val = m.group(1), m.group(2), m.group(3)
        value = self._parse_literal(raw_val)
        return {"column": col, "op": op, "value": value}

    def _parse_literal(self, raw: str):
        raw = raw.strip()
        # String literal in quotes
        if (raw.startswith("'") and raw.endswith("'")) or (
            raw.startswith('"') and raw.endswith('"')
        ):
            return raw[1:-1]

        # Try integer
        try:
            return int(raw)
        except ValueError:
            pass

        # Try float
        try:
            return float(raw)
        except ValueError:
            pass

        # Fallback to plain string
        return raw
