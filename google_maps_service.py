# google_maps_service.py
import os, math, re, requests
GOOGLE_MAPS_API_KEY = "AIzaSyDeR71F-MwYPNnJZUNP1I-xyfCjybdw4MA"
# למעלה בקובץ
CITY_COORDS = {
    "Tel Aviv": (32.0853, 34.7818),
    "Jerusalem": (31.7683, 35.2137),
    "Haifa": (32.7940, 34.9896),
    "Beer Sheva": (31.252973, 34.791462),
    "Holon": (32.0158, 34.7874),
    "Petah Tikva": (32.0871, 34.8853),
    "Rishon LeZion": (31.9643, 34.8044),
    "Netanya": (32.3215, 34.8532),
    "Kfar Ahim": (31.7440, 34.7460),   # ≈ קואורדינטה משוערת, מספיק ל‑offline
}

CITY_ALIASES = {
    "Tel Aviv": ["tel aviv-yafo", "tel aviv yafo", "yafo", "תל אביב", "תל אביב-יפו", "תל אביב יפו"],
    "Jerusalem": ["yerushalayim", "jerusalem", "ירושלים"],
    "Haifa": ["haifa", "חיפה"],
    "Beer Sheva": ["beer sheva", "be'er sheva", "באר שבע"],
    "Holon": ["holon", "חולון"],
    "Petah Tikva": ["petah tikva", "petach tikva", "פתח תקווה", "פתח תקוה"],
    "Rishon LeZion": ["rishon lezion", "rishon le-zion", "ראשון לציון"],
    "Netanya": ["netanya", "נתניה"],
    "Kfar Ahim": ["kfar ahim", "kfar-achim", "כפר אחים"],  # חדש
}


def _norm(s: str) -> str:
    s = re.sub(r"[^A-Za-zא-ת\s\-']", " ", s or "")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def _coerce_to_city(name: str) -> str | None:
    """
    מנסה להוציא שם עיר מתוך כתובת חופשית:
    1) התאמה ישירה לשמות המילון
    2) חיפוש אליאסים/מופעים בתוך המחרוזת
    3) ניסיון לקחת את אחד הטוקנים האחרונים אחרי פסיקים
    """
    if not name:
        return None
    n = _norm(name)

    # 1) התאמה ישירה
    for city in CITY_COORDS.keys():
        if _norm(city) == n:
            return city

    # 2) אליאסים/מופעים
    for city, aliases in CITY_ALIASES.items():
        if any(alias in n for alias in aliases):
            return city

    # 3) נסה “לקצץ” לפי פסיקים ולבדוק מהסוף
    parts = [p.strip() for p in name.split(",")]
    for part in reversed(parts):
        npart = _norm(part)
        # בדיקה מול אליאסים ושמות
        for city in CITY_COORDS.keys():
            if _norm(city) == npart:
                return city
        for city, aliases in CITY_ALIASES.items():
            if any(alias == npart for alias in aliases):
                return city

    return None

def _haversine_km(a, b):
    R = 6371.0
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.atan2(math.sqrt(h), math.sqrt(1 - h))

def offline_estimate(origin: str, dest: str):
    ocity = _coerce_to_city(origin)
    dcity = _coerce_to_city(dest)
    if not ocity or not dcity:
        raise RuntimeError(f"Offline mode: unknown location(s): '{origin}' → '{dest}'")
    oa, da = CITY_COORDS[ocity], CITY_COORDS[dcity]
    dist_km = _haversine_km(oa, da)
    speed_kmh = 40 if dist_km < 15 else 70
    dur_min = (dist_km / speed_kmh) * 60
    return {"distance_km": dist_km, "duration_min": dur_min}

class GoogleMapsService:
    @staticmethod
    def get_distance_and_duration(origin_address: str, dest_address: str, *, allow_fallback: bool = True):
        key = GOOGLE_MAPS_API_KEY
        try:
            if not key:
                raise RuntimeError("GOOGLE_MAPS_API_KEY not set")

            resp = requests.get(
                "https://maps.googleapis.com/maps/api/distancematrix/json",
                params={
                    "origins": origin_address,
                    "destinations": dest_address,
                    "key": key,
                    "mode": "driving",
                    "language": "he",
                },
                timeout=8
            )
            data = resp.json()
            if data.get("status") != "OK":
                raise RuntimeError(f"Google Maps API error: {data}")
            el = data["rows"][0]["elements"][0]
            if el.get("status") != "OK":
                raise RuntimeError(f"Element error: {el}")

            return {
                "distance_km": el["distance"]["value"] / 1000.0,
                "duration_min": el["duration"]["value"] / 60.0
            }

        except Exception as e:
            if allow_fallback:
                print(f"[WARN] Maps failed ({e}); using offline estimate.")
                return offline_estimate(origin_address, dest_address)
            raise
