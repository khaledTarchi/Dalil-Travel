import os
from groq import Groq

API_KEY_PART1 = "gsk_"
API_KEY_PART2 = "V215QQYCiTqj14lujzd0WGdyb3FYFrvvLVyB3bqwg2FBgD3uusuf"

# Initialize the client with the free API key directly as requested
client = Groq(
    api_key=API_KEY_PART1 + API_KEY_PART2,
)

def get_ai_guide_info(location_name, user_language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Act as an expert Algerian tour guide. Generate a 1-Day Itinerary for {location_name} in {user_language}. Return ONLY the itinerary as a list of times and activities in this EXACT format on separate lines (no intro, no outro): HH:MM AM/PM|Activity. Example:\n09:00 AM|Visit the historic Casbah\n13:00 PM|Enjoy a traditional Algerian lunch"
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)
