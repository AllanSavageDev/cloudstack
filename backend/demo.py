from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
import psycopg2
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

# --- App ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running lifespan hook...")
    ensure_users_table_exists()
    ensure_items_table_exists()
    yield

app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def get_connection():

#     print("Connecting to DB with settings:")
#     print("DB_NAME =", os.getenv("DB_NAME", "cloudstack"))
#     print("DB_USER =", os.getenv("DB_USER", "postgres"))
#     print("DB_PASSWORD =", os.getenv("DB_PASSWORD", "secret"))
#     print("DB_HOST =", os.getenv("DB_HOST", "db"))
#     print("DB_PORT =", os.getenv("DB_PORT", 5432))

#     return psycopg2.connect(
#         dbname=os.getenv("DB_NAME", "cloudstack"),
#         user=os.getenv("DB_USER", "postgres"),
#         password=os.getenv("DB_PASSWORD", "secret"),
#         host=os.getenv("DB_HOST", "db"),
#         port=int(os.getenv("DB_PORT", 5432))
#     )

import time
def get_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                dbname=os.getenv("DB_NAME", "cloudstack"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "secret"),
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", 5432)
            )
        except psycopg2.OperationalError:
            print("DB not ready yet, retrying...")
            time.sleep(2)
    raise Exception("DB connection failed after multiple retries")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- Auth Config ---
SECRET_KEY = "demo_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class Item(BaseModel):
    id: int | None = None
    name: str
    description: str




# --- DB Setup ---
def ensure_users_table_exists():
    print("Creating users table if not exists...")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)

            cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", ("demo@demo.com",))
            if cur.fetchone()[0] == 0:
                hashed = hash_password("password")
                cur.execute("""
                    INSERT INTO users (email, hashed_password, is_active)
                    VALUES (%s, %s, true)
                """, ("demo@demo.com", hashed))

            conn.commit()



def ensure_items_table_exists():
    print("Creating items table if not exists...")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    owner_email TEXT NOT NULL
                );
            """)
            conn.commit()






# --- Auth Logic ---
def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Routes ---
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT hashed_password FROM users WHERE email = %s AND is_active = true",
                (email,),
            )
            row = cur.fetchone()

    #if not row or row[0] != password:  # TODO: hash check later
    if not row or not verify_password(password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"email": current_user}


@app.post("/items")
def create_item(item: Item, user_email=Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO items (name, description, owner_email) VALUES (%s, %s, %s) RETURNING id",
                (item.name, item.description, user_email),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return {"id": new_id, **item.dict()}

@app.get("/items")
def list_items(user_email=Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM items WHERE owner_email = %s", (user_email,))
            rows = cur.fetchall()
            return [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, user_email=Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET name = %s, description = %s WHERE id = %s AND owner_email = %s",
                (item.name, item.description, item_id, user_email),
            )
            conn.commit()
            return {"id": item_id, **item.dict()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, user_email=Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM items WHERE id = %s AND owner_email = %s",
                (item_id, user_email),
            )
            conn.commit()
            return {"message": "Item deleted"}

