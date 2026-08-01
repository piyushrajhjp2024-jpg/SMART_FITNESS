import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are FitBot, the official AI Fitness Assistant of Smart Fitness Planner.

Developer: Piyush Raj

Rules:
1. Answer ONLY fitness-related questions.
2. Reply in the same language as the user.
3. Never say you are ChatGPT.
4. Say you were developed by Piyush Raj.
5. Keep replies concise and helpful.
"""

conversation_memory = {}


def get_chat_response(message, language="en", user_id="guest", user_profile=None):
    try:
        if user_id not in conversation_memory:
            conversation_memory[user_id] = []

        history = conversation_memory[user_id]
        profile_text = ""

        if user_profile:
            profile_text = f"""
User Profile:
Name: {user_profile.get('name')}
Age: {user_profile.get('age')}
Gender: {user_profile.get('gender')}
Height: {user_profile.get('height')} cm
Weight: {user_profile.get('weight')} kg
BMI: {user_profile.get('bmi')}
Goal: {user_profile.get('goal')}
Activity: {user_profile.get('activity')}
Calories: {user_profile.get('calories')}
"""

        if language == "hi":
            user_prompt = f"""
Answer only in natural Hindi.

{profile_text}

Question:
{message}
"""
        else:
            user_prompt = f"""
{profile_text}

Question:
{message}
"""

        history.append({"role": "user", "content": user_prompt})
        history = history[-10:]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2,
            max_tokens=400,
        )

        reply = completion.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": reply})
        conversation_memory[user_id] = history[-10:]

        return reply

    except Exception:
        return "Sorry, something went wrong."
