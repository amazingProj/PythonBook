from fastapi import FastAPI
from view.routes import router
from constant import API_PREFIX

app = FastAPI()

app.include_router(router, prefix=API_PREFIX)


@app.get("/")
def alive_message():
    return "alive"


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)

