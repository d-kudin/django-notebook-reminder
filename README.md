# Notebook – Personal Notes Manager with Django

This is a Django-based notebook web app that allows you to create, manage, and categorize notes with deadlines, reminders, and priority levels.

## Features

-  Register, login, logout system
-  Add, edit, complete, delete notes
-  Mark notes as priority (with visual badge)
-  Set deadlines and reminders
-  Organize notes into categories
-  Filter by category and creation date
-  Status color tag (green, yellow, red)
-  Smart sorting (latest notes appear first)
-  Visual badge indicators for reminders and priority
-  Secure password handling via Django's auth system
-  `.env` support for environment-specific settings

## Additional Functionality

### Weather Widget
- Automatically fetches and displays current weather in Warsaw.
- Uses external API (e.g., OpenWeatherMap) – API key stored securely in `.env`.

### News Feed
- Displays recent news headlines in a compact sidebar or homepage section.
- Configurable to use RSS, JSON feeds or third-party API.

Both features are integrated directly into the homepage and styled to match the app design.


## Tech Stack

- Python 3.13
- Django 5.2.4
- Bootstrap 5
- SQLite (development DB)
- HTML5 / CSS3
- `pytest` for automated testing

---

## Local Setup Instructions

### 1. Unpack and Open the Project
```
Download and unzip the project archive. Open the extracted folder in your preferred IDE (e.g., Visual Studio Code).
```

### 2. Create and Activate a Virtual Environment
```
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux / macOS
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```
Write your API keys to the file .env instead of:
your_openweather_api_key
your_news_api_key

Where to get the API keys?
OpenWeatherMap (for weather data):
Sign up at https://openweathermap.org/api
After registration, go to your profile → API keys.

NewsAPI (for news headlines):
Register at https://newsapi.org
Your API key will be available in your dashboard.
```

### 5. Apply Migrations
```
python manage.py migrate
```

### 6. Create Superuser Account
```
python manage.py createsuperuser
```

### 7. Run the Development Server
```
python manage.py runserver
```

Frontend:  
**http://127.0.0.1:8000/**

Backend:
**http://127.0.0.1:8000/admin**

---

## Example Admin Credentials

- Login: **admin**
- Password: **MyPassword1234@**

---

## Additional Notes
Default database: SQLite (db.sqlite3)

Sensitive data like API keys must be stored in .env

If badges or weather/news display incorrectly, verify your API keys and internet connection

**FRONTEND:**

<img width="1903" height="982" alt="image" src="https://github.com/user-attachments/assets/24eebc5a-462b-4496-8f93-1e437ca5ed60" />

**BACKEND:**

<img width="1898" height="906" alt="image" src="https://github.com/user-attachments/assets/9bfe82db-a66d-44be-83ca-0f2bee8bb7b5" />
