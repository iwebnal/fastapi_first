from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, ValidationError

app = FastAPI(
    title="My FastApi app"
)


@app.exception_handler(ValidationError)
async def validation_exeption_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = jsonable_encoder({"detail": exc.errors()})
    )


fake_users = [
    {"id": 1, "role": "admin", "name": ["John"], "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "newbie"}
    ]},
    {"id": 2, "role": "user", "name": "Mike", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
    {"id": 3, "role": "manager", "name": "Ann", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "newbie"}
    ]},
    {"id": 4, "role": "emploee", "name": "Ivan", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
    {"id": 5, "role": "emploee1", "name": "Ivan"}
]

fake_users1 = [
    {"id": 1, "role": "admin", "name": "John"},
    {"id": 2, "role": "user", "name": "Mike"},
    {"id": 3, "role": "manager", "name": "Ann"},
    {"id": 4, "role": "emploee", "name": "Ivan"}
]

fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 135, "amount": 2.12}
]


@app.get("/")
def say_hello():
    return "Hello !!!"


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []   # optional property


# validation of data from the server
@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


#  validation with pydantic
class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=10)
    side: str
    price: float = Field(ge=0)
    amount: float


# client data validation
@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users1))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}

