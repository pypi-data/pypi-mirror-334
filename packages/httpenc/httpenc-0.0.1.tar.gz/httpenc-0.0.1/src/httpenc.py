def create():
    index_code = """
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}

<!-- Hero Section -->
<section id="hero" class="text-center">
  <div class="container-fluid px-4">
    <h1 class="display-4">Welcome to FlagQuest</h1>
    <p class="lead">Embark on your cybersecurity learning journey through interactive challenges and real-world puzzles.</p>
    <a href="{{ url_for('learning_paths') }}" class="btn btn-primary btn-lg mt-3">Explore Learning Paths</a>
  </div>
</section>

<!-- Features Section -->
<section id="features" class="py-5">
  <div class="container-fluid px-4">
    <div class="row text-center">
      <div class="col-md-4">
        <img src="{{ url_for('static', filename='icon_challenge.svg') }}" alt="Interactive Challenges" style="height: 60px;">
        <h4 class="mt-3">Interactive Challenges</h4>
        <p>Engage in real-time CTF challenges designed for all skill levels.</p>
      </div>
      <div class="col-md-4">
        <img src="{{ url_for('static', filename='icon_learning.svg') }}" alt="Personalized Learning" style="height: 60px;">
        <h4 class="mt-3">Personalized Learning Paths</h4>
        <p>Follow tailored modules that adapt to your progress and interests.</p>
      </div>
      <div class="col-md-4">
        <img src="{{ url_for('static', filename='icon_leaderboard.svg') }}" alt="Real-Time Leaderboard" style="height: 60px;">
        <h4 class="mt-3">Real-Time Leaderboard</h4>
        <p>Compete with peers and track your progress live.</p>
      </div>
    </div>
  </div>
</section>

<!-- Latest Challenges Section -->
<section id="latest-challenges" class="py-5 bg-light">
  <div class="container-fluid px-4">
    <h2 class="mb-4 text-center">Latest Challenges</h2>
    <div class="row">
      {% for id, challenge in challenges.items() %}
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card challenge-card">
          <div class="card-header">
            {{ challenge.title }}
          </div>
          <div class="card-body">
            <p class="card-text">Category: {{ challenge.category }}</p>
            <a href="{{ url_for('challenge', challenge_id=id) }}" class="btn btn-primary">Solve Challenge</a>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<!-- Learn More Section -->
<section id="learn-more" class="py-5">
  <div class="container-fluid px-4 text-center">
    <h2>New to Cyber Security?</h2>
    <p class="lead">Start your journey with our comprehensive, step-by-step learning modules designed for beginners.</p>
    <a href="{{ url_for('learning_items_route') }}" class="btn btn-primary btn-lg">Learn Now</a>
  </div>
</section>

<!-- Testimonials Section -->
<section id="testimonials" class="py-5">
  <div class="container-fluid px-4">
    <h2 class="mb-4 text-center">What Our Users Say</h2>
    <div class="row">
      <div class="col-md-4">
        <blockquote class="blockquote text-center">
          <p class="mb-0">"FlagQuest made learning cybersecurity fun and engaging!"</p>
          <footer class="blockquote-footer">Alice</footer>
        </blockquote>
      </div>
      <div class="col-md-4">
        <blockquote class="blockquote text-center">
          <p class="mb-0">"I love the interactive challenges and personalized paths."</p>
          <footer class="blockquote-footer">Bob</footer>
        </blockquote>
      </div>
      <div class="col-md-4">
        <blockquote class="blockquote text-center">
          <p class="mb-0">"The real-time leaderboard keeps me motivated every day!"</p>
          <footer class="blockquote-footer">Carol</footer>
        </blockquote>
      </div>
    </div>
  </div>
</section>

<!-- Call to Action Section -->
<section id="cta" class="text-center">
  <div class="container-fluid px-4">
    <h2 class="mb-4">Ready to embark on your cybersecurity journey?</h2>
    <a href="{{ url_for('register') }}" class="btn btn-light btn-lg">Join Now</a>
  </div>
</section>

{% endblock %}
    """

    base_code = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FlagQuest - {% block title %}{% endblock %}</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <!-- Custom Styles -->
  <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
  <!-- Add link to custom font -->
  <link rel="stylesheet" href="{{ url_for('static', filename='fonts/CustomFont.ttf') }}">
  <!-- Optional: Google Fonts (e.g., Roboto) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>

  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
    <a class="navbar-brand d-flex align-items-center" href="{{ url_for('index') }}">
      <img src="{{ url_for('static', filename='logo.svg') }}"
           style="height: 40px; width: auto; margin-right: 8px;"
           alt="FlagQuest Logo">
      <span></span>
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item"><a class="nav-link" href="{{ url_for('index') }}">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('learning_paths') }}">Learning Paths</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('learning_items_route') }}">Learn Cyber Security</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('dashboard') }}">Dashboard</a></li>
      </ul>
      <ul class="navbar-nav">
        {% if current_user.is_authenticated %}
          <li class="nav-item"><a class="nav-link" href="#">{{ current_user.username }}</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('logout') }}">Logout</a></li>
        {% else %}
          <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('register') }}">Register</a></li>
        {% endif %}
      </ul>
    </div>
  </nav>

  <!-- Main Content: full-width with padding -->
  <div class="container-fluid mt-4 px-4">
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for message in messages %}
          <div class="alert alert-warning">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </div>

  <!-- Footer: also full-width with padding -->
  <footer class="footer">
    <div class="container-fluid text-center px-4">
      <p class="mb-2">© 2025 FlagQuest. All rights reserved.</p>
      <div class="footer-links">
        <a href="#">Privacy Policy</a> |
        <a href="#">Contact</a>
      </div>
    </div>
  </footer>

  <!-- Optional Bootstrap JS -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """

    challenge_code = """
{% extends "base.html" %}
{% block title %}{{ challenge.title }}{% endblock %}
{% block content %}
<h2>{{ challenge.title }}</h2>
<p>{{ challenge.description }}</p>
<p><strong>Category:</strong> {{ challenge.category }}</p>

