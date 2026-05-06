from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import psycopg2

app = FastAPI(title="WebGIS API Tugas 9")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Database Connection
# =========================
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="sig_123140045",
    user="postgres",
    password="admin123"
)

# =========================
# JWT Config
# =========================
SECRET_KEY = "secret-key-muharyan-123140045"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================
# Pydantic Models
# =========================
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class FasilitasCreate(BaseModel):
    nama: str
    jenis: str
    alamat: str
    longitude: float
    latitude: float

class FasilitasUpdate(BaseModel):
    nama: Optional[str] = None
    jenis: Optional[str] = None
    alamat: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

# =========================
# JWT Utility
# =========================
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# =========================
# Root
# =========================
@app.get("/")
def root():
    return {"message": "API SIG 123140045 aktif"}

# =========================
# REGISTER
# =========================
@app.post("/register")
def register(user: UserRegister):
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    existing = cur.fetchone()
    if existing:
        cur.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = pwd_context.hash(user.password)

    cur.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id, email",
        (user.email, password_hash)
    )
    new_user = cur.fetchone()
    conn.commit()
    cur.close()

    return {
        "id": new_user[0],
        "email": new_user[1]
    }

# =========================
# LOGIN
# =========================
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password_hash FROM users WHERE email = %s",
        (form_data.username,)
    )
    user = cur.fetchone()
    cur.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(form_data.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user[1]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# =========================
# WILAYAH GEOJSON
# =========================
@app.get("/api/wilayah/geojson")
def get_wilayah_geojson():
    cur = conn.cursor()
    cur.execute("""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::json,
                    'properties', json_build_object(
                        'id', id,
                        'nama', nama
                    )
                )
            ), '[]'::json)
        )
        FROM wilayah
        WHERE geom IS NOT NULL;
    """)
    data = cur.fetchone()[0]
    cur.close()
    return data

# =========================
# FASILITAS GEOJSON
# =========================
@app.get("/api/fasilitas/geojson")
def get_fasilitas_geojson():
    cur = conn.cursor()
    cur.execute("""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::json,
                    'properties', json_build_object(
                        'id', id,
                        'nama', nama,
                        'jenis', jenis,
                        'alamat', alamat
                    )
                )
            ), '[]'::json)
        )
        FROM fasilitas
        WHERE geom IS NOT NULL;
    """)
    data = cur.fetchone()[0]
    cur.close()
    return data

# =========================
# READ FASILITAS
# =========================
@app.get("/api/fasilitas")
def get_fasilitas(jenis: Optional[str] = None, limit: int = 100, offset: int = 0):
    cur = conn.cursor()

    if jenis:
        cur.execute("""
            SELECT id, nama, jenis, alamat, ST_X(geom) AS lon, ST_Y(geom) AS lat
            FROM fasilitas
            WHERE jenis = %s
            ORDER BY nama
            LIMIT %s OFFSET %s
        """, (jenis, limit, offset))
    else:
        cur.execute("""
            SELECT id, nama, jenis, alamat, ST_X(geom) AS lon, ST_Y(geom) AS lat
            FROM fasilitas
            ORDER BY nama
            LIMIT %s OFFSET %s
        """, (limit, offset))

    rows = cur.fetchall()
    cur.close()

    return [
        {
            "id": row[0],
            "nama": row[1],
            "jenis": row[2],
            "alamat": row[3],
            "lon": row[4],
            "lat": row[5]
        }
        for row in rows
    ]

# =========================
# READ FASILITAS BY ID
# =========================
@app.get("/api/fasilitas/{id}")
def get_fasilitas_by_id(id: int):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nama, jenis, alamat, ST_X(geom) AS lon, ST_Y(geom) AS lat
        FROM fasilitas
        WHERE id = %s
    """, (id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")

    return {
        "id": row[0],
        "nama": row[1],
        "jenis": row[2],
        "alamat": row[3],
        "lon": row[4],
        "lat": row[5]
    }

# =========================
# CREATE FASILITAS
# =========================
@app.post("/api/fasilitas", status_code=201)
def create_fasilitas(data: FasilitasCreate, user: str = Depends(get_current_user)):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fasilitas (nama, jenis, alamat, geom)
        VALUES (%s, %s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))
        RETURNING id, nama, jenis
    """, (data.nama, data.jenis, data.alamat, data.longitude, data.latitude))

    row = cur.fetchone()
    conn.commit()
    cur.close()

    return {
        "id": row[0],
        "nama": row[1],
        "jenis": row[2]
    }

# =========================
# UPDATE FASILITAS
# =========================
@app.put("/api/fasilitas/{id}")
def update_fasilitas(id: int, data: FasilitasUpdate, user: str = Depends(get_current_user)):
    cur = conn.cursor()

    # ambil data lama dulu
    cur.execute("""
        SELECT nama, jenis, alamat, ST_X(geom) AS lon, ST_Y(geom) AS lat
        FROM fasilitas
        WHERE id = %s
    """, (id,))
    existing = cur.fetchone()

    if not existing:
        cur.close()
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")

    nama_baru = data.nama if data.nama is not None else existing[0]
    jenis_baru = data.jenis if data.jenis is not None else existing[1]
    alamat_baru = data.alamat if data.alamat is not None else existing[2]
    lon_baru = data.longitude if data.longitude is not None else existing[3]
    lat_baru = data.latitude if data.latitude is not None else existing[4]

    cur.execute("""
        UPDATE fasilitas
        SET nama = %s,
            jenis = %s,
            alamat = %s,
            geom = ST_SetSRID(ST_Point(%s, %s), 4326)
        WHERE id = %s
        RETURNING id, nama, jenis
    """, (nama_baru, jenis_baru, alamat_baru, lon_baru, lat_baru, id))

    row = cur.fetchone()
    conn.commit()
    cur.close()

    return {
        "id": row[0],
        "nama": row[1],
        "jenis": row[2]
    }

# =========================
# DELETE FASILITAS
# =========================
@app.delete("/api/fasilitas/{id}", status_code=204)
def delete_fasilitas(id: int, user: str = Depends(get_current_user)):
    cur = conn.cursor()
    cur.execute("DELETE FROM fasilitas WHERE id = %s RETURNING id", (id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    

@app.get("/api/detections/geojson")
def get_detections_geojson():
    cur = conn.cursor()
    cur.execute("""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::json,
                    'properties', json_build_object(
                        'id', id,
                        'class_name', class_name,
                        'confidence', confidence,
                        'detected_at', detected_at
                    )
                )
            ), '[]'::json)
        )
        FROM detections
        WHERE geom IS NOT NULL;
    """)
    data = cur.fetchone()[0]
    cur.close()
    return data