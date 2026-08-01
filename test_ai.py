from ml.groq_service import generate_fitness_plan

user = {
    "name": "Piyush",
    "age": 22,
    "gender": "Male",
    "height": 175,
    "weight": 82,
    "bmi": 26.8,
    "goal": "Fat Loss",
    "activity": "Moderate"
}

result = generate_fitness_plan(user)

print(result)