{% if message %}
  <div class="alert alert-info">{{ message }}</div>
{% endif %}

<!-- Form for flag submission -->
<form method="POST" class="mb-3">
  <div class="form-group">
    <label for="flag">Enter Flag:</label>
    <input type="text" class="form-control" id="flag" name="flag" placeholder="flag{...}">
  </div>
  <button type="submit" name="action" value="submit" class="btn btn-primary">Submit Flag</button>
</form>

<!-- Button to request hint -->
<form method="POST">
  <button type="submit" name="action" value="hint" class="btn btn-warning">Show Hint (Costs 10 points)</button>
</form>

<a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Back to Challenges</a>
{% endblock %}
"""

    dashboard_code = """
{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<h1 class="mt-4">Dashboard</h1>
<p><strong>Total Points:</strong> {{ points }}</p>
<h3>Completed Challenges</h3>
{% if completed %}
  <ul class="list-group">
    {% for cid, chal in completed.items() %}
      <li class="list-group-item">
        {{ chal.title }} (Category: {{ chal.category }})
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>You haven't completed any challenges yet.</p>
{% endif %}
{% endblock %}
"""

    learning_items_code = """
{% extends "base.html" %}
{% block title %}Learn Cyber Security from Scratch{% endblock %}
{% block content %}
<section id="learning-path" class="py-5">
  <div class="container">
    <h1 class="text-center mb-4">Learn Cyber Security from Scratch</h1>
    <p class="lead text-center mb-5">Whether you’re completely new or looking to strengthen your fundamentals, follow our guided modules to master cybersecurity.</p>
    <div class="row">
      {% for id, item in learning_items.items() %}
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card challenge-card h-100">
          <div class="card-header">
            {{ item.title }}
          </div>
          <div class="card-body">
            <p>{{ item.description }}</p>
            <h6>Resources:</h6>
            <ul>
              {% for resource in item.resources %}
              <li><a href="{{ resource.url }}" target="_blank">{{ resource.title }}</a></li>
              {% endfor %}
            </ul>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>
{% endblock %}
"""

    learning_paths_code = """
{% extends "base.html" %}
{% block title %}Learning Paths{% endblock %}
{% block content %}
<h1 class="mt-4">Learning Paths</h1>
{% for category, challenges_list in paths.items() %}
  <h3 class="mt-4">{{ category }}</h3>
  <div class="list-group">
    {% for cid, chal in challenges_list %}
      <a href="{{ url_for('challenge', challenge_id=cid) }}" class="list-group-item list-group-item-action">
        {{ chal.title }}
      </a>
    {% endfor %}
  </div>
{% endfor %}
{% endblock %}
"""

    login_code = """
{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<h2>Login</h2>
<form method="POST">
  <div class="form-group">
    <label for="username">Username:</label>
    <input type="text" class="form-control" id="username" name="username" required>
  </div>
  <div class="form-group">
    <label for="password">Password:</label>
    <input type="password" class="form-control" id="password" name="password" required>
  </div>
  <button type="submit" class="btn btn-primary">Login</button>
</form>
{% endblock %}
"""

    register_code = """
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<h2>Register</h2>
<form method="POST">
  <div class="form-group">
    <label for="username">Username:</label>
    <input type="text" class="form-control" id="username" name="username" required>
  </div>
  <div class="form-group">
    <label for="password">Password:</label>
    <input type="password" class="form-control" id="password" name="password" required>
  </div>
  <button type="submit" class="btn btn-primary">Register</button>
</form>
{% endblock %}
"""

    styles_code = """
/* Global Styles */
@font-face {
    font-family: 'CustomFont';
    src: url('../fonts/CustomFont.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}
body {
    font-family: 'Roboto', sans-serif;
    background-color: #f7f7f7;
    margin: 0;
    padding: 0;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'CustomFont', sans-serif;
}

/* Navbar Customization */
.navbar-custom {
    background-color: #4caf50;
    transition: background-color 0.3s;
}
.navbar-custom .navbar-brand,
.navbar-custom .navbar-link,
.navbar-custom .nav-link {
    color: #fff !important;
}
.navbar-custom .nav-link:hover {
    color: #e8f5e9 !important;
}

/* Hero Section */
#hero {
    background-color: #e8f5e9;
    padding: 80px 0;
    transition: background-color 0.3s;
}
#hero h1 {
    font-size: 3rem;
    font-weight: bold;
}
#hero p.lead {
    font-size: 1.25rem;
}

/* Features Section */
#features {
    padding: 60px 0;
    transition: padding 0.3s;
}
#features img {
    margin-bottom: 15px;
}

