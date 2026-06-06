from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# Order matters
@app.get("/users/me")
async def read_current_user():
    return {"user_id": "current"}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# Cannot redefine the same path operation. The first one will be used and the second one will be ignored.
# This will not cause an error, but it is not recommended to have duplicate path operations.
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Mei", "Szymek"]


# Enum example
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # match model_name:
    #     case ModelName.alexnet:
    #         return {"model_name": model_name}
    #     case ModelName.resnet:
    #         return {"model_name": model_name}
    #     case ModelName.lenet:
    #         return {"model_name": model_name}
    if model_name == ModelName.alexnet:
        return {"model_name": model_name}

    if model_name.value == "resnet":
        return {"model_name": model_name}
