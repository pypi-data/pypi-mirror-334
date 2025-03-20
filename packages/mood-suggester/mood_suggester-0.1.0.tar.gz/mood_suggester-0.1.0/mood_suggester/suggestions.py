import random

def suggest_activity(mood: str) -> str:
    activities = {
        "happy": ["Go for a walk in the park", "Attend a friend's party", "Try out new hobbies"],
        "sad": ["Write in a journal", "Meditate"],
        "stressed": ["Do deep breathing exercises", "Practice yoga", "Drink a hot cup of tea"],
        "bored": ["Learn a new skill", "Watch a documentary"]
    }
    return random.choice(activities.get(mood.lower(), ["Try something new!"]))

def suggest_music(mood: str) -> str:
    music = {
        "happy": ["Pop music", "Upbeat electronic music"],
        "sad": ["Soft piano music", "Lyrical ballads"],
        "stressed": ["Nature sounds", "Calm instrumental music"],
        "bored": ["Jazz", "Rock music"]
    }
    return random.choice(music.get(mood.lower(), ["Explore a new music genre!"]))

def suggest_movie(mood: str) -> str:
    movies = {
        "happy": ["Ready Player One", "Zootopia"],
        "sad": ["Soul", "The Pursuit of Happyness"],
        "stressed": ["Forrest Gump", "Green Book"],
        "bored": ["Inception", "The Matrix"]
    }
    return random.choice(movies.get(mood.lower(), ["Try a new movie!"]))

def suggest_motivation(mood: str) -> str:
    quotes = {
        "happy": ["Keep up the good mood, the world will be even brighter!"],
        "sad": ["After darkness, there is always light."],
        "stressed": ["Take a deep breath, everything will be fine."],
        "bored": ["Try something new, the world is full of possibilities!"]
    }
    return random.choice(quotes.get(mood.lower(), ["No matter what, today is a fresh start!"]))