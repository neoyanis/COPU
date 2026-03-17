from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from deta import Deta
import hashlib

app = FastAPI()

# Deta config
deta = Deta()
users_db = deta.Base("users")
projects_db = deta.Base("projects")

# Static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# REGISTER
@app.post("/register")
async def register(req: Request):
    data = await req.json()
    email = data["email"]
    password = hash_password(data["password"])

    if users_db.get(email):
        return {"error": "User exists"}

    users_db.put({
        "key": email,
        "password": password
    })

    return {"success": True}

# LOGIN
@app.post("/login")
async def login(req: Request):
    data = await req.json()
    email = data["email"]
    password = hash_password(data["password"])

    user = users_db.get(email)

    if not user or user["password"] != password:
        return {"error": "Invalid credentials"}

    return {"success": True}

# CREATE PROJECT
@app.post("/create-project")
async def create_project(req: Request):
    data = await req.json()

    projects_db.put({
        "key": data["name"],
        "owner": data["email"],
        "code": ""
    })

    return {"success": True}

# SAVE CODE
@app.post("/save")
async def save(req: Request):
    data = await req.json()

    projects_db.put({
        "key": data["name"],
        "owner": data["email"],
        "code": data["code"]
    })

    return {"success": True}

# GET PROJECT
@app.get("/project/{name}")
def get_project(name: str):
    return projects_db.get(name)
