from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.agents import initialize_agent
from langchain_anthropic import ChatAnthropic
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine,text

claude_api_key=""

app = FastAPI(title="Ask-Anything-AI", description="Query your data with natural language", version="1.0")


engine = create_engine("postgresql+psycopg2://postgres:password%40password@localhost:5432/db_name")
db = SQLDatabase(engine=engine, schema="dbo")
llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=claude_api_key, temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)


agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True,
)

class QueryRequest(BaseModel):
    question: str


# API Endpoint
@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        response = agent.run(request.question)
        return {"question": request.question, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# question = "Show user's average per capita income group by the gender"
# response = agent.run(question)