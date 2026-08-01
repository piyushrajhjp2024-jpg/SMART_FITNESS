DIET_PLANS = {
    "bulk": {
        "breakfast": "Masala oats cooked in milk with banana, peanut butter, and two whole eggs",
        "lunch": "Rajma rice, ghee roti, chicken or paneer, curd, and seasonal vegetables",
        "snacks": "Dry fruit shake with dates plus Greek yogurt or cheese toast",
        "dinner": "Sweet potato, fish or tofu, dal khichdi, sauteed vegetables, and lassi",
    },
    "cut": {
        "breakfast": "Egg whites or paneer bhurji with sprouts, apple, and green tea",
        "lunch": "Grilled chicken or tofu salad with dal, cucumber raita, and one roti",
        "dinner": "Clear soup, stir-fry vegetables, fish tikka or palak paneer, and salad",
    },
    "recomposition": {
        "breakfast": "Besan chilla with curd, berries, boiled eggs, and chia seeds",
        "lunch": "Quinoa pulao, dal, paneer tikka, mixed vegetables, and salad",
        "snacks": "Protein shake, roasted chana, sprout chaat, buttermilk, or peanut chikki",
        "dinner": "Egg curry or tofu bowl with millet roti, beans, and sauteed greens",
    },
    "maintain": {
        "breakfast": "Balanced breakfast with protein, carbs, and fruit",
        "lunch": "Home-style balanced meal with vegetables and protein",
        "dinner": "Light balanced dinner",
        "snacks": "Fruit, nuts, or yogurt",
    },
}


WORKOUT_IMAGES = {
    "push": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=900&q=80",
    "pull": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=900&q=80",
    "legs": "https://images.unsplash.com/photo-1434682881908-b43d0467b798?auto=format&fit=crop&w=900&q=80",
    "cardio": "https://images.unsplash.com/photo-1538805060514-97d9cc17730c?auto=format&fit=crop&w=900&q=80",
    "yoga": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=900&q=80",
    "rest": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=900&q=80",
}


