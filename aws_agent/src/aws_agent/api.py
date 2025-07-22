from fastapi import FastAPI, Request
from pydantic import BaseModel
from .crew import AwsAgent
from .tools.appinsights_logger import log_event
from uuid import uuid4
import uvicorn

app = FastAPI()

class CrewRequest(BaseModel):
    topic: str
    session_id: str

@app.post("/run-agent")
async def run_agent(request: CrewRequest):    
    interaction_id = str(uuid4())
    inputs = {
        'topic': request.topic,
        'session_id': request.session_id
    }
    try:
        log_event(
            event_type="llamada",
            payload={"input": inputs},
            session_id=request.session_id,
            interaction_id=interaction_id
        )
        result = AwsAgent().crew().kickoff(inputs=inputs)
        log_event(
            event_type="respuesta",
            payload={"output": result.raw},
            session_id=request.session_id,
            interaction_id=interaction_id
        )
        return {"result": result.raw}
    except Exception as e:
        log_event(
            event_type="error",
            payload={"error": str(e)},
            session_id=request.session_id,
            interaction_id=interaction_id
        )
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
