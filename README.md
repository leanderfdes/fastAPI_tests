# 🚀 FastAPI Tests – Learning & Practice Project

This repository contains a basic FastAPI project used for testing and learning API development concepts.  
It includes examples of GET and POST endpoints, request validation, file uploads, simple authentication, and background task execution.

---

## 📁 Project Structure

fastAPI_tests/
│
├── fastAPI2/
│ ├── fastApi.py # Main FastAPI application
│ ├── uploads/ # Auto-created folder for uploaded files
│ ├── pycache/ # Python cache (ignored)
│ └── requirements.txt # Dependency list
│
├── getPostApi.py # Additional test script
├── .gitignore
└── .venv/ # Virtual environment (ignored)

yaml
Copy code

---

## ⚙️ Features Included

- FastAPI backend with auto reload
- GET / POST routes
- Query parameters and path parameters
- Pydantic v2 request validation
- File upload endpoint
- Background task example
- Simple API key authentication demo
- CORS enabled for frontend usage
- Interactive Swagger docs at `/docs`

---

## ▶️ Run the Project Locally

### **1. Clone the Repository**
```bash
git clone https://github.com/leanderfdes/fastAPI_tests.git
cd fastAPI_tests
2. Create & Activate a Virtual Environment
bash
Copy code
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install -r fastAPI2/requirements.txt
4. Start the FastAPI Server
bash
Copy code
cd fastAPI2
uvicorn fastApi:app --reload
Server will run at:
📌 http://127.0.0.1:8000
📘 Swagger UI → http://127.0.0.1:8000/docs

📚 API Endpoints Overview
Health Check
http
Copy code
GET /
Greeting
http
Copy code
GET /hello?name=YourName
Users
Method	Endpoint	Description
GET	/users	Get all users (in-memory)
GET	/users/{id}	Get user by UUID
POST	/users	Create user (requires api_key=secret123)

Echo Text
http
Copy code
POST /echo
Start Background Task
http
Copy code
POST /process
File Upload
http
Copy code
POST /upload
Intentional Error
http
Copy code
GET /fail
📦 Requirements
All Python package requirements are located in:

bash
Copy code
fastAPI2/requirements.txt
Install using:

bash
Copy code
pip install -r fastAPI2/requirements.txt

🔮 Future Improvements
Add database integration (PostgreSQL / MongoDB)

JWT authentication

Move to industry-standard folder structure (app/routers/...)

Add Docker support

Add test suite with pytest
