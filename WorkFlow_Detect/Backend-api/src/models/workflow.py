from pydantic import BaseModel
from typing import List, Optional

class WorkflowStepsRequest(BaseModel):
    workflow_step_descriptions: List[str]

class StepResult(BaseModel):
    app_name: Optional[str]
    action_name: Optional[str]
    error: Optional[str] = None

class MultipleStepResponse(BaseModel):
    results: List[StepResult]
