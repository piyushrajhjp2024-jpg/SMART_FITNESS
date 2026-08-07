# AI-Powered Smart Nutrition, Fitness & Wellness Planner

Flask web app for personalized BMI, BMR, calorie, diet, workout, yoga, and wellness planning.

## Features

- Register, login, logout, and OTP password reset by registered email
- Profile with age, gender, height, weight, activity level, experience, and body goal
- BMI, BMR, and daily calorie calculation
- Body goal recommendation: bulk, cut, recomposition, maintain
- Diet, workout, and yoga recommendations
- Progress dashboard with Plotly charts
- PDF report generation
- MySQL-ready configuration

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create MySQL database:

```sql
CREATE DATABASE fitness_db;
```

Set your database URL:

```bash
set DATABASE_URL=mysql+pymysql://root:your_password@localhost/fitness_db
set SECRET_KEY=your-secret-key
```

For Gmail OTP password reset, use a Gmail app password and set:

```bash
set MAIL_USERNAME=your_email@gmail.com
set MAIL_PASSWORD=your_gmail_app_password
set MAIL_DEFAULT_SENDER=your_email@gmail.com
```

## Render deployment notes

Add these environment variables in Render under **Environment** before deploying:

```bash
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

The local `.env` file is ignored by Git and will not be uploaded to GitHub or Render.

Run:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

For quick local testing without MySQL:

```bash
set FLASK_ENV=local
python app.py
```
