from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.services.language_model import LLMService

from src.utils import is_supported_app, is_supported_action


router = APIRouter()

class WorkflowStepsRequest(BaseModel):
    workflow_step_descriptions: List[str]

class StepResult(BaseModel):
    app_name: Optional[str]
    action_name: Optional[str]
    error: Optional[str] = None

class MultipleStepResponse(BaseModel):
    results: List[StepResult]

llm_service = LLMService()

@router.post("/suggest_steps", response_model=MultipleStepResponse)
async def suggest_steps(req: WorkflowStepsRequest):
    results = []
    for step_description in req.workflow_step_descriptions:
        step_desc = step_description.strip()
        if not step_desc or len(step_desc) < 5:
            results.append(StepResult(
                app_name=None,
                action_name=None,
                error="Description too short or empty, please provide a valid workflow step."
            ))
            continue
        try:
            result = await llm_service.call_llm(step_desc)
        except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))
        
        app_name = result.get("app_name")
        action_name = result.get("action_name")
        
        if app_name is None or action_name is None:
            results.append(StepResult(
                app_name=None,
                action_name=None,
                error="Could not map description to a workflow step."
            ))
            continue
        
        if not is_supported_app(app_name):
            results.append(StepResult(
                app_name=None,
                action_name=None,
                error=f"The app '{app_name}' is not supported or is private."
            ))
            continue
        
        if not is_supported_action(app_name, action_name):
            results.append(StepResult(
                app_name=None,
                action_name=None,
                error=f"The action '{action_name}' is not supported for the app '{app_name}'."
            ))
            continue
        
        results.append(StepResult(
            app_name=app_name,
            action_name=action_name,
            error=None
        ))
    return MultipleStepResponse(results=results)
