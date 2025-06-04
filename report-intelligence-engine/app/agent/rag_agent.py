from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent
from app.core.config import db,llm

def create_agent():
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        max_execution_time=60
    )
    return agent