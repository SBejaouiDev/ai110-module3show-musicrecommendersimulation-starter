# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **sebCloud**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 



The recommender generates music recommendations from a small song catalog. It suggests songs that best match a user's preferred genre, mood, energy level, and acoustic preference.

The system assumes that the user's music taste can be represented with a simple profile: one favorite genre, one favorite mood, one target energy level, and one acoustic preference. It also assumes that songs with similar content features are more likely to be good recommendations.

This recommender is for classroom exploration, not real users. It is designed to show how a basic content-based recommendation system works, how scoring rules affect rankings, and how bias or limitations can appear in recommendation systems.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

The model uses each song's genre, mood, energy, and acousticness. Genre and mood are text categories, while energy and acousticness are numeric values between 0 and 1.

The user profile considers the user's favorite genre, favorite mood, target energy level, and whether they like acoustic songs.

The model turns these into a score by comparing each song to the user profile. A song gets points if its genre matches the user's favorite genre, if its mood matches the user's favorite mood, if its energy is close to the user's target energy, and if its acousticness matches the user's acoustic preference. These smaller scores are combined into one final weighted score from 0 to 100.

The scoring formula is:

score = 100 * (
    0.30 * genre_score +
    0.30 * mood_score +
    0.25 * energy_score +
    0.15 * acoustic_score
)

I changed the starter logic so it no longer returns the first songs from the list. Instead, it loads songs from the CSV file, converts numeric columns into numbers, scores every song, sorts the songs by score, and returns the highest-ranked recommendations with specific reasons for each score.
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

The catalog contains 25 songs.

The genres represented are pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, and folk.

The moods represented are happy, chill, intense, relaxed, moody, and focused.

I added more songs to the original dataset so the recommender would have a larger catalog to rank. The added songs give the system more variety across genres, moods, energy levels, and acousticness.

Some parts of musical taste are still missing. The dataset does not include hiphop, classical, dubstep, country, metal, Latin, R&B, or many other genres. It also does not include lyrics, language, artist popularity, user listening history, song length, or context like workout music versus study music. Because of this, the system can only recommend based on a small set of simple song features.


---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  
The scoring captures basic matching patterns well. Songs with the same genre and mood as the user profile usually rise to the top, especially when their energy level is close to the user's target energy. It also correctly separates calm acoustic songs from high-energy non-acoustic songs.

For example, a chill lofi profile tends to recommend lofi songs with low energy and high acousticness. A happy pop profile tends to recommend upbeat pop songs with low acousticness. This shows that the scoring rule can recognize simple music preference patterns based on the features in the dataset.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

With content based filtering we need lots of data for the recommendation system to return more accurate results. A sample size of 15 to 20 songs will only provide us with a limited system. In terms of the algorithm itself the system treats categories as either the full math or no match. This is biased against related catogories. pop, indie pop, synth wave, electronic. The system gives no partial credit unless the text matches exactly. 

---


## 8. Future Work  

Ideas for how you would improve the model next.  

The biggest issue I see is how explicit the input has to be. The system has a set logic for genre where its either a match or not based. Genres that are similar could potential be subed out of the recommendation. 

If this were to be implemented into an app that has multiple users. Collaborative filtering could be added to recommend songs based on patterns of other users. 

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
The music reommendation system we created is just the bare minimum. Real systems are extremetly complex and usally involve machine learning archtectures such as neural networks. Neural networks are great for mapping out patterns in data that include many different features. To provide context, netflix hosted a competition to any team that could improve their recommendation algorithm by 10%, the payout was 1 million. The competition took exactly three years to complete. Goes to show how complex a recommendation system can truly be.


---

## Evaluation and Stress test with diverse profiles

These stress tests use unusual or conflicting user profiles to see whether the scoring logic produces unexpected results. Each profile was run through the recommender and the top 3 songs were recorded.

### Unknown genre but strong mood match

Profile:

```python
{
    "favorite_genre": "alien jazz",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}
```

Output:

```text
1. Metro Bloom - Score: 67.35
   - Genre is pop, not alien jazz.
   - Matches your favorite mood: happy.
   - Energy is 0.81, close to your target of 0.80.
   - Acousticness is 0.16, which helps because you prefer less acoustic songs.

2. Sunrise City - Score: 66.80
   - Genre is pop, not alien jazz.
   - Matches your favorite mood: happy.
   - Energy is 0.82, close to your target of 0.80.
   - Acousticness is 0.18, which helps because you prefer less acoustic songs.

3. Afterglow Avenue - Score: 66.50
   - Genre is synthwave, not alien jazz.
   - Matches your favorite mood: happy.
   - Energy is 0.78, close to your target of 0.80.
   - Acousticness is 0.20, which helps because you prefer less acoustic songs.
```

