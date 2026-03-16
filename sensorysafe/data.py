"""Datahantering for SensorySafe - JSON-baserad platsdatabas."""

import json
import os
from pathlib import Path


def get_data_path():
    """Returnerar sökväg till JSON-databasen."""
    data_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "sensorysafe"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "platser.json"


def load_places():
    """Ladda platser från JSON-fil."""
    path = get_data_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return get_default_places()


def save_places(places):
    """Spara platser till JSON-fil."""
    path = get_data_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)


def get_default_places():
    """Returnerar exempelplatser."""
    return [
        {
            "namn": "Stadsbiblioteket",
            "beskrivning": "Lugnt bibliotek med tysta zoner",
            "ljud": 2,
            "ljus": 3,
            "traengsel": 2,
            "kommentar": "Bra tysta hörn på övervåningen"
        },
        {
            "namn": "Centralstationen",
            "beskrivning": "Stor tågstation med mycket folk",
            "ljud": 8,
            "ljus": 6,
            "traengsel": 9,
            "kommentar": "Undvik rusningstid 07-09 och 16-18"
        },
        {
            "namn": "Stadsparken",
            "beskrivning": "Öppen park med grönytor",
            "ljud": 3,
            "ljus": 5,
            "traengsel": 3,
            "kommentar": "Lugnt på vardagar, folkrikare på helger"
        },
        {
            "namn": "Gallerian",
            "beskrivning": "Stort köpcentrum med många butiker",
            "ljud": 7,
            "ljus": 8,
            "traengsel": 8,
            "kommentar": "Starkt lysrör och hög musik i flera butiker"
        },
        {
            "namn": "Kaféet Lugna Vrån",
            "beskrivning": "Litet café med dämpad belysning",
            "ljud": 2,
            "ljus": 2,
            "traengsel": 2,
            "kommentar": "Perfekt för känsliga personer, max 15 gäster"
        },
    ]


def get_sensory_level(value):
    """Returnerar textbeskrivning av sensorisk nivå."""
    if value <= 3:
        return "Låg"
    elif value <= 6:
        return "Medel"
    else:
        return "Hög"


def get_sensory_icon(value):
    """Returnerar ikon baserat på sensorisk nivå."""
    if value <= 3:
        return "\u2705"  # green check
    elif value <= 6:
        return "\u26a0\ufe0f"  # warning
    else:
        return "\u274c"  # red X


def get_overall_rating(place):
    """Beräknar genomsnittlig sensorisk belastning."""
    return round((place["ljud"] + place["ljus"] + place["traengsel"]) / 3, 1)
