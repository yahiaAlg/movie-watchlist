#!C:\Users\yahia\AppData\Local\Programs\Python\Python312\Scripts
import json
import os
import datetime
from operator import itemgetter
from pprint import pprint
class JSONDatabaseUtility:
    def __init__(self, database_file):
        self.database_file = database_file
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.database_file):
            with open(self.database_file, 'r') as file:
                return json.load(file)
        else:
            with open(self.database_file, "w") as f:
                f.seek(0)
                json.dump({}, f)
            with open(self.database_file) as f:
                return json.load(f)

    def _save_data(self):
        with open(self.database_file, 'w') as file:
            json.dump(self.data, file, indent=2, default=self._json_serial)

    def _json_serial(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def create_table(self, table_name):
        if table_name not in self.data:
            self.data[table_name] = []
            self._save_data()
            return True
        return False

    def drop_table(self, table_name):
        if table_name in self.data:
            del self.data[table_name]
            self._save_data()
            return True
        return False

    def list_tables(self):
        return list(self.data.keys())

    # DML Operations

    def insert(self, table_name, record):
        if table_name in self.data:
            self.data[table_name].append(record)
            self._save_data()
            return True
        return False

    def select(self, table_name, conditions=None, fields=None, order_by=None, limit=None):
        if table_name not in self.data:
            return []

        result = self.data[table_name]

        # Apply conditions
        if conditions:
            result = [record for record in result if self._meets_conditions(record, conditions)]

        # Select specific fields
        if fields:
            result = [{k: r[k] for k in fields if k in r} for r in result]

        # Apply sorting
        if order_by:
            reverse = False
            if isinstance(order_by, tuple):
                order_by, reverse = order_by
            result = sorted(result, key=itemgetter(order_by), reverse=reverse)

        # Apply limit
        if limit:
            result = result[:limit]

        return result

    def _meets_conditions(self, record, conditions):
        if callable(conditions):
            return conditions(record)
        
        for field, condition in conditions.items():
            if field not in record:
                return False
            if callable(condition):
                if not condition(record[field]):
                    return False
            elif record[field] != condition:
                return False
        return True

    def update(self, table_name, condition, update_func):
        if table_name in self.data:
            updated = False
            for record in self.data[table_name]:
                if condition(record):
                    update_func(record)
                    updated = True
            if updated:
                self._save_data()
            return updated
        return False

    def delete(self, table_name, condition):
        if table_name in self.data:
            original_length = len(self.data[table_name])
            self.data[table_name] = [record for record in self.data[table_name] if not condition(record)]
            if len(self.data[table_name]) < original_length:
                self._save_data()
                return True
        return False

# Usage example
if __name__ == "__main__":
    db = JSONDatabaseUtility("example_db.json")

    # DDL operations
    db.create_table("users")
    db.create_table("posts")
    print("Tables:")
    pprint(db.list_tables())

    # DML operations

    db.insert("users", {"id": 1, "name": "John Doe", "age": 30, "created_at": datetime.datetime.now()})
    db.insert("users", {"id": 2, "name": "Jane Smith", "age": 25, "created_at": datetime.datetime.now()})
    db.insert("users", {"id": 3, "name": "Bob Johnson", "age": 35, "created_at": datetime.datetime.now()})
    print("All users:")
    pprint(db.select("users"))
    print("Users with id > 1:")
    pprint(db.select("users", lambda x: x["id"] > 1))

    db.update("users", lambda x: x["id"] == 1, lambda x: x.update({"name": "John Updated"}))
    print("After update:")
    pprint(db.select("users", lambda x: x["id"] == 1))

    db.delete("users", lambda x: x["id"] == 2)
    print("After delete:")
    pprint(db.select("users"))

    # Drop table
    db.drop_table("posts")
    print("Tables after drop:")
    pprint(db.list_tables())
    
    
    # Simple select all
    print("All users:")
    pprint(db.select("users"))

    # Select with conditions
    print("Users older than 28:")
    pprint(db.select("users", conditions={"age": lambda x: x > 28}))

    # Select specific fields
    print("User names:")
    pprint(db.select("users", fields=["name"]))

    # Select with ordering
    print("Users ordered by age (descending):")
    pprint(db.select("users", order_by=("age", True)))

    # Select with limit
    print("First 2 users:")
    pprint(db.select("users", limit=2))

    # Combining multiple options
    print("Names of 2 youngest users:")
    pprint(db.select("users", 
                    fields=["name", "age"],
                    order_by="age",
                    limit=2))

    # Using a callable for complex conditions
    print("Users with even id and age > 28:")
    pprint(db.select("users", 
                    conditions=lambda r: r["age"] % 2 == 0 and r["age"] > 28))
    
    db.drop_table("posts")
    db.drop_table("users")
    
    # Create a table and insert some data
    db.create_table("users")
    db.insert("users", {"id": 1, "name": "John Doe", "age": 30, "created_at": datetime.datetime.now()})
    db.insert("users", {"id": 2, "name": "Jane Smith", "age": 25, "created_at": datetime.datetime.now()})
    db.insert("users", {"id": 3, "name": "Bob Johnson", "age": 35, "created_at": datetime.datetime.now()})
    db.insert("users", {"id": 4, "name": "Alice Brown", "age": 40, "created_at": datetime.datetime.now()})
    db.insert("users", {"id": 5, "name": "Charlie Davis", "age": 22, "created_at": datetime.datetime.now()})

    print("All users:")
    pprint(db.select("users"))

    print("\nUsers older than 28:")
    pprint(db.select("users", conditions={"age": lambda x: x > 28}))

    print("\nUser names:")
    pprint(db.select("users", fields=["name"]))

    print("\nUsers ordered by age (descending):")
    pprint(db.select("users", order_by=("age", True)))

    print("\nFirst 2 users:")
    pprint(db.select("users", limit=2))

    print("\nNames of 2 youngest users:")
    pprint(db.select("users", 
                     fields=["name", "age"],
                     order_by="age",
                     limit=2))

    print("\nUsers with even id and age > 28:")
    pprint(db.select("users", 
                     conditions=lambda r: r["id"] % 2 == 0 and r["age"] > 28))