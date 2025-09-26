from typing import Optional
import base64
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_REVERSE = "https://geocoding-api.open-meteo.com/v1/reverse"
IP_LOOKUP = "https://ipapi.co/json/"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_NOW_PLAYING = "https://api.spotify.com/v1/me/player/currently-playing"


WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def _reverse_geocode(lat: float, lon: float) -> Optional[str]:
    try:
        r = requests.get(OPEN_METEO_REVERSE, params={
            "latitude": lat,
            "longitude": lon,
            "language": "en",
        }, timeout=8)
        if r.ok:
            data = r.json()
            results = data.get("results") or []
            if results:
                # Use name (city/town) if available, else admin1/2
                name = results[0].get("name")
                admin1 = results[0].get("admin1")
                return name or admin1
    except Exception:
        pass
    return None


@api_view(["GET"])
def location_weather(request):
    lat = request.query_params.get("lat")
    lon = request.query_params.get("lon")

    try:
        if not lat or not lon:
            # Fallback to IP lookup
            ipr = requests.get(IP_LOOKUP, timeout=6)
            if ipr.ok:
                ipdata = ipr.json()
                lat = ipdata.get("latitude") or ipr.json().get("lat")
                lon = ipdata.get("longitude") or ipr.json().get("lon")
                city = ipdata.get("city")
            else:
                return Response({"detail": "Could not determine location"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            lat = float(lat)
            lon = float(lon)
            city = None

        fr = requests.get(OPEN_METEO_FORECAST, params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        }, timeout=8)
        if not fr.ok:
            return Response({"detail": "Weather service error"}, status=status.HTTP_502_BAD_GATEWAY)

        fjson = fr.json()
        cw = fjson.get("current_weather") or {}
        temp = cw.get("temperature")
        code = cw.get("weathercode")
        condition = WEATHER_CODE_MAP.get(code, "Unknown")

        if not city:
            city = _reverse_geocode(float(lat), float(lon)) or "Unknown"

        return Response({
            "city": city,
            "temperature": temp,
            "condition": condition,
        })
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _refresh_spotify_access_token() -> Optional[str]:
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    refresh_token = settings.SPOTIFY_REFRESH_TOKEN

    if not client_id or not client_secret or not refresh_token:
        return None

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    r = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data, timeout=8)
    if not r.ok:
        return None
    return r.json().get("access_token")


@api_view(["GET"])
def spotify_now_playing(request):
    try:
        access_token = _refresh_spotify_access_token()
        if not access_token:
            return Response({"is_playing": False, "detail": "Spotify not configured"}, status=status.HTTP_200_OK)

        headers = {"Authorization": f"Bearer {access_token}"}
        r = requests.get(SPOTIFY_NOW_PLAYING, headers=headers, timeout=8)
        if r.status_code == 204:
            return Response({"is_playing": False})
        if not r.ok:
            return Response({"is_playing": False}, status=r.status_code)

        data = r.json()
        is_playing = data.get("is_playing", False)
        item = data.get("item") or {}
        name = item.get("name")
        artists = ", ".join(a.get("name") for a in (item.get("artists") or []))
        album = (item.get("album") or {}).get("name")
        urls = (item.get("external_urls") or {})
        track_url = urls.get("spotify")
        images = (item.get("album") or {}).get("images") or []
        album_image_url = images[0].get("url") if images else None
        duration_ms = item.get("duration_ms")
        progress_ms = data.get("progress_ms")

        return Response({
            "is_playing": is_playing,
            "name": name,
            "artists": artists,
            "album": album,
            "url": track_url,
            "album_image_url": album_image_url,
            "duration_ms": duration_ms,
            "progress_ms": progress_ms,
        })
    except Exception as e:
        return Response({"is_playing": False, "detail": str(e)}, status=status.HTTP_200_OK)
