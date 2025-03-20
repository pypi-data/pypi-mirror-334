from fastapi import FastAPI
from PROJECT_NAME.routes import ROUTE


app = FastAPI()

app.include_router(ROUTE.router)
