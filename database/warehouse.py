from datetime import datetime
from database.models import db


# ==============================
# Dimension Tables
# ==============================

class DimUser(db.Model):
    __tablename__ = "dim_user"

    user_key = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    name = db.Column(db.String(120))

    age = db.Column(db.Integer)

    gender = db.Column(db.String(20))

    goal = db.Column(db.String(50))

    activity_level = db.Column(db.String(50))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class DimDate(db.Model):
    __tablename__ = "dim_date"

    date_key = db.Column(
        db.Integer,
        primary_key=True
    )

    full_date = db.Column(
        db.Date,
        unique=True
    )

    day = db.Column(db.Integer)

    month = db.Column(db.Integer)

    year = db.Column(db.Integer)

    weekday = db.Column(db.String(20))

    month_name = db.Column(db.String(20))


# ==============================
# Fact Tables
# ==============================

class FactDailyHealth(db.Model):
    __tablename__ = "fact_daily_health"

    health_key = db.Column(
        db.Integer,
        primary_key=True
    )

    user_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_user.user_key")
    )

    date_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_date.date_key")
    )

    weight = db.Column(db.Float)

    bmi = db.Column(db.Float)

    calories = db.Column(db.Float)

    health_score = db.Column(db.Float)


class FactWorkout(db.Model):
    __tablename__ = "fact_workout"

    workout_key = db.Column(
        db.Integer,
        primary_key=True
    )

    user_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_user.user_key")
    )

    date_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_date.date_key")
    )

    goal = db.Column(db.String(50))

    workout_plan = db.Column(db.Text)


class FactDiet(db.Model):
    __tablename__ = "fact_diet"

    diet_key = db.Column(
        db.Integer,
        primary_key=True
    )

    user_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_user.user_key")
    )

    date_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_date.date_key")
    )

    goal = db.Column(db.String(50))

    breakfast = db.Column(db.Text)

    lunch = db.Column(db.Text)

    dinner = db.Column(db.Text)

    snacks = db.Column(db.Text)


class FactYoga(db.Model):
    __tablename__ = "fact_yoga"

    yoga_key = db.Column(
        db.Integer,
        primary_key=True
    )

    user_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_user.user_key")
    )

    date_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_date.date_key")
    )

    focus = db.Column(db.String(100))

    poses = db.Column(db.Text)


class FactChat(db.Model):
    __tablename__ = "fact_chat"

    chat_key = db.Column(
        db.Integer,
        primary_key=True
    )

    user_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_user.user_key")
    )

    date_key = db.Column(
        db.Integer,
        db.ForeignKey("dim_date.date_key")
    )

    question = db.Column(db.Text)

    answer = db.Column(db.Text)

    language = db.Column(db.String(20))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )