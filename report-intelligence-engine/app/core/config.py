from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_anthropic import ChatAnthropic
from dotenv import  load_dotenv
import os

load_dotenv()
# Secure these via env vars in production
DB_URL = "postgresql+psycopg2://postgres:Success%402025@localhost:5432/entitlement"
ANTHROPIC_API_KEY = "sk-ant-api03-..."  # move to .env

engine = create_engine(DB_URL)
db = SQLDatabase(engine=engine, schema="dbo")

llm = ChatAnthropic(
    model="claude-3-opus-20240229",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    temperature=0
)