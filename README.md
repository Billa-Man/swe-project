# Project: PhishLearn
## Description
**PhishLearn** is a cybersecurity awareness platform designed to enhance employees' ability to recognize and respond to phishing and smishing attacks. It provides IT administrators with a comprehensive dashboard to monitor user awareness levels by simulating real-world phishing scenarios.

Through the platform’s dashboard, administrators can craft and distribute phishing emails that mimic legitimate addresses, targeting specific user groups within the organization. By analyzing employee responses to these simulated attacks, companies can assess vulnerabilities and improve their overall security posture.

If an employee falls victim to a phishing attempt, PhishLearn provides a dedicated training dashboard with interactive learning modules, informative readings, and quizzes. These resources reinforce best practices for identifying and avoiding phishing threats.

By integrating real-world phishing simulations with targeted educational interventions, PhishLearn helps organizations strengthen their cybersecurity defenses and mitigate risks associated with social engineering attacks.

In short:

- Improve end-user phishing awareness
- Reduce the risk of breaches
- Ensure user is qualified to work 

## Technology Stack
- **Frontend:** Django
- **Backend:** Django with Django Rest Framework (DRF) to provide secure and scalable APIs, handle user authentication, and power the platform’s simulation logic.
- **Database:** Firebase will be used for its real-time database capabilities, user authentication, and seamless integration across devices.


## Collaborators
- Alasmari, Abdulelah
- Bandari, Sohith
- Ganesh Babu, Swetha
- Goel, Chetan
- Sundhan, Vishnu
- Zhang, Leile

## File Directory
```
.gitignore
phishlearn/
├── README.md
├── manage.py
├── db.sqlite3
├── phishlearn/         # Project configuration folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main/               # Main Django app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        └── home.html
```

## Installation Steps

First, clone the repository
```
git clone https://github.com/Billa-Man/swe-project.git
cd swe-project/
```

### 1. Virtual Environment Setup
```
# Create virtual environment
python3.12 -m venv swe_project_env

# Activate virtual environment
# For Unix/macOS
source swe_project_env/bin/activate

# For Windows
# swe_project_env\Scripts\activate
```

### 2. Go into the directory and install requirements
```
cd phishlearn
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```
# Create .env file
nano .env
```

**Important: Paste the latest configuration from the #group-1 Slack channel to your .env and save** 

**For security reasons:**
- Never commit the .env file to version control
- Keep your API keys and passwords secure
- Make sure .env is included in your .gitignore file

### 5. Run the Django application
```
python manage.py runserver
```

### 6. Visit the link to view project 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

**username: faculty** 

**password: faculty** 

### (Optional) Check Connection
[http://127.0.0.1:8000/api/connection/](http://127.0.0.1:8000/api/connection/)
