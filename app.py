import os
import tempfile
import re
from ml.whisper_service import speech_to_text
import json
import random
import smtplib
import ssl
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from email.message import EmailMessage
from io import BytesIO
from flask_wtf.csrf import CSRFProtect

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
    jsonify,
)
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()

try:
    import bcrypt
except ImportError:
    bcrypt = None

try:
    import plotly.graph_objects as go
except ImportError:
    go = None

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
        PageBreak,
    )
except ImportError:
    letter = None
    canvas = None

from config import Config, LocalConfig
from database.models import (
    db,
    User,
    Profile,
    Progress,
    Workout,
    Yoga,
    DietPlan,
    BodyGoal
)
from database.warehouse import *
from ml.bmi import bmi_category, calculate_bmi, recommend_goal_from_bmi
from ml.calories import calculate_bmr, goal_calories, maintenance_calories
from ml.recommendation import diet_for_goal, workout_for_goal, yoga_for_focus

from ml.groq_service import generate_fitness_plan, normalize_fitness_plan
from ml.chatbot import get_chat_response

GOAL_MEAL_DETAILS = {
    "bulk": {
        "breakfast": {
            "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=900&q=80",
            "tip": "Use a calorie-dense breakfast with protein, carbs, and healthy fats for muscle gain.",
            "foods": ["masala oats", "whole eggs", "banana", "peanut butter", "milk"],
        },
        "lunch": {
            "image": "https://images.unsplash.com/photo-1543353071-10c8ba85a904?auto=format&fit=crop&w=900&q=80",
            "tip": "Make lunch the biggest balanced plate so training energy stays high.",
            "foods": ["rice", "rajma", "chicken or paneer", "ghee roti", "curd"],
        },
        "snacks": {
            "image": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=900&q=80",
            "tip": "Liquid calories and nuts help you bulk without feeling overfull.",
            "foods": ["dry fruit shake", "dates", "trail mix", "Greek yogurt", "cheese toast"],
        },
        "dinner": {
            "image": "https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=900&q=80",
            "tip": "Dinner should restore glycogen and protein after the day.",
            "foods": ["sweet potato", "fish or tofu", "dal khichdi", "sauteed vegetables", "lassi"],
        },
    },
    "cut": {
        "breakfast": {
            "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=900&q=80",
            "tip": "Cutting works better with high protein and high volume foods early in the day.",
            "foods": ["egg whites", "paneer bhurji", "apple", "green tea", "sprouts"],
        },
        "lunch": {
            "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
            "tip": "Keep lunch filling with vegetables and lean protein, but control rice or roti.",
            "foods": ["grilled chicken", "tofu salad", "dal", "one roti", "cucumber raita"],
        },
        "dinner": {
            "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
            "tip": "A lighter dinner supports the calorie deficit and better sleep.",
            "foods": ["clear soup", "stir-fry vegetables", "fish tikka", "palak paneer", "salad"],
        },
    },
    "recomposition": {
        "breakfast": {
            "image": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?auto=format&fit=crop&w=900&q=80",
            "tip": "Recomposition needs steady protein at each meal, starting at breakfast.",
            "foods": ["besan chilla", "curd", "berries", "boiled eggs", "chia seeds"],
        },
        "lunch": {
            "image": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=900&q=80",
            "tip": "Balance carbs around training while keeping protein consistent.",
            "foods": ["quinoa pulao", "dal", "paneer tikka", "mixed vegetables", "salad"],
        },
        "snacks": {
            "image": "https://images.unsplash.com/photo-1485963631004-f2f00b1d6606?auto=format&fit=crop&w=900&q=80",
            "tip": "Use snacks to hit protein targets without overeating dinner.",
            "foods": ["protein shake", "roasted chana", "sprout chaat", "buttermilk", "peanut chikki"],
        },
        "dinner": {
            "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=900&q=80",
            "tip": "Finish with lean protein, vegetables, and a moderate carb portion.",
            "foods": ["egg curry", "millet roti", "tofu bowl", "beans", "sauteed greens"],
        },
    },
    "maintain": {
        "breakfast": {
        "image": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?auto=format&fit=crop&w=900&q=80",
        "tip": "Start with protein and slow carbs so energy stays steady through the morning.",
        "foods": ["oats", "eggs or paneer", "banana", "curd", "nuts"],
        },
        "lunch": {
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
        "tip": "Keep lunch balanced: protein, complex carbs, vegetables, and a small healthy fat.",
        "foods": ["dal", "rice or roti", "chicken or paneer", "vegetables", "curd"],
        },
        "snacks": {
        "image": "https://images.unsplash.com/photo-1485963631004-f2f00b1d6606?auto=format&fit=crop&w=900&q=80",
        "tip": "Use snacks to fill protein or hydration gaps instead of only chasing calories.",
        "foods": ["roasted chana", "fruit", "sprouts", "buttermilk", "protein shake"],
        },
        "dinner": {
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
        "tip": "Dinner should support recovery while staying light enough for good sleep.",
        "foods": ["lean protein", "vegetables", "soup", "sweet potato", "salad"],
        },
    },
}


