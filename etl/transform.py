from collections import defaultdict


def calculate_health_score(profile):
    """
    Calculate health score based only on BMI.
    """

    if not profile or not profile.bmi:
        return 0

    bmi = profile.bmi

    if 18.5 <= bmi <= 24.9:
        return 100
    elif 25 <= bmi <= 29.9:
        return 80
    elif 17 <= bmi < 18.5:
        return 70
    else:
        return 60


def transform_data(data):
    """
    Transform operational data into warehouse data.
    """

    warehouse_data = []

    users = {u.id: u for u in data["users"]}
    profiles = {p.user_id: p for p in data["profiles"]}

    progress_map = defaultdict(list)

    for progress in data["progress"]:
        progress_map[progress.user_id].append(progress)

    for user_id, user in users.items():

        profile = profiles.get(user_id)

        latest_progress = (
            progress_map[user_id][-1]
            if progress_map[user_id]
            else None
        )

        health_score = calculate_health_score(profile)

        warehouse_data.append({

            "user": user,

            "profile": profile,

            "progress": latest_progress,

            "health_score": health_score

        })

    return warehouse_data