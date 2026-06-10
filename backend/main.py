from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, AfterValidator
from typing import Annotated
import random

from fastapi import Query, Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


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
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items")
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "This is an amazing item that has a long description"})
#     return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# @app.get("/items/")
# async def read_items(
#     q: Annotated[str | None, Query(min_length=5)] = "fixedquery",
# ):
#     results: dict[str, list[dict[str, str]] | str] = {
#         "items": [{"item_id": "Foo"}, {"item_id": "Bar"}]
#     }
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         list[str],
#         Query(
#             title="Search queries",
#             description="List of search queries",
#             alias="item-query",
#             min_length=3,
#             deprecated=True,
#             include_in_schema=False,
#         ),
#     ] = ["foo", "bar"]
# ):
#     query_items = {"q": q}
#     return query_items

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID, it must start with 'isbn-' or 'imdb-'")
    return id


@app.get("/items/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id, "Item not found")
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "item": item}


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results: dict[str, int | str] = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


if __name__ == "__main__":
    import requests
    from pprint import pp

    print(list(data.items()))

    # url = "http://127.0.0.1:8000"
    # headers = {"Content-Type": "application/json"}
    # data = {"name": 42, "price": 42.0, "description": "this is a good item"}
    # r = requests.post(f"{url}/items/", headers=headers, json=data)
    # pp(r.json())
    # print(r.status_code)

    # get = requests.get("https://www.w3schools.com/python")
    # print(get.json())