### Unknown mood and genre

Profile:

```python
{
    "favorite_genre": "vapor opera",
    "favorite_mood": "sleepy-angry",
    "target_energy": 0.5,
    "likes_acoustic": True,
}
```

Output:

```text
1. Morning Sketches - Score: 36.80
   - Genre is folk, not vapor opera.
   - Mood is relaxed, not sleepy-angry.
   - Energy is 0.45, close to your target of 0.50.
   - Acousticness is 0.87, which helps because you like acoustic songs.

2. Late Train Waltz - Score: 35.35
   - Genre is jazz, not vapor opera.
   - Mood is chill, not sleepy-angry.
   - Energy is 0.41, close to your target of 0.50.
   - Acousticness is 0.84, which helps because you like acoustic songs.

3. Coffee Shop Stories - Score: 35.10
   - Genre is jazz, not vapor opera.
   - Mood is relaxed, not sleepy-angry.
   - Energy is 0.37, close to your target of 0.50.
   - Acousticness is 0.89, which helps because you like acoustic songs.
```

### Extreme low energy

Profile:

```python
{
    "favorite_genre": "ambient",
    "favorite_mood": "chill",
    "target_energy": 0.0,
    "likes_acoustic": True,
}
```

Output:

```text
1. Spacewalk Thoughts - Score: 91.80
   - Matches your favorite genre: ambient.
   - Matches your favorite mood: chill.
   - Energy is 0.28, close to your target of 0.00.
   - Acousticness is 0.92, which helps because you like acoustic songs.

2. Deep Work Drift - Score: 61.45
   - Matches your favorite genre: ambient.
   - Mood is focused, not chill.
   - Energy is 0.27, close to your target of 0.00.
   - Acousticness is 0.88, which helps because you like acoustic songs.

3. Desert Satellites - Score: 60.75
   - Matches your favorite genre: ambient.
   - Mood is moody, not chill.
   - Energy is 0.31, close to your target of 0.00.
   - Acousticness is 0.90, which helps because you like acoustic songs.
```

### Conflicting preferences

Profile:

```python
{
    "favorite_genre": "lofi",
    "favorite_mood": "intense",
    "target_energy": 0.95,
    "likes_acoustic": True,
}
```

Output:

```text
1. Thunder Arcade - Score: 56.20
   - Genre is rock, not lofi.
   - Matches your favorite mood: intense.
   - Energy is 0.95, close to your target of 0.95.
   - Acousticness is 0.08, which helps because you like acoustic songs.

2. Storm Runner - Score: 55.50
   - Genre is rock, not lofi.
   - Matches your favorite mood: intense.
   - Energy is 0.91, close to your target of 0.95.
   - Acousticness is 0.10, which helps because you like acoustic songs.

3. Gym Hero - Score: 55.25
   - Genre is pop, not lofi.
   - Matches your favorite mood: intense.
   - Energy is 0.93, close to your target of 0.95.
   - Acousticness is 0.05, which helps because you like acoustic songs.
```

### Boolean as a string

Profile:

```python
{
    "favorite_genre": "classical",
    "favorite_mood": "relaxed",
    "target_energy": 0.3,
    "likes_acoustic": "False",
}
```

Output:

```text
1. Velvet Window - Score: 67.65
   - Genre is jazz, not classical.
   - Matches your favorite mood: relaxed.
   - Energy is 0.34, close to your target of 0.30.
   - Acousticness is 0.91, which helps because you like acoustic songs.

2. Coffee Shop Stories - Score: 66.60
   - Genre is jazz, not classical.
   - Matches your favorite mood: relaxed.
   - Energy is 0.37, close to your target of 0.30.
   - Acousticness is 0.89, which helps because you like acoustic songs.

3. Morning Sketches - Score: 64.30
   - Genre is folk, not classical.
   - Matches your favorite mood: relaxed.
   - Energy is 0.45, close to your target of 0.30.
   - Acousticness is 0.87, which helps because you like acoustic songs.
```

This last case shows a possible weakness in the scoring logic. The string `"False"` is treated as `True` by Python's `bool()` function, so the recommender accidentally behaves as if the user likes acoustic songs.
