from fastapi import FastAPI


from app.api import routes


app = FastAPI(
    title="Ask-Anything-AI",
    description="Query your data with natural language",
    version="1.0"
)

app.include_router(routes.router)