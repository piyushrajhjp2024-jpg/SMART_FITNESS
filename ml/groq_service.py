import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_fitness_plan(user_data):

    prompt = f"""
You are a certified nutritionist, fitness coach, and health consultant.

Prepare a detailed personalized fitness report.

User Information

Name: {user_data["name"]}
Age: {user_data["age"]}
Gender: {user_data["gender"]}
Height: {user_data["height"]} cm
Weight: {user_data["weight"]} kg
BMI: {user_data["bmi"]}
Goal: {user_data["goal"]}
Activity Level: {user_data["activity"]}

Return ONLY valid JSON.

{{
    "greeting":"",
    "bmi_analysis":"",
    "goal":"",
    "breakfast":"",
    "lunch":"",
    "dinner":"",
    "snacks":"",
    "workout":"",
    "water":"",
    "sleep":"",
    "health_tips":"",
    "motivation":""
}}

Rules:

- Greeting should use the user's name.
- BMI analysis should explain whether BMI is healthy.
- Meal recommendations should use Indian foods.
- Workout should include Monday to Sunday.
- Water should be in litres/day.
- Sleep should be in hours/day.
- Health tips should be 5 bullet points.
- Motivation should be short.
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert fitness coach."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            response_format={
                "type": "json_object"
            }

        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {

            "greeting": "AI Coach is unavailable.",

            "bmi_analysis": str(e),

            "goal": "",

            "breakfast": "",

            "lunch": "",

            "dinner": "",

            "snacks": "",

            "workout": "",

            "water": "",

            "sleep": "",

            "health_tips": "",

            "motivation": ""

        }
