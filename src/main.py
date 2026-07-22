"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def get_text_input(prompt: str) -> str:
    while True:
        user_input = input(prompt).strip().lower()

        if user_input:
            return user_input

        print("Please enter a value.")


def get_float_input(prompt: str, minimum: float, maximum: float) -> float:
    while True:
        user_input = input(prompt)

        try:
            value = float(user_input)
        except ValueError:
            print("Please enter a number.")
            continue

        if minimum <= value <= maximum:
            return value

        print(f"Please enter a value from {minimum} to {maximum}.")


def get_yes_no_input(prompt: str) -> bool:
    while True:
        user_input = input(prompt).strip().lower()

        if user_input in ["yes", "y"]:
            return True
        if user_input in ["no", "n"]:
            return False

        print("Please enter yes or no.")


def get_manual_user_preferences() -> dict:
    print()
    print("ENTER USER PREFERENCES")
    print("======================")

    return {
        "favorite_genre": get_text_input("Favorite genre: "),
        "favorite_mood": get_text_input("Favorite mood: "),
        "target_energy": get_float_input("Target energy from 0.0 to 1.0: ", 0.0, 1.0),
        "likes_acoustic": get_yes_no_input("Do you like acoustic songs? yes/no: "),
    }


def get_user_preferences() -> dict:
    preset_profiles = {
        "2": {
            "name": "Default sample preferences",
            "preferences": {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.8,
                "likes_acoustic": False,
            },
        },
        "3": {
            "name": "Hard dubstep preferences",
            "preferences": {
                "favorite_genre": "dubstep",
                "favorite_mood": "intense",
                "target_energy": 0.95,
                "likes_acoustic": False,
            },
        },
        "4": {
            "name": "Hiphop preferences",
            "preferences": {
                "favorite_genre": "hiphop",
                "favorite_mood": "focused",
                "target_energy": 0.75,
                "likes_acoustic": False,
            },
        },
        "5": {
            "name": "Classical preferences",
            "preferences": {
                "favorite_genre": "classical",
                "favorite_mood": "relaxed",
                "target_energy": 0.30,
                "likes_acoustic": True,
            },
        },
    }

    while True:
        print()
        print("MUSIC RECOMMENDER MENU")
        print("======================")
        print("1. Enter preferences manually")
        for option, preset in preset_profiles.items():
            print(f"{option}. Use {preset['name']}")
        print("6. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            return get_manual_user_preferences()
        if choice in preset_profiles:
            return preset_profiles[choice]["preferences"]
        if choice == "6":
            return {}

        print("Please choose an option from 1 to 6.")


def display_recommendations(recommendations: list) -> None:
    print()
    print("MUSIC RECOMMENDATIONS")
    print("=====================")
    print()

    for rank, recommendation in enumerate(recommendations, start=1):
        song, score, reasons = recommendation

        print(f"{rank}. {song['title']}")
        print(f"   Final Score: {score:.2f}")
        print("   Reasons:")

        for reason in reasons:
            print(f"   - {reason}")

        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = get_user_preferences()

    if not user_prefs:
        print("Goodbye.")
        return

    recommendations = recommend_songs(user_prefs, songs, k=5)
    display_recommendations(recommendations)


if __name__ == "__main__":
    main()