YOGA_DETAILS = {
    "stress": {
        "image": "https://images.unsplash.com/photo-1593811167562-9cef47bfc4d7?auto=format&fit=crop&w=900&q=80",
        "video": "https://www.youtube-nocookie.com/embed/HI-hKN-dVLY",
        "steps": [
            {"name": "Slow nasal breathing", "video": "https://www.youtube-nocookie.com/embed/j4-7XX2AhAs"},
            {"name": "Child pose", "video": "https://www.youtube-nocookie.com/embed/HI-hKN-dVLY"},
            {"name": "Legs up the wall", "video": "https://www.youtube-nocookie.com/embed/yqeirBfn2j4"},
            {"name": "Savasana", "video": "https://www.youtube-nocookie.com/embed/rXBSXF8VVoI"},
        ],
    },
    "weight_loss": {
        "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=900&q=80",
        "video": "https://www.youtube-nocookie.com/embed/qg3xdJv4waU",
        "steps": [
            {"name": "Warm up flow", "video": "https://www.youtube-nocookie.com/embed/36wUTAi4m7Q"},
            {"name": "Sun salutation rounds", "video": "https://www.youtube-nocookie.com/embed/qg3xdJv4waU"},
            {"name": "Power yoga flow", "video": "https://www.youtube-nocookie.com/embed/bOE2oaBJdgY"},
            {"name": "Core finisher", "video": "https://www.youtube-nocookie.com/embed/jO7ISnME9pg"},
        ],
    },
    "flexibility": {
        "image": "https://images.unsplash.com/photo-1599447421416-3414500d18a5?auto=format&fit=crop&w=900&q=80",
        "video": "https://www.youtube-nocookie.com/embed/EvMTrP8eRvM",
        "steps": [
            {"name": "Forward fold", "video": "https://www.youtube-nocookie.com/embed/Y8vJqiePu1I"},
            {"name": "Full body stretch", "video": "https://www.youtube-nocookie.com/embed/5Ju3XvZ6S1Q"},
            {"name": "Flexibility practice", "video": "https://www.youtube-nocookie.com/embed/Yzm3fA2HhkQ"},
            {"name": "Beginner stretch", "video": "https://www.youtube-nocookie.com/embed/5yf0nLjAWd8"},
        ],
    },
    "back_pain": {
        "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=900&q=80",
        "video": "https://www.youtube-nocookie.com/embed/VlUfKp1LKpc",
        "steps": [
            {"name": "Cat-cow", "video": "https://www.youtube-nocookie.com/embed/VlUfKp1LKpc"},
            {"name": "Hip and back release", "video": "https://www.youtube-nocookie.com/embed/LW3qkcNe-bE"},
            {"name": "Lower back stretch", "video": "https://www.youtube-nocookie.com/embed/rFf4MPMFGOA"},
            {"name": "Child pose rest", "video": "https://www.youtube-nocookie.com/embed/ZDiyOGM9zrk"},
        ],
    },
    "sleep": {
        "image": "https://images.unsplash.com/photo-1600618528240-fb9fc964b853?auto=format&fit=crop&w=900&q=80",
        "video": "https://www.youtube-nocookie.com/embed/5sKIdUn7lPU",
        "steps": [
            {"name": "Dim lights and settle", "video": "https://www.youtube-nocookie.com/embed/5sKIdUn7lPU"},
            {"name": "Bedtime stretch", "video": "https://www.youtube-nocookie.com/embed/Vb1fui5cccM"},
            {"name": "Relaxing bedtime flow", "video": "https://www.youtube-nocookie.com/embed/6XJhSa7g_rU"},
            {"name": "Wind down and rest", "video": "https://www.youtube-nocookie.com/embed/R478fdBJPpY"},
        ],
    },
    "chakrasana": {
        "image": "https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?auto=format&fit=crop&w=900&q=80",
        "video": "https://www.youtube-nocookie.com/embed/gyVlq5ivXC0",
        "steps": [
            {"name": "Shoulder and wrist warm-up", "video": "https://www.youtube-nocookie.com/embed/gyVlq5ivXC0"},
            {"name": "Bridge pose preparation", "video": "https://www.youtube-nocookie.com/embed/2tc3J8hEg4Y"},
            {"name": "Backbend practice", "video": "https://www.youtube-nocookie.com/embed/Yzm3fA2HhkQ"},
            {"name": "Counter stretch and rest", "video": "https://www.youtube-nocookie.com/embed/5Ju3XvZ6S1Q"},
        ],
    },
}


