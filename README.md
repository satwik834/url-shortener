# URL Shortener Web App

A full-stack Flask application to shorten URLs, track user-specific links, and view analytics like click counts. Includes user authentication with session-based login, a clean dashboard interface, and support for anonymous URL shortening.

## Features

- User registration and login with secure password hashing
- Session-based authentication
- User-specific dashboard to manage shortened URLs
- Anonymous URL shortening for non-logged-in users
- Base62-encoded short URLs (derived from database IDs)
- Redirects to original URLs using encoded short IDs
- Click tracking for each shortened URL
- PostgreSQL (or SQLite) database with SQLAlchemy ORM

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, Bootstrap (optional)
- **Database**: PostgreSQL (can switch to SQLite)
- **Auth**: Sessions, Flask-Bcrypt for password hashing

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your database**
   Update the `SQLALCHEMY_DATABASE_URI` in `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/yourdbname'
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Access the app**
   Open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure

```
url-shortener/
│
├── app.py                # Main Flask app
├── models.py             # SQLAlchemy models
├── database.py           # DB setup/init
├── helpers.py            # base62 encode/decode functions
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/               # (Optional) CSS, JS files
├── requirements.txt
└── README.md
```

## Notes

- Short URLs are not stored in the database; they are generated dynamically using base62-encoded primary keys.
- Click counts are tracked per short URL.