/* Latest Challenges Section */
#latest-challenges {
    background-color: #fff;
    padding: 60px 0;
    transition: background-color 0.3s, padding 0.3s;
}
.challenge-card {
    border: none;
    border-radius: 8px;
    background-color: #fff;
    transition: transform 0.2s, box-shadow 0.2s;
}
.challenge-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.challenge-card .card-header {
    background-color: #4caf50;
    color: #fff;
    font-weight: bold;
}

/* Testimonials Section */
#testimonials {
    padding: 60px 0;
    background-color: #f1f1f1;
    transition: background-color 0.3s, padding 0.3s;
}
blockquote {
    border-left: 4px solid #4caf50;
    padding-left: 15px;
}

/* Call to Action Section */
#cta {
    background-color: #4caf50;
    color: #fff;
    padding: 60px 0;
    border-radius: 8px;
    transition: background-color 0.3s, padding 0.3s;
}


.footer {
    background-color: #4caf50;
    color: #fff;
    padding: 20px 0;
    margin-top: 40px;
    transition: background-color 0.3s, padding 0.3s;
}
.footer a {
    color: #fff;
}
.footer a:hover {
    text-decoration: underline;
}

/* Button Overrides */
.btn-primary {
    background-color: #4caf50;
    border-color: #43a047;
    transition: background-color 0.3s, border-color 0.3s;
}
.btn-primary:hover {
    background-color: #43a047;
    border-color: #388e3c;
}
"""

    app_code = """
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/flagquest"
mongo = PyMongo(app)

challenges = {
    1: {
        "title": "Basic Web Challenge",
        "description": "Check the page source to find hidden clues and retrieve the flag.",
        "category": "Web Security",
        "flag": "flag{basic_web_challenge}",
        "hint": "Right-click → View Page Source. Keep an eye out for hidden comments or parameters.",
        "points": 100
    },
    2: {
        "title": "SQL Injection Challenge",
        "description": (
            "An insecure login form might allow you to bypass authentication or extract data "
            "from the database. Try typical SQL injection payloads."
        ),
        "category": "Web Security",
        "flag": "flag{sql_injection_success}",
        "hint": "Use common SQL injection techniques like ' OR '1'='1' --",
        "points": 200
    },
    3: {
        "title": "Cross-Site Scripting (XSS)",
        "description": (
            "Find a vulnerable input field that doesn't sanitize user input, and inject a "
            "malicious script to display an alert."
        ),
        "category": "Web Security",
        "flag": "flag{xss_attack_success}",
        "hint": "Look for a parameter in the URL or form input that reflects your input back onto the page.",
        "points": 150
    },
    4: {
        "title": "Basic Cryptography",
        "description": "Decode a Base64 string and see if you can decrypt the hidden message.",
        "category": "Cryptography",
        "flag": "flag{crypto_decrypted}",
        "hint": "Use an online Base64 decoder or a command-line tool like base64.",
        "points": 100
    },
    5: {
        "title": "Command Injection",
        "description": (
            "A vulnerable parameter might allow OS commands to run on the server. "
            "Find the parameter and run 'whoami' or 'ls' to discover the flag."
        ),
        "category": "System Security",
        "flag": "flag{cmd_injection_found}",
        "hint": "Look for a field that might pass your input to a system command (ping, for example).",
        "points": 250
    }
}

