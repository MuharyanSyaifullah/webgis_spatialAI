import cv2
import json
import os

IMAGE_PATH = "images/mobil2.jpg"
OUTPUT_GEOJSON = "output/detections.geojson"
OUTPUT_IMAGE = "output/detection_result.jpg"
MANUAL_DETECTIONS = [
    {"bbox": [330, 370, 435, 585], "class_name": "car", "confidence": 0.95},
    {"bbox": [465, 605, 560, 835], "class_name": "car", "confidence": 0.96}
]

MANUAL_GEO_POINTS = [
    {"lon": 106.811678, "lat": -6.315336},
    {"lon": 106.811700, "lat": -6.315378}
]

def draw_detections(image, detections, output_path):
    img_copy = image.copy()

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        class_name = det["class_name"]
        confidence = det["confidence"]

        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            img_copy,
            f"{class_name} ({confidence:.2f})",
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    cv2.imwrite(output_path, img_copy)

def export_to_geojson(detections, geo_points, output_path):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for i, (det, geo) in enumerate(zip(detections, geo_points), start=1):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [geo["lon"], geo["lat"]]
            },
            "properties": {
                "id": i,
                "class_name": det["class_name"],
                "confidence": det["confidence"]
            }
        }
        geojson["features"].append(feature)

    with open(output_path, "w") as f:
        json.dump(geojson, f, indent=2)

def main():
    os.makedirs("output", exist_ok=True)

    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise FileNotFoundError(f"Gagal membaca citra: {IMAGE_PATH}")

    draw_detections(image, MANUAL_DETECTIONS, OUTPUT_IMAGE)
    export_to_geojson(MANUAL_DETECTIONS, MANUAL_GEO_POINTS, OUTPUT_GEOJSON)

    print(f"Jumlah deteksi: {len(MANUAL_DETECTIONS)}")
    print(f"Hasil gambar: {OUTPUT_IMAGE}")
    print(f"Hasil GeoJSON: {OUTPUT_GEOJSON}")

if __name__ == "__main__":
    main()