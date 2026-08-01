ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}


def calculate_bmr(weight_kg, height_cm, age, gender):
    base = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    if gender.lower() == "male":
        return round(base + 5, 2)
    return round(base - 161, 2)


def maintenance_calories(bmr, activity_level):
    return round(bmr * ACTIVITY_MULTIPLIERS.get(activity_level, 1.2))


def goal_calories(maintenance, goal):
    if goal == "bulk":
        return maintenance + 300
    if goal == "cut":
        return max(1200, maintenance - 500)
    if goal == "recomposition":
        return maintenance - 100
    return maintenance
