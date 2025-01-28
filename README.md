# swe-project
Software Engineering Project of Group 1 - Spring 2025
# Collaborators
- Alasmari, Abdulelah
- Bandari, Sohith
- Ganesh Babu, Swetha
- Goel, Chetan
- Sundhan, Vishnu
- Zhang, Leile

# Project Ideas
## 1. ResAI
### Description
ResAI is a web application designed to assist job seekers by providing tools for resume building, tailoring, and job matching.

### Problem

The competitive computer science job market presents challenges for job seekers in standing out and securing roles. ResAI addresses these issues by offering advanced resume optimization, tailored job suggestions, and enhanced job-matching capabilities, improving users’ chances of landing interviews and making meaningful connections.

### Targeted Users

- Job seekers
  - Individuals actively looking for jobs in various industries.
  - Use the platform to build resumes, tailor applications, and find relevant job opportunities.

- Recruiters
  - Professionals or companies seeking qualified candidates.
  - Use the platform to search for resumes, post job openings, and identify top matches.

### Major Features
- **Resume Rating:** Evaluate resumes against job descriptions to provide a score and feedback on alignment.
- **Resume Matching:** Match job seekers' resumes with job postings based on qualifications, experience, and skills.
- **Resume Tailoring:** Suggest optimizations to resumes to better fit specific roles and job requirements.
- **Job Suggestions:** Provide personalized job recommendations based on the user’s qualifications, preferences, and experience.

### Minimum Viable Product

- **Dashboard:** Central hub to manage resumes, applications, and recommendations.
- **Resume Rating Based on Job Descriptions:** Provide a rating system and feedback for resumes tailored to specific jobs.
- **Cover Letter Generation:** Automatically create personalized cover letters for job applications.

### Minimum Lovable Product
- **Automatic Job Application Tracking:** Track applied jobs, statuses, and deadlines.
- **AI-Powered Resume Tailoring:** Allow users to upload job descriptions to get resume suggestions for optimized keyword alignment.
- **Custom Job Alerts:** Notify users of new job postings tailored to their profile.
- **Job Scraping:** Automatically pull job postings from multiple platforms based on location, qualifications, and keywords.
  
### Nice-to-Haves
- **Connection Suggestions Based on Resume Qualifications:** Recommend relevant professionals, mentors, or recruiters to network with.
- **Skill Gap Analysis:** Identify missing skills for target roles and provide Personalized Learning Recommendations (e.g., courses or certifications).
- **Application Templates:** Provide customizable application templates for different industries.
- **Job Interview Preparation:** Offer AI-powered mock interviews and suggested responses based on common questions for the role.
- **Salary Insights:** Display salary ranges for target roles based on location and qualifications.
- **Social Media Profile Enhancement:** Suggest updates to LinkedIn or other professional profiles based on the user’s resume.
- **Language Optimization:** Offer grammar, tone, and language improvements for resumes and cover letters.
- **Global Job Opportunities:** Include a feature to search for international job postings with visa and relocation details.

### CRUD (Create, Read, Update, Delete) Operations
#### Admin
- **Create:** Automated Workflow (Email Notification from platform)
- **Read:** Take a look at all accounts and application statistics
- **Update:** Manage User roles / Permissions
- **Delete:** Remove job postings or inappropriate users

#### Persona 1: Job Seekers

- **Create:** Create a new profile, add education and experiences
- **Read:** Explore job descriptions, application statuses, job dashboard
- **Update:** Edit resumes, Job Preferences, enhance profile details with new skills or qualifications.
- **Delete:** Deactivate Account, Remove outdated resumes, cover letters, or account data.

#### Persona 2: Recruiters

- **Create:** Post job openings, add keywords for optimized candidate matching
- **Read:** Review applicant resumes, view matched candidates, and access analytics on posting performance.
- **Update:** Modify job descriptions, adjust candidate requirements
- **Delete:** Remove job postings, archive old Job Postings or delete outdated postings and profiles.