def hash_password(password):
    if bcrypt:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return generate_password_hash(password)


def password_matches(password, password_hash):
    if bcrypt:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except ValueError:
            pass
    return check_password_hash(password_hash, password)


def send_reset_otp(app, recipient, otp):
    sender = app.config.get("MAIL_DEFAULT_SENDER")
    username = app.config.get("MAIL_USERNAME")
    password = app.config.get("MAIL_PASSWORD")
    if not sender or not username or not password:
        return False, "Mail is not configured. Add MAIL_USERNAME, MAIL_PASSWORD, and MAIL_DEFAULT_SENDER to .env."

    message = EmailMessage()
    message["Subject"] = "Smart Fitness Planner password reset OTP"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "Use this OTP to reset your Smart Fitness Planner password: "
        f"{otp}\n\nThis code is valid for 10 minutes."
    )

    mail_server = app.config.get("MAIL_SERVER", "smtp.gmail.com")
    mail_port = int(app.config.get("MAIL_PORT", 587))
    use_tls = app.config.get("MAIL_USE_TLS", True)
    use_ssl = app.config.get("MAIL_USE_SSL", False)
    context = ssl.create_default_context()

    if use_ssl:
        with smtplib.SMTP_SSL(mail_server, mail_port, context=context) as server:
            server.login(username, password)
            server.send_message(message)
    else:
        with smtplib.SMTP(mail_server, mail_port) as server:
            if use_tls:
                server.starttls(context=context)
            server.login(username, password)
            server.send_message(message)
    return True, None


