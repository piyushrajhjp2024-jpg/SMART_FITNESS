import os
import json
import logging
from dotenv import load_dotenv
from ml.groq_client import create_chat_completion

load_dotenv()

logger = logging.getLogger(__name__)

AI_PLAN_KEYS = {
    "greeting": "",
    "bmi_analysis": "",
    "goal": "",
    "breakfast": "",
    "lunch": "",
    "dinner": "",
    "snacks": "",
    "workout": {},
    "water": "",
    "sleep": "",
    "health_tips": [],
    "motivation": "",
}


def _fallback_plan(message="AI Coach is unavailable right now. Please try again later."):
    plan = AI_PLAN_KEYS.copy()
    plan.update(
        {
            "greeting": message,
            "bmi_analysis": "Your saved profile is available, but AI recommendations could not be generated at this moment.",
            "goal": "Keep following your selected goal and update your progress regularly.",
            "workout": {
                "Monday": "30 minutes brisk walk and light stretching.",
                "Tuesday": "Bodyweight strength: squats, push-ups, planks.",
                "Wednesday": "Active recovery with yoga or mobility.",
                "Thursday": "Cardio intervals for 20-25 minutes.",
                "Friday": "Full-body strength training.",
                "Saturday": "Long walk, cycling, or your favorite sport.",
                "Sunday": "Rest and recovery.",
            },
            "water": "Drink 2-3 litres of water across the day.",
            "sleep": "Aim for 7-8 hours of quality sleep.",
            "health_tips": [
                "Eat protein with every main meal.",
                "Keep your meals balanced with vegetables and whole foods.",
                "Warm up before training and cool down after.",
                "Track progress weekly instead of daily.",
                "Stay consistent with small habits.",
            ],
            "motivation": "Small daily wins build real fitness.",
        }
    )
    return plan


def normalize_fitness_plan(plan):
    if not isinstance(plan, dict):
        return _fallback_plan()

    normalized = AI_PLAN_KEYS.copy()
    normalized.update(plan)

    workout = normalized.get("workout")
    if isinstance(workout, str):
        normalized["workout"] = {"Plan": workout}
    elif not isinstance(workout, dict):
        normalized["workout"] = _fallback_plan()["workout"]

    health_tips = normalized.get("health_tips")
    if isinstance(health_tips, str):
        normalized["health_tips"] = [
            tip.strip(" -•")
            for tip in health_tips.replace("\r", "\n").split("\n")
            if tip.strip(" -•")
        ] or _fallback_plan()["health_tips"]
    elif not isinstance(health_tips, list):
        normalized["health_tips"] = _fallback_plan()["health_tips"]

    return normalized


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
    "workout":{{}},
    "water":"",
    "sleep":"",
    "health_tips":[],
    "motivation":""
}}

Rules:

- Greeting should use the user's name.
- BMI analysis should explain whether BMI is healthy.
- Meal recommendations should use Indian foods.
- Workout should be a JSON object with Monday to Sunday as keys.
- Water should be in litres/day.
- Sleep should be in hours/day.
- Health tips should be a JSON array of 5 short tips.
- Motivation should be short.
"""

    try:

        content = create_chat_completion(
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
            max_tokens=1200,
            response_format={
                "type": "json_object"
            }
        )

        return normalize_fitness_plan(json.loads(content))

    except Exception:
        logger.exception("Groq AI coach request failed")
        return _fallback_plan()
