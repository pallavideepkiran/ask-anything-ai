from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.agent.rag_agent import create_agent

router = APIRouter()

agent = create_agent()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        prompt = f"""
You are a financial analyst AI. Given the following natural language question: 
"{request.question}"

Use the SQL database tool to get the answer. Return the final result ONLY as structured JSON. 
Do NOT include explanation, SQL, or formatting.

Format:
{{
  "question": "...",
  "summary": "...",
  "result": [{{ ... }}]
}}
"""

        raw_response = agent.invoke({"input": prompt})
        output_text = raw_response.get("output", "").strip()
        print("RAW AGENT OUTPUT:\n", output_text)

        try:
            cleaned = output_text.replace("```json", "").replace("```", "")
            parsed = json.loads(cleaned)
        except Exception:
            raise HTTPException(status_code=500, detail=f"Agent response was not valid JSON:\n{output_text}")

        return parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))