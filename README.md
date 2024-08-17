# FastAPI JSON CRUD Operations

This project is a basic implementation of CRUD (Create, Read, Update, Delete) operations using FastAPI. The data is stored in a JSON file (`data.json`) for simplicity and easy file-based persistence. The application allows you to perform operations on student data, including adding new records, reading all records, updating existing records, and deleting records based on the student's roll number.

## Project Definition and Explanation

### Endpoints

- **`GET /read_data`**: Reads and returns the entire content of `data.json`. If the file doesn't exist or is empty, an appropriate message is returned.
- **`POST /add_data`**: Adds a new student record to `data.json`. The data is provided in JSON format with fields like `name`, `roll_no`, `year`, `division`, and `age`.
- **`PUT /update_data?roll_no=<int>`**: Updates an existing student record in `data.json` based on the provided roll number.
- **`DELETE /delete_data?roll_no=<int>`**: Deletes a student record from `data.json` based on the provided roll number.

### Data Model

The application uses a simple data model defined by the `Data` class:

```python
class Data(BaseModel):
    name: str
    roll_no: int
    year: int
    division: str
    age: int
```

Each student record is stored as a dictionary in the JSON file with the following structure:

```json
{
  "name": "John Doe",
  "roll_no": 1,
  "year": 3,
  "division": "A",
  "age": 20
}
```

## Project Setup

### Prerequisites

- Python 3.7 or higher
- FastAPI
- Uvicorn (for running the FastAPI application)

### Installation

1. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

### Project Files

- **`main.py`**: The main FastAPI application file containing all CRUD operations.
- **`data.json`**: The JSON file where all student records are stored. This file is created automatically when you add the first record.

### How to Run the Project

1. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

   The application will be accessible at `http://127.0.0.1:8000`.

2. **Access the API documentation:**

   FastAPI provides an interactive API documentation at `http://127.0.0.1:8000/docs`. You can test the endpoints directly from the browser.

### Example Requests

- **Read Data:**

  ```bash
  curl -X 'GET' 'http://127.0.0.1:8000/read_data' -H 'accept: application/json'
  ```

- **Add Data:**

  ```bash
  curl -X 'POST' 'http://127.0.0.1:8000/add_data' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Jane Doe",
  "roll_no": 2,
  "year": 3,
  "division": "B",
  "age": 21
  }'
  ```

- **Update Data:**

  ```bash
  curl -X 'PUT' 'http://127.0.0.1:8000/update_data?roll_no=2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Jane Smith",
  "roll_no": 2,
  "year": 2,
  "division": "A",
  "age": 22
  }'
  ```

- **Delete Data:**

  ```bash
  curl -X 'DELETE' 'http://127.0.0.1:8000/delete_data?roll_no=2' \
  -H 'accept: application/json'
  ```