WORKOUT_PLANS = {
    "bulk": [
        {
            "day": "Monday",
            "focus": "Chest + Triceps",
            "duration": "55 min",
            "intensity": "Strength",
            "image": WORKOUT_IMAGES["push"],
            "exercises": [
                "Bench press - 4 sets x 8 reps",
                "Incline dumbbell press - 3 sets x 10 reps",
                "Cable fly - 3 sets x 12 reps",
                "Triceps pushdown - 3 sets x 12 reps",
                "Overhead triceps extension - 3 sets x 10 reps",
            ],
        },
        {
            "day": "Tuesday",
            "focus": "Back + Biceps",
            "duration": "55 min",
            "intensity": "Strength",
            "image": WORKOUT_IMAGES["pull"],
            "exercises": [
                "Lat pulldown - 4 sets x 10 reps",
                "Seated cable row - 4 sets x 10 reps",
                "One-arm dumbbell row - 3 sets x 10 reps",
                "Barbell curl - 3 sets x 12 reps",
                "Hammer curl - 3 sets x 12 reps",
            ],
        },
        {
            "day": "Wednesday",
            "focus": "Legs",
            "duration": "60 min",
            "intensity": "Heavy",
            "image": WORKOUT_IMAGES["legs"],
            "exercises": [
                "Squat - 4 sets x 8 reps",
                "Leg press - 4 sets x 10 reps",
                "Romanian deadlift - 3 sets x 10 reps",
                "Walking lunges - 3 sets x 12 reps",
                "Calf raises - 4 sets x 15 reps",
            ],
        },
        {
            "day": "Thursday",
            "focus": "Recovery",
            "duration": "25 min",
            "intensity": "Light",
            "image": WORKOUT_IMAGES["rest"],
            "exercises": [
                "Easy walk - 15 minutes",
                "Full-body mobility - 10 minutes",
                "Deep breathing - 5 minutes",
            ],
        },
        {
            "day": "Friday",
            "focus": "Shoulders + Core",
            "duration": "50 min",
            "intensity": "Strength",
            "image": WORKOUT_IMAGES["push"],
            "exercises": [
                "Overhead press - 4 sets x 8 reps",
                "Lateral raise - 4 sets x 12 reps",
                "Rear delt fly - 3 sets x 12 reps",
                "Plank - 3 rounds x 45 seconds",
                "Cable crunch - 3 sets x 15 reps",
            ],
        },
        {
            "day": "Saturday",
            "focus": "Full Body",
            "duration": "45 min",
            "intensity": "Moderate",
            "image": WORKOUT_IMAGES["cardio"],
            "exercises": [
                "Goblet squat - 3 sets x 12 reps",
                "Push-ups - 3 sets x 12 reps",
                "Dumbbell row - 3 sets x 12 reps",
                "Farmer carry - 3 rounds",
                "Stationary bike - 10 minutes",
            ],
        },
        {
            "day": "Sunday",
            "focus": "Rest",
            "duration": "20 min",
            "intensity": "Easy",
            "image": WORKOUT_IMAGES["yoga"],
            "exercises": [
                "Light stretching",
                "Hydration check",
                "Prepare meals and training clothes for Monday",
            ],
        },
    ],
    "cut": [
        {
            "day": "Monday",
            "focus": "Upper Strength",
            "duration": "45 min",
            "intensity": "Moderate",
            "image": WORKOUT_IMAGES["push"],
            "exercises": ["Push-ups - 4 sets", "Dumbbell press - 3 sets x 10 reps", "Lat pulldown - 3 sets x 12 reps", "Shoulder press - 3 sets x 10 reps"],
        },
        {
            "day": "Tuesday",
            "focus": "Cardio",
            "duration": "35 min",
            "intensity": "Fat Burn",
            "image": WORKOUT_IMAGES["cardio"],
            "exercises": ["Brisk walk - 10 minutes", "Jog intervals - 18 minutes", "Cool down walk - 7 minutes"],
        },
        {
            "day": "Wednesday",
            "focus": "Lower Body",
            "duration": "45 min",
            "intensity": "Moderate",
            "image": WORKOUT_IMAGES["legs"],
            "exercises": ["Goblet squat - 4 sets x 12 reps", "Step-ups - 3 sets x 12 reps", "Hip thrust - 3 sets x 12 reps", "Calf raises - 3 sets x 15 reps"],
        },
        {
            "day": "Thursday",
            "focus": "HIIT",
            "duration": "25 min",
            "intensity": "High",
            "image": WORKOUT_IMAGES["cardio"],
            "exercises": ["Jumping jacks - 40 seconds", "Mountain climbers - 40 seconds", "Bodyweight squats - 40 seconds", "Rest - 40 seconds", "Repeat 5 rounds"],
        },
        {
            "day": "Friday",
            "focus": "Full Body Circuit",
            "duration": "40 min",
            "intensity": "Moderate",
            "image": WORKOUT_IMAGES["pull"],
            "exercises": ["Kettlebell deadlift - 3 sets", "Incline push-up - 3 sets", "Cable row - 3 sets", "Plank - 3 rounds"],
        },
        {
            "day": "Saturday",
            "focus": "Walk + Yoga",
            "duration": "40 min",
            "intensity": "Easy",
            "image": WORKOUT_IMAGES["yoga"],
            "exercises": ["Outdoor walk - 25 minutes", "Sun salutation - 5 rounds", "Hip and back stretches - 10 minutes"],
        },
        {
            "day": "Sunday",
            "focus": "Rest",
            "duration": "15 min",
            "intensity": "Easy",
            "image": WORKOUT_IMAGES["rest"],
            "exercises": ["Rest", "Sleep 7 to 9 hours", "Plan next week's meals"],
        },
    ],
}

WORKOUT_PLANS["recomposition"] = [
    {**item, "intensity": "Balanced"} for item in WORKOUT_PLANS["bulk"]
]
WORKOUT_PLANS["maintain"] = [
    {**item, "intensity": "Steady"} for item in WORKOUT_PLANS["cut"]
]


YOGA_PLANS = {
    "stress": "Balasana, Sukhasana breathing, Viparita Karani, Savasana",
    "weight_loss": "Surya Namaskar, Utkatasana, Virabhadrasana, Naukasana",
    "flexibility": "Paschimottanasana, Bhujangasana, Trikonasana, Baddha Konasana",
    "back_pain": "Cat-Cow, Makarasana, Setu Bandhasana, Child Pose",
    "sleep": "Legs-up-the-wall, forward fold, box breathing, Savasana",
}


def diet_for_goal(goal):
    return DIET_PLANS.get(goal, DIET_PLANS["maintain"])


def workout_for_goal(goal, experience, bmi):
    plan = WORKOUT_PLANS.get(goal, WORKOUT_PLANS["maintain"])
    plan = [dict(day_plan) for day_plan in plan]
    if experience == "beginner":
        for day_plan in plan:
            day_plan["note"] = "Keep intensity moderate and focus on form."
        return plan
    if bmi > 30:
        for day_plan in plan:
            day_plan["note"] = "Prefer low-impact cardio and gradual progression."
        return plan
    return plan


def yoga_for_focus(focus):
    return YOGA_PLANS.get(focus, YOGA_PLANS["stress"])
