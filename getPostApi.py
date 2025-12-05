from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -----------------------
# SIMPLE GET ROUTE
# -----------------------
@app.get("/hello")
def say_hello(name: str = "Guest"):
    return {"message": f"Hello, {name}!"}


# -----------------------
# SIMPLE POST ROUTE
# -----------------------
class UserInput(BaseModel):
    name: str
    age: int

@app.post("/info")
def user_info(data: UserInput):
    return {
        "message": f"Hello {data.name}, you are {data.age} years old."
    }