learning_items = {
    1: {
        "title": "Introduction to Cyber Security",
        "description": (
            "Learn the basics of cyber security, the CIA triad (Confidentiality, Integrity, "
            "Availability), and common threat actors."
        ),
        "resources": [
            {
                "title": "What is Cyber Security? (CISA)",
                "url": "https://www.cisa.gov/uscert/ncas/tips/ST04-001"
            },
            {
                "title": "TryHackMe Pre-Security Path (Free Intro)",
                "url": "https://tryhackme.com/path/outline/presecurity"
            }
        ]
    },
    2: {
        "title": "Linux Fundamentals",
        "description": (
            "Understand the basics of Linux, commonly used commands, and how to set up a "
            "hacking environment."
        ),
        "resources": [
            {
                "title": "Kali Linux Official Docs",
                "url": "https://www.kali.org/docs/"
            },
            {
                "title": "Linux Fundamentals (TryHackMe)",
                "url": "https://tryhackme.com/room/linuxfundamentals"
            }
        ]
    },
    3: {
        "title": "Web Security Basics",
        "description": (
            "Dive into the fundamentals of web security, including the OWASP Top 10. "
            "Learn about common vulnerabilities like SQL injection, XSS, and more."
        ),
        "resources": [
            {
                "title": "OWASP Top 10 Official Page",
                "url": "https://owasp.org/www-project-top-ten/"
            },
            {
                "title": "PortSwigger Web Security Academy",
                "url": "https://portswigger.net/web-security"
            }
        ]
    },
    4: {
        "title": "Cryptography 101",
        "description": (
            "An introduction to encryption, hashing, and how cryptography protects information "
            "in transit and at rest."
        ),
        "resources": [
            {
                "title": "Cryptography Basics (Stanford)",
                "url": "https://crypto.stanford.edu/~dabo/cs255/"
            },
            {
                "title": "Practical Cryptography (MDN)",
                "url": "https://developer.mozilla.org/en-US/docs/Web/Security"
            }
        ]
    }
}


# Set up Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Define a User class that integrates with Flask-Login
class User(UserMixin):
    def __init__(self, user_dict):
        self.id = str(user_dict['_id'])
        self.username = user_dict['username']
        self.password = user_dict['password']
        self.points = user_dict.get('points', 0)
        self.badges = user_dict.get('badges', [])

# User loader callback: fetch user from MongoDB by ID
@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(user)
    return None

