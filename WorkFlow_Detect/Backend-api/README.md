# Python Workflow API

This project is a simple API service that processes plain text descriptions of workflow steps using a language model. It is built with FastAPI and designed to be easily extendable.

## Project Structure

```
python-workflow-api
├── src
│   ├── main.py                # Entry point of the application
│   ├── api
│   │   ├── __init__.py        # Marks the api directory as a package
│   │   └── endpoints.py       # Defines API endpoints for processing workflow steps
│   ├── models
│   │   ├── __init__.py        # Marks the models directory as a package
│   │   └── workflow.py        # Defines data models for workflow steps
│   ├── services
│   │   ├── __init__.py        # Marks the services directory as a package
│   │   └── language_model.py   # Logic for interacting with the language model
│   └── utils
│       ├── __init__.py        # Marks the utils directory as a package
│       └── helpers.py         # Utility functions for validation and formatting
├── tests
│   ├── __init__.py            # Marks the tests directory as a package
│   └── test_api.py            # Unit tests for the API endpoints
├── requirements.txt            # Lists dependencies required for the project
├── .env.example                # Example of environment variables needed for the application
└── README.md                   # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-workflow-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables by copying `.env.example` to `.env` and modifying it as needed.

## Usage

To run the API, execute the following command:
```
uvicorn src.main:app --reload
```

You can then access the API at `http://127.0.0.1:8000`.

## API Endpoints

- **POST /workflow**: Process a workflow step description.
  
  Request body:
  ```json
  {
  "workflow_step_descriptions": [
    "Send a welcome email to new leads using Gmail",
    "Post a message to a Slack channel",
    "Random text not a workflow"
  ]
}
  

  Response:
  ```json
  {
  "results": [
    {
      "app_name": "gmail",
      "action_name": "send_email",
      "error": null
    },
    {
      "app_name": "slack",
      "action_name": "send_message",
      "error": null
    },
    {
      "app_name": null,
      "action_name": null,
      "error": "Could not map description to a workflow step."
    }
  ]
}
  ```

