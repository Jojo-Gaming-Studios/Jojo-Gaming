import os
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
import json



def get_streamers():
    with open("streamers.json", "r") as file:
        data = json.load(file)
    return data["streamers"]


load_dotenv()  # Lädt API-Keys aus .env Datei

app = FastAPI()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

# Twitch OAuth Token holen
def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")


# Live-Streamer abrufen
@app.get("/live_streams")
def get_live_streams():
    token = get_twitch_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }

    # Liste der Jojo Gaming Streamer (kann später in einer DB gespeichert werden)
    streamer_logins = get_streamers()  # <-- Hier deine Streamer eintragen

    url = f"https://api.twitch.tv/helix/streams?user_login={'&user_login='.join(streamer_logins)}"
    response = requests.get(url, headers=headers)
    data = response.json()

    live_streams = [
        {
            "name": stream["user_name"],
            "game": stream["game_name"],
            "viewer_count": stream["viewer_count"]
        }
        for stream in data.get("data", [])
    ]
    return {"live_streams": live_streams}
