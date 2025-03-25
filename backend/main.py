from fastapi import FastAPI
import uvicorn
from hadnlers import spending_router, users_router


app = FastAPI()

app.include_router(spending_router)
app.include_router(users_router)
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8000)