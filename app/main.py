from fastapi import FastAPI
import uvicorn

app = FastAPI(title='Trading App')

@app.get("/users")
async def get_user():
    return {"message": "test"}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)