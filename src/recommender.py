from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool



class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog used for recommendations."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by their content-based score."""
        scored_songs = []

        for song in self.songs:
            user_prefs = {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            }
            song_data = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_data)
            scored_songs.append((song, score))

        scored_songs.sort(key=lambda item: item[1], reverse=True)
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation for why a song matches the user."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_data = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }
        score, reasons = score_song(user_prefs, song_data)
        return f"Score: {score:.2f}. " + " ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields."""
    songs = []

    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])

            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a user profile and return reasons."""
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre", ""))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood", ""))
    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5)))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    genre_score = 1 if song["genre"].lower() == favorite_genre.lower() else 0
    mood_score = 1 if song["mood"].lower() == favorite_mood.lower() else 0
    energy_score = 1 - abs(float(song["energy"]) - target_energy)
    energy_score = max(0, min(1, energy_score))

    acousticness = float(song["acousticness"])
    if likes_acoustic:
        acoustic_score = acousticness
    else:
        acoustic_score = 1 - acousticness

    score = 100 * (
        0.30 * genre_score +
        0.30 * mood_score +
        0.25 * energy_score +
        0.15 * acoustic_score
    )

    reasons = []
    if genre_score == 1:
        reasons.append(f"Matches your favorite genre: {favorite_genre}.")
    else:
        reasons.append(f"Genre is {song['genre']}, not {favorite_genre}.")

    if mood_score == 1:
        reasons.append(f"Matches your favorite mood: {favorite_mood}.")
    else:
        reasons.append(f"Mood is {song['mood']}, not {favorite_mood}.")

    reasons.append(f"Energy is {float(song['energy']):.2f}, close to your target of {target_energy:.2f}.")

    if likes_acoustic:
        reasons.append(f"Acousticness is {acousticness:.2f}, which helps because you like acoustic songs.")
    else:
        reasons.append(f"Acousticness is {acousticness:.2f}, which helps because you prefer less acoustic songs.")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Return the top k song dictionaries with scores and reasons."""
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
