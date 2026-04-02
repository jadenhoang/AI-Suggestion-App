# app.py
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


# Load variables from .env

load_dotenv()

# Your static activity data

activities = [
    # Berkeley
    {"name": "Local coffee shop", "type": "chill", "city": "Berkeley"},
    {"name": "Hiking trail", "type": "outdoor", "city": "Berkeley"},
    {"name": "Art gallery", "type": "creative", "city": "Berkeley"},
    {"name": "Food market", "type": "food", "city": "Berkeley"},
    {"name": "Community board game night", "type": "social", "city": "Berkeley"},
    {"name": "Rooftop lounge", "type": "bar", "city": "Berkeley"},

    # San Francisco
    {"name": "SF Museum of Modern Art", "type": "creative", "city": "San Francisco"},
    {"name": "Yerba Buena Center for the Arts", "type": "creative", "city": "San Francisco"},
    {"name": "Street Art Tour", "type": "creative", "city": "San Francisco"},
    {"name": "The Tipsy Tavern", "type": "bar", "city": "San Francisco"},
    {"name": "Rooftop Lounge", "type": "bar", "city": "San Francisco"},
    {"name": "Downtown Pub Crawl", "type": "bar", "city": "San Francisco"},
    {"name": "Food market", "type": "food", "city": "San Francisco"},
    {"name": "Ferry Building tasting tour", "type": "food", "city": "San Francisco"},
    {"name": "Golden Gate Park walk", "type": "outdoor", "city": "San Francisco"},
    {"name": "Yoga in the park", "type": "chill", "city": "San Francisco"},
    {"name": "Local meetup event", "type": "social", "city": "San Francisco"},

    # New York City
    {"name": "Live music event", "type": "social", "city": "New York City"},
    {"name": "Central Park walk", "type": "outdoor", "city": "New York City"},
    {"name": "Food festival", "type": "food", "city": "New York City"},
    {"name": "Art gallery hopping", "type": "creative", "city": "New York City"},
    {"name": "Chill cafe hangout", "type": "chill", "city": "New York City"},
    {"name": "Rooftop bar", "type": "bar", "city": "New York City"}
]

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper function
def normalize_input(text):
    return text.strip().lower()

# Core function to get suggestions
def get_suggestions(city, vibe):
    city = normalize_input(city)
    vibe = normalize_input(vibe)

    # Filter activities by city + vibe
    filtered = [a for a in activities if a["city"].lower() == city and a["type"].lower() == vibe]

    if not filtered:
        return f"Sorry, no {vibe} activities found in {city.title()} 😅"

    activity = filtered[0]

    # AI prompt: multiple fun variations
    prompt = f"""
You are a lively local guide.
Take this activity: "{activity['name']}" in {city.title()}.
Write 3-5 fun, engaging, that are different but same type of energy as the activity.
Include emojis, short tips, and make each suggestion feel unique. Don't ask to tailor response after giving suggestions.
"""

    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="🌆 AI City Activity Suggester", layout="wide")
st.title("🌆 AI City Activity Suggester")

city = st.text_input("Enter city:")
vibe = st.selectbox("Choose your vibe:", ["food", "bar", "chill", "social", "outdoor", "creative"])

if st.button("Get Suggestions"):
    if city:
        suggestions = get_suggestions(city, vibe)
        st.markdown(suggestions)
    else:
        st.warning("Please enter a city first!")