### Existing Applications
**1. Job Right AI** [Link](https://jobright.ai/): Helps job seekers upload resumes and fetch relevant job postings. Also features AI-powered resume optimization.

**2. Simplify Jobs** [Link](https://simplify.jobs/): Autofills job applications using user profiles and resumes, optimizing resumes and allowing candidates to track applications and bookmark jobs.


**3. Huntr** [Link](https://huntr.co/): Organizes Job applications, users can manually track their applications and integrate with email for tracking too, providing a centralized platform for job seekers.


## 2. RapidRead
### Description
A news application designed to deliver concise summaries of news articles tailored to users’ interests. The app incorporates an intuitive “swipe-to-like” mechanism, allowing users to swipe right if they like an article or left if they do not. Over time, the app personalizes the news feed based on the user’s swiping behavior, ensuring a tailored and relevant experience. By focusing on delivering shortened content, the application caters to the needs of modern users with limited attention spans.

### Problem
- Difficulty in consuming long-form content during busy schedules and short attention span.
- Information overload from traditional news platforms.
- Lack of customization and personalization in most news apps.

### Targeted Users

- Professionals who need quick, relevant updates on industry news, allowing them to stay informed.
- Casual readers who want a broad awareness.
- Students who need simplified, educational content

### Major Features
- **News Summarization:** Extract and summarize articles using AI models for quick reading.
- **Personalized News Feed:** Adaptive feed tailored to user interactions and preferences.
- **Swipe-to-Like:** Intuitive swiping to like or dislike articles, refining recommendations.
- **Community Features:** Engage with comments, likes, sharing, and bookmarking articles.

### Minimum Viable Product

- Personalized news feed based on categories/topics chosen by users.
- Summaries of articles.
- User profile creation 
- Interactive swipe functionality for liking or disliking articles, refining recommendations over time.

### Minimum Lovable Product
- Insights into users’ preferences based on their interactions.
- Community Features such as comments, likes, and sharing options for articles.	
  
### Nice-to-Haves
- Offline reading capabilities.
- Content filters for specific news type 

### CRUD (Create, Read, Update, Delete) Operations
#### Admin
- **Create:** Add new news sources or integrate with APIs, create content categories.
- **Read:** Analyze user interaction reports (e.g., swipe behavior)
- **Update:** Modifies and updates existing articles, notification settings, or saved items.
- **Delete:** Remove outdated or irrelevant new articles

#### Persona 1: Professionals, casual reader, students

- **Create:** Create a user profile with preferences based on their choices
- **Read:** Read concise summaries of articles
- **Update:** Update preferences, notification settings, or saved items.
- **Delete:** Delete saved bookmarks, deactivate accounts.

#### Persona 2: Journalist

- **Create:** Write and publish original articles, investigative reports, and feature stories.
- **Read:** Access and analyze articles, reports, or publications from other journalists and media outlets for research and inspiration.
- **Update:** Edit and refine AI-generated summaries or drafts to ensure factual accuracy, clarity, and alignment with journalistic standards.
- **Delete:** Remove outdated, irrelevant, or incorrect articles from their portfolio or publication database.

### Existing Applications
**1. Inshorts** [Link](https://inshorts.com/en/read): Gives users concise news summaries but does not emphasize personalized feeds.

**2. Google News** [Link](https://news.google.com/home?hl=en-US&gl=US&ceid=US:en): Autofills job applications using user profiles and resumes, optimizing resumes and allowing candidates to track applications and bookmark jobs.

**3. Pocket** [Link](https://getpocket.com/home): Unlike RapidRead, it does not summarize content but emphasizes saving and consuming it late.

## 3. PhishLearn
### Description
- We are developing a dashboard that enables a company’s IT administrators to monitor the cybersecurity awareness of their users by sending them different sorts of Phishing/Smishing emails that simulate an attack. The application provides functionality to spoof any email address the email is coming from, send it to a list of email addresses and generate a template for the phishing email. 
- If the user falls victim to the email, we have another user fronting dashboard that consists of training the user. Training consists of some reading and interactive quizzes.

### Problem

- Improve end-user awareness
- Reduce the risk of breaches

### Targeted Users

- **IT administrators:** the IT department of the organization
- **End user:** someone who would interact with this website to complete the lessons

### Major Features
- **IT Administrator Dashboard:**
  - Create, customize and send phishing emails to different users from different email addresses
  - Monitor and track phishing “victims”
  - Record user actions (e.g., clicked on the link, entered credentials)
- **User-Facing Dashboard:**
  - Interactive training modules for users
  - Learning material covering phishing and smishing awareness and answering questions in the form of quizzes
- **Analytics & Reporting:**
  - Real-time monitoring of simulation campaigns
  - Aggregated statistics like the percentage of users falling for phishing attempts
  - Comparative analysis of awareness improvements over time

### Minimum Viable Product
- Admin dashboard with the ability to send phishing emails from any email address and to a list of email addresses
- Ability to track whether a user interacts with the phishing email and displaying statistics for the admin
- User facing dashboard where the user reads articles and answers questions as part of a quiz

### Minimum Lovable Product
- Interactive graphs and detailed analytics regarding user click through rate and security trends
- More engaging user dashboard including videos/games
- Create new email templates to stay updated with newer scams

### Nice-to-Haves
- Some form of social media phishing
- Additional modules for simulating other cyber attacks

### CRUD (Create, Read, Update, Delete) Operations
#### Admin
- **Create:** New admin accounts, new email templates, new simulated threats
- **Read:** View all accounts, access system logs
- **Update:** Edit admin permissions or roles, update email templates
- **Delete:** Remove admin accounts, delete outdated email templates

#### Persona 1: IT administrators

- **Create:** New user accounts, new training modules
- **Read:** Analysis reports, logs of user training progress
- **Update:** Assign users to training, update user roles
- **Delete:** Delete inactive users, delete outdated training modules

#### Persona 2: Users

- **Create:** New user profile.
- **Read:** Review assigned training, access test scores.
- **Update:** Update profile information eg. password, email etc.
- **Delete:** Delete own account.

### Existing Applications
**1. KnowBe4** [Link](https://www.knowbe4.com): Offers phishing security tests and training.

**2. PhishMe(Cofense)** [Link](https://cofense.com): Focuses on phishing simulations and threat reporting.

**3. Terranova Security** [Link](https://www.terranovasecurity.com): Provides phishing simulations and interactive eLearning.

# Environment Setup
First, clone the repository
```
git clone https://github.com/Billa-Man/swe-project.git
cd <project-directory>
```

### 1. Virtual Environment Setup
Create and activate a Python virtual environment:
```
# Create virtual environment
python3 -m venv swe_project

# Activate virtual environment
# For Unix/macOS
source swe_project/bin/activate

# For Windows
# swe_project\Scripts\activate
```
