# GradingAgentAPI

CSCE 247 Grading Agent API

## Build Instructions

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8001
    ```

## API Documentation

### POST /assignments

Create a new assignment.

**Request Body:**

```json
{
  "assignment_name": "string"
}
```

### POST /assignments/{assignment_name}/criteria

Upload a criteria file for an assignment. The criteria file can be a `.txt`, `.docx`, or `.json` file.

**Request Body:**

-   `criteria_file`: The criteria file to upload.

### POST /grade

Grade an assignment.

**Request Body:**

```json
{
  "assignment_name": "string",
  "repo_link": "string",
  "token": "string"
}
```

### GET /grades

Get all grading results.

### GET /grades/{student_name}

Get all grading results for a specific student.

## Testing

To run the tests, run the following command:

```bash
pytest
```