import pytest
from mood_suggestions import suggest_activity, suggest_music, suggest_movie, suggest_motivation

def test_suggest_activity():
    assert suggest_activity("happy") in ["Go for a walk in the park", "Attend a friend's party", "Try out new hobbies"]
    assert suggest_activity("sad") in ["Write in a journal", "Meditate"]
    assert suggest_activity("stressed") in ["Do deep breathing exercises", "Practice yoga", "Drink a hot cup of tea"]
    assert suggest_activity("bored") in ["Learn a new skill", "Watch a documentary"]
    assert suggest_activity("excited") == "Try something new!"

def test_suggest_music():
    assert suggest_music("happy") in ["Pop music", "Upbeat electronic music"]
    assert suggest_music("sad") in ["Soft piano music", "Lyrical ballads"]
    assert suggest_music("stressed") in ["Nature sounds", "Calm instrumental music"]
    assert suggest_music("bored") in ["Jazz", "Rock music"]
    assert suggest_music("curious") == "Explore a new music genre!"

def test_suggest_movie():
    assert suggest_movie("happy") in ["Ready Player One", "Zootopia"]
    assert suggest_movie("sad") in ["Soul", "The Pursuit of Happyness"]
    assert suggest_movie("stressed") in ["Forrest Gump", "Green Book"]
    assert suggest_movie("bored") in ["Inception", "The Matrix"]
    assert suggest_movie("mystery") == "Try a new movie!"

def test_suggest_motivation():
    assert suggest_motivation("happy") == "Keep up the good mood, the world will be even brighter!"
    assert suggest_motivation("sad") == "After darkness, there is always light."
    assert suggest_motivation("stressed") == "Take a deep breath, everything will be fine."
    assert suggest_motivation("bored") == "Try something new, the world is full of possibilities!"
    assert suggest_motivation("confused") == "No matter what, today is a fresh start!"

