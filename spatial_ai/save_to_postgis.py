import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="sig_123140045",
    user="postgres",
    password="admin123"
)

with open("output/detections.geojson", "r") as f:
    geojson = json.load(f)

cur = conn.cursor()

for feature in geojson["features"]:
    coords = feature["geometry"]["coordinates"]
    props = feature["properties"]

    cur.execute("""
        INSERT INTO detections (class_name, confidence, geom)
        VALUES (%s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))
    """, (
        props["class_name"],
        props["confidence"],
        coords[0],
        coords[1]
    ))

conn.commit()
cur.close()
conn.close()

print("Hasil deteksi berhasil disimpan ke PostGIS")