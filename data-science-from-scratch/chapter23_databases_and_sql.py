from typing import Tuple, Sequence, List, Any, Callable, Dict, Iterator
from collections import defaultdict

# A few type aliases we'll use later
Row = Dict[str, Any]                        # A database row
WhereClause = Callable[[Row], bool]         # Predicate for a single row
HavingClause = Callable[[List[Row]], bool]  # Predicate over multiple rows

class Table:
    def __init__(self, columns: List[str], types: List[type]) -> None:
        assert len(columns) == len(types), "# of columns must == # of types"

        self.columns = columns         # Names of columns
        self.types = types             # Data types of columns
        self.rows: List[Row] = []      # (no data yet)

    def col2type(self, col: str) -> type:
        idx = self.columns.index(col)      # Find the index of the column,
        return self.types[idx]             # and return its type.

    def insert(self, values: list) -> None:
        # Check for right # of values
        if len(values) != len(self.types):
            raise ValueError(f"You need to provide {len(self.types)} values")

        # Check for right types of values
        for value, typ3 in zip(values, self.types):
            if not isinstance(value, typ3) and value is not None:
                raise TypeError(f"Expected type {typ3} but got {value}")

        # Add the corresponding dict as a "row"
        self.rows.append(dict(zip(self.columns, values)))

    def __getitem__(self, idx: int) -> Row:
        return self.rows[idx]

    def __iter__(self) -> Iterator[Row]:
        return iter(self.rows)

    def __len__(self) -> int:
        return len(self.rows)

    def __repr__(self):
        """Pretty representation of the table: columns then rows"""
        rows = "\n".join(str(row) for row in self.rows)

        return f"{self.columns}\n{rows}"

    def update(self,
               updates: Dict[str, Any],
               predicate: WhereClause = lambda row: True):
        # First make sure the updates have valid names and types
        for column, new_value in updates.items():
            if column not in self.columns:
                raise ValueError(f"invalid column: {column}")

            typ3 = self.col2type(column)
            if not isinstance(new_value, typ3) and new_value is not None:
                raise TypeError(f"expected type {typ3}, but got {new_value}")

        # Now update
        for row in self.rows:
            if predicate(row):
                for column, new_value in updates.items():
                    row[column] = new_value

    def delete(self, predicate: WhereClause = lambda row: True) -> None:
        """Delete all rows matching predicate"""
        self.rows = [row for row in self.rows if not predicate(row)]

    def select(self,
               keep_columns: List[str] = None,
               additional_columns: Dict[str, Callable] = None) -> 'Table':

        if keep_columns is None:         # If no columns specified,
            keep_columns = self.columns  # return all columns

        if additional_columns is None:
            additional_columns = {}

        # New column names and types
        new_columns = keep_columns + list(additional_columns.keys())
        keep_types = [self.col2type(col) for col in keep_columns]

        # This is how to get the return type from a type annotation.
        # It will crash if `calculation` doesn't have a return type.
        add_types = [calculation.__annotations__['return']
                     for calculation in additional_columns.values()]

        # Create a new table for results
        new_table = Table(new_columns, keep_types + add_types)

        for row in self.rows:
            new_row = [row[column] for column in keep_columns]
            for column_name, calculation in additional_columns.items():
                new_row.append(calculation(row))
            new_table.insert(new_row)

        return new_table

    def where(self, predicate: WhereClause = lambda row: True) -> 'Table':
        """Return only the rows that satisfy the supplied predicate"""
        where_table = Table(self.columns, self.types)
        for row in self.rows:
            if predicate(row):
                values = [row[column] for column in self.columns]
                where_table.insert(values)
        return where_table

    def limit(self, num_rows: int) -> 'Table':
        """Return only the first `num_rows` rows"""
        limit_table = Table(self.columns, self.types)
        for i, row in enumerate(self.rows):
            if i >= num_rows:
                break
            values = [row[column] for column in self.columns]
            limit_table.insert(values)
        return limit_table

# CREATING A TABLE

users = Table(['user_id', 'name', 'num_friends'], [int, str, int])


# INSERTING ROWS

users.insert([0, 'Hero', 0])
users.insert([1, 'Dunn', 2])
users.insert([2, 'Sue', 3])
users.insert([3, 'Chi', 3])
users.insert([4, 'Thor', 3])
users.insert([5, 'Clive', 2])
users.insert([6, 'Hicks', 3])
users.insert([7, 'Devin', 2])
users.insert([8, 'Kate', 2])
users.insert([9, 'Klein', 3])
users.insert([10, 'Jen', 1])
print(users)

# UPDATING VALUES
user_update = users.update({'num_friends': 3},
             lambda row: row['user_id'] == 1)

# DELETING  VALUES
user_delete = users.delete(lambda row: row['user_id'] == 1)

# FILTERING COLUMNS AND ROWS

# SELECT * from users;
user_select_all = users.select()

# SELECT * FROM users LIMIT 2;
user_limit = users.limit(2)

# SELECT user_id FROM users;
user_select_id = users.select(keep_columns=['user_id'])

# SELECT user_id FROM users WHERE name = 'Sue'
sue_ids = users.where(lambda row: row["name"] == "Sue")\
               .select(keep_columns=["user_id"])

# SELECT LENGTH(name) AS name_length FROM users;
def name_length(row): return len(row['name'])
