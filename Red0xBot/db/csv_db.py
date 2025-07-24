import pandas as pd
import os
from datetime import datetime, timezone

db_name = "books_db.csv"
null_values = [
    "NA",
    "N/A",
    "missing",
    "null",
    "-",
    "",
    "NaN"
]
columns=["book_name", "created_at", "author", "topic"]
data_type = {
    "book_name": "object",
    "created_at": "datetime64[ns]",
    "author": "object",
    "topic": "object"
}

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None # File not found

def mainFunc() -> bool:
    try:
        start_directory = "./"
        found_path = find_file(db_name, start_directory)
        if found_path:
            return True
        else:
            df = pd.DataFrame(columns=columns).astype(data_type)
            df.to_csv(db_name, index=True)
            return True
    except Exception as e:
        raise Exception("An error occured")
    
def searchFunc(search_item: str):
    try:
        df = pd.read_csv(
            db_name,
            na_values=null_values,
        )
        search_result = df[df["book_name"] == search_item]
        if search_result.empty:
            return None
        else:
            return search_result
    except Exception as e:
        raise Exception("There was an error.")

def add_record(book_name: str, created_at: datetime, author: str, topic: str):
    new_record = pd.DataFrame([[book_name, created_at, author, topic]], columns=columns)
    new_record.to_csv(db_name, mode="a", header=False, index=False)