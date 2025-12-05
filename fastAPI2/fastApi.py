from typing import Optional, List, Annotated
from fastapi import (
    FastAPI,
    HTTPException,
    Path,
    Query,
    Body,
    Depends,
    BackgroundTasks,
    UploadFile,
    File,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, PositiveInt, constr
import uvicorn
import logging
import time
import uuid
import shutil
from pathlib import Path as SysPath

# -----------------------
# Logging setup
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("fastapi_app")

# -----------------------
# App & CORS
# -----------------------
app = FastAPI(title="Larger Example API", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Models (Pydantic v2 friendly)
# -----------------------

EmailStr = Annotated[str, Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")]

class UserCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    age: PositiveInt = Field(..., lt=130)
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    id: str
    name: str
    age: int
    email: Optional[str] = None


class MessageOut(BaseModel):
    message: str


# In-memory "DB"
DB = {}

# -----------------------
# Dependencies
# -----------------------
def api_key_auth(api_key: Optional[str] = Query(None, alias="api_key")):
    if api_key != "secret123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return True

# -----------------------
# Startup / Shutdown events
# -----------------------
@app.on_event("startup")
async def on_startup():
    logger.info("Starting app...")
    time.sleep(0.1)
    uploads = SysPath("uploads")
    if not uploads.exists():
        uploads.mkdir(parents=True)

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down app...")

# -----------------------
# ROUTES
# -----------------------

@app.get("/", response_model=MessageOut, tags=["health"])
def root():
    return {"message": "Server is up and running"}

@app.get("/hello", response_model=MessageOut, tags=["greeting"])
def say_hello(name: str = Query("Guest", min_length=1, max_length=50)):
    return {"message": f"Hello, {name}!"}

@app.get("/users/{user_id}", response_model=UserOut, tags=["users"])
def get_user(user_id: str = Path(...)):
    user = DB.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.get("/users", response_model=List[UserOut], tags=["users"])
def list_users(skip: int = Query(0), limit: int = Query(10, ge=1, le=100)):
    users = list(DB.values())
    return users[skip: skip + limit]

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(payload: UserCreate, auth: bool = Depends(api_key_auth)):
    new_id = str(uuid.uuid4())
    user = {
        "id": new_id,
        "name": payload.name,
        "age": payload.age,
        "email": payload.email,
    }
    DB[new_id] = user
    logger.info("Created user %s", new_id)
    return user

@app.post("/echo", response_model=MessageOut, tags=["utility"])
def echo_text(
    text: str = Body(..., embed=True, min_length=1, max_length=500)
):
    return {"message": f"You said: {text}"}

def long_background_job(task_name: str, duration: float = 2.0):
    logger.info("Background job %s started", task_name)
    time.sleep(duration)
    logger.info("Background job %s finished", task_name)

@app.post("/process", response_model=MessageOut, tags=["jobs"])
def start_process(background_tasks: BackgroundTasks, job_name: str = Body("job1")):
    background_tasks.add_task(long_background_job, job_name, 1.5)
    return {"message": f"Job {job_name} scheduled"}

@app.post("/upload", response_model=MessageOut, tags=["files"])
def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    dest = SysPath("uploads") / f"{file_id}_{file.filename}"
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"Saved file as {dest.name}"}

@app.get("/fail", tags=["errors"])
def always_fail():
    raise HTTPException(
        status_code=418,
        detail="This endpoint always fails — I'm a teapot"
    )

# -----------------------
# Run-able main
# -----------------------
if __name__ == "__main__":
    uvicorn.run("fastApi:app", host="127.0.0.1", port=8000, reload=True)
