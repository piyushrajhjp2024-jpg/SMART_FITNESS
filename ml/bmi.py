def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def recommend_goal_from_bmi(bmi):
    if bmi < 18.5:
        return "bulk", "BMI is below normal, so a controlled bulk can help build healthy weight."
    if bmi > 25:
        return "cut", "BMI is above normal, so a calorie deficit can support fat loss."
    return "recomposition", "BMI is in a workable range, so recomposition can improve muscle and body composition."
