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

### 1. Clone the repository
Begin by cloning the project repository and navigating into the project directory:
```
git clone https://github.com/Billa-Man/swe-project.git
cd swe-project/
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment for the project:
```
# Create virtual environment
python3.12 -m venv swe_project_env

# Activate virtual environment
# For Unix/macOS:
source swe_project_env/bin/activate

# For Windows:
swe_project_env\Scripts\activate
```

### 3. Install Project Dependencies
Navigate to the `phishlearn` directory and install the required dependencies:
```
cd phishlearn
pip install --no-cache-dir -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of the project to store configuration settings:
```
nano .env
```

**Important: Paste the latest configuration from the #group-1 Slack channel to your .env and save** 

**For security reasons:**
- Never commit the .env file to version control
- Keep your API keys and passwords secure
- Make sure .env is included in your .gitignore file

# You have two options to run PhishLearn:

### Option 1: Run the Django application on local host
Start the development server using Django:
```
python manage.py runserver
```

Access the application at:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Admin Credentials:

- Username: `faculty`
- Password: `faculty` 

### Option 2: Run the Django application on Docker
If you prefer using Docker, ensure that Docker is installed on your system, then proceed with the following steps:

```
# Navigate to the phishlearn directory
docker stop $(docker ps -q)
docker build -t django-docker .
docker compose up --build
```

Access the application at:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Admin Credentials:

- Username: `faculty`
- Password: `faculty`

### (Optional) Verify API Connection

To ensure proper connectivity, visit:

[http://127.0.0.1:8000/api/connection/](http://127.0.0.1:8000/api/connection/)