def create_app():
    app = Flask(__name__)
    if os.getenv("FLASK_ENV") == "local":
        app.config.from_object(LocalConfig)
    else:
        app.config.from_object(Config)

    print("DATABASE_URL =", os.getenv("DATABASE_URL"))
    print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form["name"].strip()
            email = request.form["email"].strip().lower()
            email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

            if not re.fullmatch(email_pattern, email):
                flash("Please enter a valid email address.", "error")
                return redirect(url_for("register"))
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("register"))
            

            # Password validation starts here
            if len(password) < 8:
                flash("Password must be at least 8 characters long.", "error")
                return redirect(url_for("register"))

            # More validation...
            

            

            if not re.search(r"[A-Z]", password):
                flash("Password must contain at least one uppercase letter.", "error")
                return redirect(url_for("register"))

            if not re.search(r"[a-z]", password):
                flash("Password must contain at least one lowercase letter.", "error")
                return redirect(url_for("register"))

            if not re.search(r"\d", password):
                flash("Password must contain at least one number.", "error")
                return redirect(url_for("register"))

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                flash("Password must contain at least one special character.", "error")
                return redirect(url_for("register"))
            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "error")
                return redirect(url_for("register"))
            

            password_hash = hash_password(password)

            user = User(
                name=name,
                email=email,
                password_hash=password_hash
            )

            try:
                db.session.add(user)
                db.session.commit()

                flash("Account created. Please log in.", "success")
                return redirect(url_for("login"))

            except Exception:
                db.session.rollback()
                app.logger.exception("Registration Error")

                flash("Unable to create your account. Please try again.", "error")
                return redirect(url_for("register"))





        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form["email"].strip().lower()
            password = request.form["password"]

            user = User.query.filter_by(email=email).first()

            if user and password_matches(password, user.password_hash):
                login_user(user)
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.", "error")

        return render_template("login.html")

    @app.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        reset_session_keys = ["reset_email", "reset_otp_hash", "reset_otp_expires", "reset_step"]
        if request.method == "GET" and request.args.get("reset") == "1":
            for key in reset_session_keys:
                session.pop(key, None)
            return redirect(url_for("forgot_password"))

        reset_step = session.get("reset_step", "email")
        reset_email = session.get("reset_email", "")
        if request.method == "POST":
            action = request.form.get("action")
            if action == "change_email":
                for key in reset_session_keys:
                    session.pop(key, None)
                return redirect(url_for("forgot_password"))

            if action == "send_otp":
                email = request.form["email"].strip().lower()
                email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

                if not re.fullmatch(email_pattern, email):
                    flash("Please enter a valid email address.", "error")
                    return redirect(url_for("forgot_password"))
                user = User.query.filter_by(email=email).first()
                if not user:
                    flash("No account is registered with that email.", "error")
                    return redirect(url_for("forgot_password"))
                otp = f"{random.randint(100000, 999999)}"
                session["reset_email"] = email
                session["reset_otp_hash"] = generate_password_hash(otp)
                session["reset_otp_expires"] = datetime.now().timestamp() + 600
                session["reset_step"] = "otp"
                try:
                    sent, mail_error = send_reset_otp(app, email, otp)
                except Exception as exc:
                    app.logger.exception("Password reset OTP email failed")
                    sent = False
                    mail_error = f"Unable to send OTP email: {exc}"
                if sent:
                    flash("OTP sent to your registered email.", "success")
                else:
                    app.logger.error("Password reset OTP email was not sent: %s", mail_error)
                    flash(f"{mail_error} Development OTP: {otp}", "warning")
                return redirect(url_for("forgot_password"))

            if action == "verify_otp":
                otp = request.form["otp"].strip()
                otp_hash = session.get("reset_otp_hash")
                expires_at = session.get("reset_otp_expires", 0)
                if not otp_hash or datetime.now().timestamp() > expires_at:
                    flash("OTP expired. Please request a new one.", "error")
                    session["reset_step"] = "email"
                    return redirect(url_for("forgot_password"))
                if not check_password_hash(otp_hash, otp):
                    flash("Invalid OTP.", "error")
                    return redirect(url_for("forgot_password"))
                session["reset_step"] = "password"
                flash("OTP verified. Please set a new password.", "success")
                return redirect(url_for("forgot_password"))

            if action == "reset_password":
                new_password = request.form["password"]

                # Same password validation
                if len(new_password) < 8:
                    flash("Password must be at least 8 characters long.", "error")
                    return redirect(url_for("forgot_password"))
                
                if not re.search(r"[A-Z]", new_password):
                    flash("Password must contain at least one uppercase letter.", "error")
                    return redirect(url_for("forgot_password"))

                if not re.search(r"[a-z]", new_password):
                    flash("Password must contain at least one lowercase letter.", "error")
                    return redirect(url_for("forgot_password"))

                if not re.search(r"\d", new_password):
                    flash("Password must contain at least one number.", "error")
                    return redirect(url_for("forgot_password"))

                if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
                    flash("Password must contain at least one special character.", "error")
                    return redirect(url_for("forgot_password"))

                # More validation...
                confirm_password = request.form["confirm_password"]
                if new_password != confirm_password:
                    flash("Passwords do not match.", "error")
                    return redirect(url_for("forgot_password"))
                

                user = User.query.filter_by(email=reset_email).first()
                if not user:
                    flash("Reset session expired. Please start again.", "error")
                    return redirect(url_for("forgot_password"))
                

                try:
                    user.password_hash = hash_password(new_password)
                    db.session.commit()

                except Exception:
                    db.session.rollback()
                    app.logger.exception("Password Reset Error")

                    flash("Unable to reset your password. Please try again.", "error")
                    return redirect(url_for("forgot_password"))

                for key in reset_session_keys:
                    session.pop(key, None)

                flash("Password updated. Please log in.", "success")
                return redirect(url_for("login"))






        return render_template("forgot_password.html", reset_step=reset_step, reset_email=reset_email)

    @app.route("/logout", methods=["GET", "POST"])
    @login_required
    def logout():
        if request.method == "GET":
            return render_template("logout.html")
        logout_user()
        flash("You have logged out safely. See you at the next session.", "success")
        return redirect(url_for("index"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        profile = current_user.profile

        latest_progress = (
            Progress.query.filter_by(user_id=current_user.id)
            .order_by(Progress.logged_on.desc())
            .first()
        )

        return render_template(
            "dashboard.html",
            profile=profile,
            category=bmi_category(profile.bmi) if profile and profile.bmi else None,
            latest_progress=latest_progress,
        )

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        if request.method == "POST":
            try:
                age = int(request.form["age"])
                gender = request.form["gender"]
                height_cm = float(request.form["height_cm"])
                weight_kg = float(request.form["weight_kg"])
                activity_level = request.form["activity_level"]
                experience = request.form["experience"]
                selected_goal = request.form["goal"]

            except (ValueError, TypeError):
                flash("Please enter valid values.", "error")
                return redirect(url_for("profile"))

            if age < 10 or age > 100:
                flash("Age must be between 10 and 100 years.", "error")
                return redirect(url_for("profile"))

            if height_cm < 50 or height_cm > 250:
                flash("Height must be between 50 cm and 250 cm.", "error")
                return redirect(url_for("profile"))

            if weight_kg < 20 or weight_kg > 400:
                flash("Weight must be between 20 kg and 400 kg.", "error")
                return redirect(url_for("profile"))
            bmi = calculate_bmi(weight_kg, height_cm)
            recommended_goal, reason = recommend_goal_from_bmi(bmi)
            final_goal = selected_goal or recommended_goal
            bmr = calculate_bmr(weight_kg, height_cm, age, gender)
            calories = goal_calories(maintenance_calories(bmr, activity_level), final_goal)

            profile_model = current_user.profile or Profile(user_id=current_user.id)
            profile_model.age = age
            profile_model.gender = gender
            profile_model.height_cm = height_cm
            profile_model.weight_kg = weight_kg
            profile_model.activity_level = activity_level
            profile_model.experience = experience
            profile_model.goal = final_goal
            profile_model.bmi = bmi
            profile_model.bmr = bmr
            profile_model.calories = calories
            profile_model.recommended_goal = recommended_goal
            db.session.add(profile_model)
            existing_goal = BodyGoal.query.filter_by(user_id=current_user.id).first()

            if existing_goal:
                existing_goal.goal = recommended_goal
                existing_goal.reason = reason
            else:
                db.session.add(
                    BodyGoal(
                        user_id=current_user.id,
                        goal=recommended_goal,
                        reason=reason
                    )
                )
            db.session.add(Progress(user_id=current_user.id, weight_kg=weight_kg, bmi=bmi, calories=calories))
            

            try:
                db.session.commit()

                flash("Profile saved and recommendations updated.", "success")
                return redirect(url_for("dashboard"))

            except Exception:
                db.session.rollback()
                app.logger.exception("Profile Save Error")

                flash("Unable to save your profile. Please try again.", "error")
                return redirect(url_for("profile"))






        return render_template("profile.html", profile=current_user.profile)

    @app.route("/bmi")
    @login_required
    def bmi():
        return render_template("bmi.html", profile=current_user.profile, bmi_category=bmi_category)

    @app.route("/diet")
    @login_required
    def diet():
        goal = current_user.profile.goal if current_user.profile else "maintain"
        plan = diet_for_goal(goal)
        stored_plan = {key: plan.get(key) for key in ["breakfast", "lunch", "dinner", "snacks"]}
        existing_plan = DietPlan.query.filter_by(user_id=current_user.id).first()
        

        try:
            if existing_plan:
                existing_plan.goal = goal
                existing_plan.breakfast = stored_plan.get("breakfast")
                existing_plan.lunch = stored_plan.get("lunch")
                existing_plan.dinner = stored_plan.get("dinner")
                existing_plan.snacks = stored_plan.get("snacks")
            else:
                db.session.add(
                    DietPlan(
                        user_id=current_user.id,
                        goal=goal,
                        **stored_plan
                    )
                )
            db.session.commit()

        except Exception:
            db.session.rollback()
            app.logger.exception("Diet Save Error")

            flash("Unable to save your diet plan. Please try again.", "error")
            return redirect(url_for("diet"))






        meal_details = GOAL_MEAL_DETAILS.get(goal, GOAL_MEAL_DETAILS["maintain"])
        return render_template("diet.html", goal=goal, plan=plan, meal_details=meal_details)

    

    @app.route("/workout")
    @login_required
    def workout():
        profile = current_user.profile
        goal = profile.goal if profile else "maintain"

        plan = workout_for_goal(
            goal,
            profile.experience if profile else "beginner",
            profile.bmi if profile else 22
        )
        existing_workout = Workout.query.filter_by(user_id=current_user.id).first()

        try:
            if existing_workout:
                existing_workout.goal = goal
                existing_workout.day_plan = json.dumps(plan, indent=2)
            else:
                db.session.add(
                    Workout(
                        user_id=current_user.id,
                        goal=goal,
                        day_plan=json.dumps(plan, indent=2)
                    )
                )
            db.session.commit()

        except Exception:
            db.session.rollback()
            app.logger.exception("Workout Save Error")
            flash("Unable to save your workout plan.", "error")

        return render_template(
            "workout.html",
            goal=goal,
            plan=plan
        )
        
    @app.route("/yoga", methods=["GET", "POST"])
    @login_required
    def yoga():
        focus = request.values.get("focus", "stress").lower()
        if focus not in YOGA_DETAILS:
            focus = "stress"
        poses = yoga_for_focus(focus)

        if request.method == "POST":
            try:
                yoga_plan = Yoga(
                    user_id=current_user.id,
                    focus=focus,
                    poses=", ".join(poses)
                )

                db.session.add(yoga_plan)
                db.session.commit()

                flash("Yoga plan saved successfully.", "success")
                return redirect(url_for("yoga", focus=focus))

            except Exception as e:
                db.session.rollback()
                app.logger.exception("Yoga Save Error")

                flash("Unable to save your yoga plan. Please try again.", "error")
                return redirect(url_for("yoga"))

        return render_template(
            "yoga.html",
            focus=focus,
            poses=poses,
            detail=YOGA_DETAILS[focus],
            yoga_details=YOGA_DETAILS,
            yoga_poses={name: yoga_for_focus(name) for name in YOGA_DETAILS}
        )

    @app.route("/progress")
    @login_required
    def progress():
        rows = Progress.query.filter_by(user_id=current_user.id).order_by(Progress.logged_on.asc()).all()
        dates = [row.logged_on.strftime("%d %b") for row in rows]
        weight = [row.weight_kg for row in rows]
        bmi_values = [row.bmi for row in rows]
        calories = [row.calories for row in rows]
        if go:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=weight, name="Weight"))
            fig.add_trace(go.Scatter(x=dates, y=bmi_values, name="BMI"))
            fig.add_trace(go.Bar(x=dates, y=calories, name="Calories"))
            fig.update_layout(
                autosize=True,
                hovermode="x unified",
                legend=dict(orientation="h"),
                margin=dict(l=32, r=20, t=36, b=32),
                template="plotly_white",
            )
            chart = fig.to_html(full_html=False)
        else:
            rows_html = "".join(
                f"<tr><td>{date}</td><td>{w}</td><td>{b}</td><td>{c}</td></tr>"
                for date, w, b, c in zip(dates, weight, bmi_values, calories)
            )
            chart = f"<table><tr><th>Date</th><th>Weight</th><th>BMI</th><th>Calories</th></tr>{rows_html}</table>"
        profile = current_user.profile
        insights = []
        
        if profile and profile.bmi:
            if profile.bmi >= 25:
                insights.append("BMI is above the healthy range, so prioritize consistent activity and controlled portions.")
            elif profile.bmi < 18.5:
                insights.append("BMI is below the healthy range, so focus on calorie surplus and strength training.")
        

        

        if not insights:
            insights.append("Great balance so far. Keep your profile updated to make the chart smarter.")

        
        return render_template("progress.html", chart=chart, insights=insights)
        

    

    @app.route("/analytics")
    @login_required
    def analytics():

        total_users = User.query.count()

        total_profiles = Profile.query.count()

        total_progress = Progress.query.count()

        avg_bmi = db.session.query(
            db.func.avg(Profile.bmi)
        ).scalar() or 0

        progress = Progress.query.filter_by(
            user_id=current_user.id
        ).order_by(Progress.logged_on).all()

        weight_chart = None
        bmi_chart = None

        if progress:

            df = pd.DataFrame({

                "Date": [p.logged_on.strftime("%d-%b") for p in progress],

                "Weight": [p.weight_kg for p in progress],

                "BMI": [p.bmi for p in progress]

            })

            fig1 = px.line(
                df,
                x="Date",
                y="Weight",
                markers=True,
                title="Weight Trend"
            )

            fig2 = px.line(
                df,
                x="Date",
                y="BMI",
                markers=True,
                title="BMI Trend"
            )

            weight_chart = fig1.to_html(full_html=False)

            bmi_chart = fig2.to_html(full_html=False)

        return render_template(

            "analytics.html",

            total_users=total_users,

            total_profiles=total_profiles,

            total_progress=total_progress,

            avg_bmi=round(avg_bmi, 2),

            weight_chart=weight_chart,

            bmi_chart=bmi_chart

        )

        

    @app.route("/ai-coach")
    @login_required
    def ai_coach():

        profile = current_user.profile

        if not profile:
            flash("Please complete your profile first.", "warning")
            return redirect(url_for("profile"))

        user_data = {
            "name": current_user.name,
            "age": profile.age,
            "gender": profile.gender,
            "height": profile.height_cm,
            "weight": profile.weight_kg,
            "bmi": profile.bmi,
            "goal": profile.goal,
            "activity": profile.activity_level,
        }

        try:
            ai_data = normalize_fitness_plan(generate_fitness_plan(user_data))

        except Exception as e:
            app.logger.exception("AI Coach Error")

            ai_data = normalize_fitness_plan(None)

        return render_template(
            "ai_coach.html",
            ai=ai_data,
            profile=profile,
            user=current_user
        )

    @app.route("/chat")
    @login_required
    def chat():
        return render_template("chat.html")


    @app.route("/chat-api", methods=["POST"])
    @login_required
    def chat_api():

        data = request.get_json(silent=True) or {}

        message = data.get("message", "")
        language = data.get("language", "en")

        if not message.strip():
            return jsonify({
                "reply": "Please type a fitness question first."
            })

        profile = current_user.profile

        user_profile = None

        if profile:
            user_profile = {
                "name": current_user.name,
                "age": profile.age,
                "gender": profile.gender,
                "height": profile.height_cm,
                "weight": profile.weight_kg,
                "bmi": profile.bmi,
                "goal": profile.goal,
                "activity": profile.activity_level,
                "calories": profile.calories
            }

        try:
            reply = get_chat_response(
                message=message,
                language=language,
                user_id=current_user.id,
                user_profile=user_profile
            )
        except Exception:
            app.logger.exception("Chat API Error")
            reply = "Sorry, I could not reach the AI assistant right now. Please try again."

        if not reply:
            reply = "Sorry, I could not generate a reply right now. Please try again."

        return jsonify({
            "reply": reply
        })

    @app.route("/report")
    @login_required
    def report():
        return render_template("report.html")


    @app.route("/report/download")
    @login_required
    def report_download():

        profile = current_user.profile

        latest_progress = Progress.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Progress.logged_on.desc()
        ).first()

        if not profile:
            flash("Please complete your profile first.", "warning")
            return redirect(url_for("profile"))

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=letter)

        pdf.setTitle("Smart Fitness Planner Report")

        width, height = letter

        y = height - 50

        # ==================================================
        # TITLE
        # ==================================================

        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(120, y, "SMART FITNESS PLANNER")

        y -= 30

        pdf.setFont("Helvetica", 14)
        pdf.drawString(190, y, "Fitness Report")

        y -= 35

        pdf.line(40, y, 560, y)

        y -= 35

        # ==================================================
        # USER DETAILS
        # ==================================================

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, y, "User Information")

        y -= 25

        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, y, f"Name : {current_user.name}")

        y -= 20

        pdf.drawString(50, y, f"Age : {profile.age}")

        y -= 20

        pdf.drawString(50, y, f"Gender : {profile.gender}")

        y -= 20

        pdf.drawString(50, y, f"Height : {profile.height_cm} cm")

        y -= 20

        pdf.drawString(50, y, f"Weight : {profile.weight_kg} kg")

        y -= 20

        pdf.drawString(50, y, f"Goal : {profile.goal.title()}")

        y -= 35

        # ==================================================
        # HEALTH METRICS
        # ==================================================

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, y, "Health Metrics")

        y -= 25

        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, y, f"BMI : {round(profile.bmi,2)}")

        y -= 20

        pdf.drawString(50, y, f"BMR : {round(profile.bmr,2)} kcal")

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Recommended Calories : {round(profile.calories,2)} kcal/day"
        )

        y -= 35

        # ==================================================
        # PROGRESS
        # ==================================================

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, y, "Latest Progress")

        y -= 25

        pdf.setFont("Helvetica", 12)

        if latest_progress:

            pdf.drawString(
                50,
                y,
                f"Latest Weight : {latest_progress.weight_kg} kg"
            )

            y -= 20

            pdf.drawString(
                50,
                y,
                f"Latest BMI : {latest_progress.bmi}"
            )

        else:

            pdf.drawString(
                50,
                y,
                "No progress records available."
            )

        y -= 35

        # ==================================================
        # AI RECOMMENDATIONS
        # ==================================================

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, y, "AI Recommendations")

        y -= 25

        pdf.setFont("Helvetica", 12)

        pdf.drawString(
            50,
            y,
            "• Follow your personalized diet recommendation."
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            "• Complete today's workout plan."
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            "• Practice yoga regularly."
        )

        y -= 35

        # ==================================================
        # FOOTER
        # ==================================================

        pdf.line(40, y, 560, y)

        y -= 25

        pdf.setFont("Helvetica-Oblique", 10)

        pdf.drawString(
            40,
            y,
            "Generated by Smart Fitness Planner"
        )

        pdf.drawRightString(
            560,
            y,
            datetime.now().strftime("%d-%m-%Y %H:%M")
        )

        pdf.save()

        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="Smart_Fitness_Report.pdf",
            mimetype="application/pdf"
        )
    return app


app = create_app()


@app.route("/speech-to-text", methods=["POST"])
@login_required
def speech_to_text_api():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio = request.files["audio"]

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".webm"
        ) as temp:

            temp_path = temp.name
            audio.save(temp_path)

        language = request.form.get("language", "en")

        text = speech_to_text(temp_path, language)

        return jsonify({
            "text": text
        })

    except Exception:
        app.logger.exception("Speech-to-Text Error")

        return jsonify({
            "error": "Unable to process audio."
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(debug=True)
