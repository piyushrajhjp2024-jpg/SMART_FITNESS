from database.models import (
    User,
    Profile,
    Progress,
    Workout,
    Yoga,
    DietPlan,
    BodyGoal
)


def extract_data():
    """
    Extract data from the operational database.
    """

    return {
        "users": User.query.all(),
        "profiles": Profile.query.all(),
        "progress": Progress.query.all(),
        "workouts": Workout.query.all(),
        "yoga": Yoga.query.all(),
        "diet_plans": DietPlan.query.all(),
        "body_goals": BodyGoal.query.all()
    }