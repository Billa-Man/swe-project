# swe-project
Software Engineering Project of Group 1 - Spring 2025
# Collaborators
- Alasmari, Abdulelah
- Bandari, Sohith
- Ganesh Babu, Swetha
- Goel, Chetan
- Sundhan, Vishnu
- Zhang, Leile

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
- **Frontend:** React JS (for web) and React Native (for mobile) to provide a responsive and seamless user experience across platforms.
- **Backend:** Django with Django Rest Framework (DRF) to provide secure and scalable APIs, handle user authentication, and power the platform’s simulation logic.
- **Database:** Firebase will be used for its real-time database capabilities, user authentication, and seamless integration across devices.

## 1. Introduction

In today’s digital world, cybersecurity threats, specifically phishing and smishing attacks, pose a significant risk to businesses and individuals alike. These social engineering tactics are increasingly sophisticated, making it harder for employees to recognize and effectively respond to such threats. Despite technological advances, human error remains the most vulnerable point in security defenses, as employees are often the primary targets of these attacks.

Organizations need to prioritize cybersecurity awareness to prevent breaches and safeguard sensitive data. Employees must be equipped with the knowledge to identify, respond to, and avoid phishing attacks, reducing the risk of successful attacks that could compromise company resources.

## 2. Objectives
#### Goals
- **Improve End-User Phishing Awareness:** Equip employees with the tools and knowledge to identify phishing and smishing attempts.
- **Reduce the Risk of Breaches:** Lower the chances of a security breach by minimizing the effectiveness of social engineering tactics.
- **Ensure Employees Are Qualified to Work Securely:** Create a workforce that is educated on best security practices and compliant with industry cybersecurity standards.
#### Key Deliverables
- A user-friendly dashboard for IT administrators to monitor phishing awareness.
- A real-time phishing simulation system to create and send targeted phishing emails.
- An interactive training dashboard with educational modules, quizzes, and analytics.
- Progress tracking for employees to evaluate their performance and improvements in awareness. (Nice-to-have!)

## 3. Problem Statement
#### Phishing Threat Landscape
Phishing and smishing attacks have evolved in complexity, with attackers using personalized messages, fake websites, and spoofed email addresses to deceive victims. These attacks can lead to significant data breaches, financial loss, and damage to an organization’s reputation.
#### Challenges Faced by Organizations
Organizations struggle with ensuring that their employees are adequately prepared to spot and report phishing attacks. Training often lacks real-world context and fails to engage employees in a way that reinforces their learning. Additionally, traditional methods like workshops or static materials fail to measure employee comprehension and readiness.

## 4. Proposed Solution (PhishLearn)
PhishLearn will combine real-world phishing attack simulations with interactive training modules to create a continuous feedback loop. By allowing IT administrators to craft and send targeted phishing emails, PhishLearn will simulate realistic threats to assess employee vulnerabilities. Employees who fall victim to phishing attacks will then receive tailored training to improve their awareness.

## 5. Features & Functionality
#### Phishing Simulation
- **Email Spoofing:** IT administrators will be able to create phishing emails that impersonate legitimate sources.
- **Targeted User Groups:** Administrators can send phishing emails to specific teams or departments within an organization.
- **Real-Time Tracking:** Track user responses to phishing attempts, including clicks, reportings, and the completion of follow-up actions.
#### Awareness Monitoring
- **User Dashboard:** Employees will have access to a personal dashboard showing their progress in phishing awareness.
- **Reports & Analytics:** IT administrators will have detailed reports on user performance, trends in phishing awareness, and vulnerabilities within the organization.
#### Training System
- **Interactive Modules:** After falling victim to a phishing attempt, users will be prompted to complete training on identifying phishing attempts and best practices.
- **Quizzes & Assessments:** Users will be tested through quizzes to reinforce knowledge.
- **Progress Tracking:** A comprehensive tracking system will show employee progress over time.
#### Security Measures
- **User Authentication:** Robust authentication methods (e.g., JWT/OAuth) will be used to ensure secure access.
- **Email Spoofing Prevention:** PhishLearn will include built-in anti-spoofing features to ensure simulations are ethical and safe.

## 6. Target Audience
#### Primary Users
- **IT Administrators:** They will manage phishing simulations, track user awareness, and ensure the platform is effective in training employees.
- **Employees:** They will engage with phishing simulations and training modules to improve their understanding of security best practices.
#### Organizations of All Sizes
- PhishLearn will cater to small, medium, and large organizations, enabling them to tailor simulations to their specific needs and monitor user performance at scale.

## 7. Technology Stack
- **Frontend:** React JS (for web) and React Native (for mobile) to provide a responsive and seamless user experience across platforms.
- **Backend:** Django with Django Rest Framework (DRF) to provide secure and scalable APIs, handle user authentication, and power the platform’s simulation logic.
- **Database:** Firebase will be used for its real-time database capabilities, user authentication, and seamless integration across devices.

This stack ensures scalability, security, and efficiency, while also offering flexibility for future enhancements.

## 8. Implementation Plan
#### Phase 1: Research & Design (1 months)
- Define detailed system requirements.
- Conduct user research to understand needs.
- Design the platform’s UI/UX.

#### Phase 2: MVP Development (2 months)
- Build the core features (phishing simulations, user dashboard, admin interface).
- Set up database integration with Firebase.
- Implement basic email spoofing functionality and real-time tracking.

#### Phase 3: Testing & Feedback (3 weeks)
- Conduct internal testing and gather user feedback.
- Refine the system based on real-world usage and feedback.

#### Phase 4: Launch & Deployment (1 week)
- Deploy the platform for initial clients.
- Provide ongoing support and optimization.

## 9. Security Considerations
- **Data Encryption:** All user data and interactions will be encrypted in transit and at rest.
- **Authentication & Authorization:** JWT/OAuth2 will be used for secure authentication, and role-based access will ensure only authorized users can access certain features.
- **Anti-Spoofing Measures:** Phishing simulations will be designed to ensure they mimic real-world threats without putting user data at risk.

PhishLearn will provide companies with a powerful tool to proactively combat phishing and smishing threats. Through simulated attacks and real-time educational feedback, organizations will improve their employees' awareness and reduce the risk of breaches. This platform’s scalability and security features, powered by a modern tech stack, will enable PhishLearn to effectively meet the growing cybersecurity needs of businesses.

## Installation Steps

First, clone the repository
```
git clone https://github.com/Billa-Man/swe-project.git
cd swe-project/
```

### 1. Virtual Environment Setup
```
# Create virtual environment
python3 -m venv swe_project

# Activate virtual environment
# For Unix/macOS
source swe_project/bin/activate

# For Windows
# swe_project\Scripts\activate
```

### 2. Go into the directory
```
cd phishlearn
```

### 3. Install Django
```
python -m pip install django
```

### 4. Run the Django application
```
python manage.py runserver
```

### 5. Visit the link to view project 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