# Sample challenges data stored as a Python dictionary (could later be stored in Mongo too)
challenges = {
    1: {
        "title": "Basic Web Challenge",
        "description": "Find the hidden flag in the HTML comments of this page.",
        "flag": "flag{hidden_in_html}",
        "hint": "View the page source in your browser to see hidden comments.",
        "category": "Web Security",
        "points": 100,
        "resources": [
            {"title": "HTML Comments Tutorial", "url": "https://example.com/html-comments"}
        ]
    },
    2: {
        "title": "Simple Cryptography",
        "description": "Decode the Base64 encoded string to find the flag: ZmxhZ3t1bmxvY2tlZF9jb2RlX2ludmFsaWR9",
        "flag": "flag{unlocked_code_invalid}",
        "hint": "Use an online Base64 decoder to decode the string.",
        "category": "Cryptography",
        "points": 150,
        "resources": [
            {"title": "Base64 Guide", "url": "https://example.com/base64-guide"}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', challenges=challenges)

# ---------------------------
# User Registration and Login
# ---------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if user already exists
        if mongo.db.users.find_one({"username": username}):
            flash("Username already exists!")
            return redirect(url_for('register'))
        # Create new user document with hashed password
        new_user = {
            "username": username,
            "password": generate_password_hash(password),
            "points": 0,
            "badges": []
        }
        mongo.db.users.insert_one(new_user)
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_doc = mongo.db.users.find_one({"username": username})
        if user_doc and check_password_hash(user_doc['password'], password):
            user = User(user_doc)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!")
    return render_template('login.html')

@app.route('/learning_items')
def learning_items_route():
    return render_template('learning_items.html', learning_items=learning_items)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ---------------------------
# Main Application Routes
# ---------------------------

# Dashboard: Show User Progress and Points (stored in MongoDB)
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user's completed challenge IDs from the challenge_progress collection
    progress_docs = mongo.db.challenge_progress.find({"user_id": current_user.id})
    completed_ids = [doc['challenge_id'] for doc in progress_docs]
    completed_challenges = {cid: challenges[cid] for cid in completed_ids if cid in challenges}
    
    # Refresh current_user points from the database
    user_doc = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    points = user_doc.get("points", 0)
    
    return render_template('dashboard.html', points=points, completed=completed_challenges)

# Learning Paths: Group challenges by category
@app.route('/learning_paths')
def learning_paths():
    paths = {}
    for cid, chal in challenges.items():
        cat = chal.get("category", "General")
        paths.setdefault(cat, []).append((cid, chal))
    return render_template('learning_paths.html', paths=paths)

# Challenge Route: Solve Challenge, Update Points and Progress
@app.route('/challenge/<int:challenge_id>', methods=['GET', 'POST'])
@login_required
def challenge(challenge_id):
    challenge = challenges.get(challenge_id)
    if not challenge:
        flash("Challenge not found!")
        return redirect(url_for('index'))
    
    message = None
    if request.method == 'POST':
        if request.form.get('action') == 'hint':
            message = f"Hint: {challenge['hint']}"
            # Deduct points for a hint (update user in MongoDB)
            mongo.db.users.update_one(
                {"_id": ObjectId(current_user.id)},
                {"$inc": {"points": -10}}
            )
        else:
            user_flag = request.form.get('flag')
            if user_flag == challenge["flag"]:
                message = "Correct! You solved the challenge!"
                # Check if challenge already solved
                if not mongo.db.challenge_progress.find_one({"user_id": current_user.id, "challenge_id": challenge_id}):
                    # Award points for the challenge
                    mongo.db.users.update_one(
                        {"_id": ObjectId(current_user.id)},
                        {"$inc": {"points": challenge['points']}}
                    )
                    # Record the challenge as completed
                    mongo.db.challenge_progress.insert_one({
                        "user_id": current_user.id,
                        "challenge_id": challenge_id
                    })
            else:
                message = "Incorrect flag, try again."
    return render_template('challenge.html', challenge=challenge, message=message)

# ---------------------------
# Real-Time Leaderboard API
# ---------------------------

@app.route('/api/leaderboard')
def leaderboard():
    # Fetch top 10 users sorted by points
    top_users = mongo.db.users.find().sort("points", -1).limit(10)
    leaderboard_data = [{"username": u["username"], "points": u.get("points", 0)} for u in top_users]
    return jsonify(leaderboard_data)

# ---------------------------
# Admin Panel (Example for Adding Challenges)
# ---------------------------

@app.route('/admin/add_challenge', methods=['GET', 'POST'])
@login_required
def add_challenge():
    # Simple admin check (replace with proper role-based logic)
    if current_user.username != 'admin':
        flash("Access denied.")
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        flag = request.form.get('flag')
        hint = request.form.get('hint')
        category = request.form.get('category')
        points = int(request.form.get('points'))
        # For now, simply flash a message; in production, you might store challenges in MongoDB too.
        flash("Challenge added! (Implement persistent storage for challenges.)")
        return redirect(url_for('index'))
    return render_template('admin_add_challenge.html')

if __name__ == '__main__':
    app.run(debug=True)
"""

    with open("base.html", "w", encoding="utf-8") as file:
        file.write(base_code)

    with open("challenge.html", "w", encoding="utf-8") as file:
        file.write(challenge_code)

    with open("dashboard.html", "w", encoding="utf-8") as file:
        file.write(dashboard_code)

    with open("learning_items.html", "w", encoding="utf-8") as file:
        file.write(learning_items_code)

    with open("learning_paths.html", "w", encoding="utf-8") as file:
        file.write(learning_paths_code)

    with open("login.html", "w", encoding="utf-8") as file:
        file.write(login_code)

    with open("register.html", "w", encoding="utf-8") as file:
        file.write(register_code)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(index_code)

    with open("styles.css", "w", encoding="utf-8") as file:
        file.write(styles_code)

    with open("app.py", "w", encoding="utf-8") as file:
        file.write(app_code)

# create()