from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_anthropic import ChatAnthropic
from sqlalchemy import create_engine
from langchain.agents import initialize_agent
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
import json

claude_api_key=""

app = FastAPI(title="Ask-Anything-AI", description="Query your data with natural language", version="1.0")


engine = create_engine("postgresql+psycopg2://postgres:password%40password@localhost:5432/db_name")
db = SQLDatabase(engine=engine, schema="dbo")
llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=claude_api_key, temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent_type="zero-shot-react-description",
#         verbose=True,
#     ),
#     tools=tools,
#     handle_parsing_errors=True,  # 👈 This tells it to retry if parsing fails
# )

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,  # <-- pass this here to enable parsing retry
)
class QueryRequest(BaseModel):
    question: str


# API Endpoint
@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        # Build the custom prompt
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

        # Run the agent
        raw_response = agent.invoke({"input": prompt})
        output_text = raw_response["output"]
        print("RAW AGENT OUTPUT:\n", output_text)
        try:
            parsed = json.loads(output_text)
        except Exception:
            raise HTTPException(status_code=500, detail=f"Agent response was not valid JSON:\n{output_text}")

        return parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# question = "Show user's average per capita income group by the gender"
# response = agent.run(question)