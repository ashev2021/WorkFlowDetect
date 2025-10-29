import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a TestClient instance for the FastAPI application.
    This fixture is automatically injected into test functions that declare it as a parameter.
    
    Returns:
        TestClient: FastAPI test client for making HTTP requests to the application
    """
    return TestClient(app)


@patch("src.services.language_model.LLMService.call_llm", new_callable=AsyncMock)
def test_suggest_steps_multiple_valid_and_invalid_descriptions(mock_call_llm, client):
    """
    Test the /suggest_steps endpoint with a mix of valid and invalid workflow descriptions.
    
    This test verifies that:
    1. Valid workflow descriptions are correctly processed and return expected app/action pairs
    2. Invalid/non-workflow text is properly rejected with appropriate error messages
    3. The API can handle batch processing of multiple steps in a single request
    
    Args:
        mock_call_llm: Mocked LLM service to control responses without making real API calls
        client: FastAPI test client fixture
    """
    # Mock different LLM responses for each workflow step description
    # First two are valid workflows, third is invalid non-workflow text
    mock_call_llm.side_effect = [
        {"app_name": "gmail", "action_name": "send_email"},      # Valid Gmail workflow
        {"app_name": "slack", "action_name": "send_message"},   # Valid Slack workflow
        {"app_name": None, "action_name": None},                # Invalid - not a workflow
    ]

    # Test payload with mixed valid and invalid workflow descriptions
    payload = {
        "workflow_step_descriptions": [
            "Send a welcome email to new leads using Gmail",  # Should map to gmail/send_email
            "Post a message to Slack",                        # Should map to slack/send_message
            "Random text not a workflow",                     # Should be rejected as invalid
        ]
    }
    
    # Make API request and verify basic response structure
    response = client.post("/suggest_steps", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 3  # Should return results for all 3 inputs

    # Verify first valid workflow step is correctly processed
    assert data["results"][0]["app_name"] == "gmail"
    assert data["results"][0]["action_name"] == "send_email"
    assert data["results"][0]["error"] is None  # No error for valid workflow

    # Verify second valid workflow step is correctly processed
    assert data["results"][1]["app_name"] == "slack"
    assert data["results"][1]["action_name"] == "send_message"
    assert data["results"][1]["error"] is None  # No error for valid workflow

    # Verify invalid workflow step is properly rejected
    assert data["results"][2]["app_name"] is None      # No app returned for invalid input
    assert data["results"][2]["action_name"] is None   # No action returned for invalid input
    assert "Could not map description" in data["results"][2]["error"]  # Appropriate error message


@patch("src.services.language_model.LLMService.call_llm", new_callable=AsyncMock)
def test_suggest_steps_empty_description(mock_call_llm, client):
    """
    Test the API's handling of empty or very short workflow descriptions.
    
    This test ensures that the API validates input length and rejects empty strings
    before even calling the LLM service, providing immediate feedback to users.
    
    Args:
        mock_call_llm: Mocked LLM service (should not be called for empty input)
        client: FastAPI test client fixture
    """
    # Mock LLM response (though it shouldn't be called for empty input)
    mock_call_llm.return_value = {"app_name": None, "action_name": None}
    
    # Test with empty string description
    payload = {"workflow_step_descriptions": [""]}
    response = client.post("/suggest_steps", json=payload)
    
    # Verify response structure and error handling
    assert response.status_code == 200
    data = response.json()
    # Should return specific error message for empty descriptions
    assert data["results"][0]["error"] == "Description too short or empty, please provide a valid workflow step."


@patch("src.services.language_model.LLMService.call_llm", new_callable=AsyncMock)
def test_suggest_steps_unsupported_app(mock_call_llm, client):
    """
    Test the API's handling of requests for unsupported or private applications.
    
    This test verifies the business requirement that private apps should be flagged
    as unsupported to prevent users from trying to use apps they don't have access to.
    
    Args:
        mock_call_llm: Mocked LLM service returning an unsupported app
        client: FastAPI test client fixture
    """
    # Mock LLM returning a private/unsupported app that should be rejected
    mock_call_llm.return_value = {"app_name": "private_app", "action_name": "do_something"}
    
    payload = {"workflow_step_descriptions": ["Use a private app"]}
    response = client.post("/suggest_steps", json=payload)
    
    # Verify that unsupported apps are properly flagged
    assert response.status_code == 200
    data = response.json()
    # Should contain specific error message about unsupported/private apps
    assert "not supported or is private" in data["results"][0]["error"]


@patch("src.services.language_model.LLMService.call_llm", new_callable=AsyncMock)
def test_suggest_steps_unsupported_action(mock_call_llm, client):
    """
    Test the API's handling of requests for unsupported actions within supported apps.
    
    This test ensures that even if an app is supported (like Gmail), the API properly
    validates that the requested action is also supported for that specific app.
    
    Args:
        mock_call_llm: Mocked LLM service returning an unsupported action
        client: FastAPI test client fixture
    """
    # Mock LLM returning a supported app but unsupported action
    mock_call_llm.return_value = {"app_name": "gmail", "action_name": "unknown_action"}
    
    payload = {"workflow_step_descriptions": ["Do an unsupported action"]}
    response = client.post("/suggest_steps", json=payload)
    
    # Verify that unsupported actions are properly flagged
    assert response.status_code == 200
    data = response.json()
    # Should contain specific error message about unsupported actions
    assert "not supported for the app" in data["results"][0]["error"]


@pytest.mark.parametrize("payload", [
    {},  # Missing required field - no 'workflow_step_descriptions' key
    {"workflow_step_descriptions": None},  # Invalid value - None instead of list
    {"workflow_step_descriptions": "not a list"},  # Invalid type - string instead of list
])
def test_invalid_request_payloads(client, payload):
    """
    Test the API's input validation using parameterized testing for various invalid payloads.
    
    This test uses pytest's parametrize decorator to test multiple invalid request formats
    in a single test function, ensuring comprehensive validation coverage.
    
    The test verifies that the API properly validates:
    - Required fields are present
    - Field values are of correct type (list)
    - Field values are not None when they should contain data
    
    Args:
        client: FastAPI test client fixture
        payload: Parameterized test data containing various invalid request payloads
    """
    response = client.post("/suggest_steps", json=payload)
    # FastAPI's Pydantic validation should return 422 for invalid request schemas
    assert response.status_code == 422  # Unprocessable Entity - validation error
