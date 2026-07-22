"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

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


if __name__ == "__main__":
    main()
