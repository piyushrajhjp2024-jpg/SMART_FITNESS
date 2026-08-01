from datetime import date, datetime
from zoneinfo import ZoneInfo

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
APP_TIMEZONE = ZoneInfo("Asia/Kolkata")


def local_now():
    return datetime.now(APP_TIMEZONE).replace(tzinfo=None)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=local_now)

    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")
    progress = db.relationship("Progress", backref="user", cascade="all, delete-orphan")
    


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(40), nullable=False)
    experience = db.Column(db.String(40), default="beginner")
    goal = db.Column(db.String(40), nullable=False)
    bmi = db.Column(db.Float)
    bmr = db.Column(db.Float)
    calories = db.Column(db.Integer)
    recommended_goal = db.Column(db.String(40))
    updated_at = db.Column(db.DateTime, default=local_now, onupdate=local_now)


class BodyGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    goal = db.Column(db.String(40), nullable=False)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=local_now)


class DietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    goal = db.Column(db.String(40), nullable=False)
    breakfast = db.Column(db.Text)
    lunch = db.Column(db.Text)
    dinner = db.Column(db.Text)
    snacks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=local_now)


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    goal = db.Column(db.String(40), nullable=False)
    day_plan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=local_now)


class Yoga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    focus = db.Column(db.String(80), nullable=False)
    poses = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=local_now)








class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float)
    calories = db.Column(db.Integer)
    goal_completion = db.Column(db.Integer, default=0)
    logged_on = db.Column(db.Date, default=date.today)
