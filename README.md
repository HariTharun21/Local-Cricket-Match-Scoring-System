<h1>🏏Local Cricket Match Scoring System</h1>

A web-based application built using Django to track and manage gully cricket matches with real-time ball-by-ball scoring.

<h3>🚧 **Project Status: In Progress**</h3>

This is a Django-based web application for scoring local cricket matches ball-by-ball.

⚠️ Note:
- This project is still under development
- Some features may not work fully
- Improvements and updates are ongoing

<h2>📖 Project Description</h2>

The Local Match Scoring System is a web-based application developed using Django that enables users to efficiently manage and track gully cricket matches in real time. This system is designed to simplify the traditional manual scoring process by providing a digital platform for ball-by-ball score updates, player management, and match history storage.

The application allows users to create matches, assign players (batsmen and bowlers), and update scores dynamically using an interactive interface. It incorporates intelligent features such as automatic strike rotation, handling of extras like no-balls, and generation of over-wise summaries, ensuring an accurate and smooth scoring experience.

To enhance usability and security, the system implements role-based access control, where normal users can only view match details, while admin and authorized users can add or modify scores. Additionally, the application integrates with ServiceNow for issue reporting and tracking, enabling users to report problems and monitor their resolution status efficiently.

With a mobile-friendly design and a scalable architecture, this project can be used in local tournaments, street cricket matches, or small-scale leagues, providing a reliable and user-friendly solution for real-time cricket scoring.

<h2>📌 Features</h2>
📊 Create and manage multiple matches<br>
🧑‍🤝‍🧑 Add players (batsmen & bowlers)<br>
🏏 Ball-by-ball scoring system<br>
🔄 Automatic strike rotation<br>
🚫 No-ball and wicket handling<br>
📈 Live score updates<br>
📝 Over summary tracking<br>
💾 Save match history in database<br>
📱 Mobile-friendly interface<br>
<h3>🔐 Access Control & User Roles</h3>
👀 Viewer (Normal User): Can only view live scores and match details<br>
🧑‍💼 Admin: Full access to all features<br>
✅ Admin-Approved Users: Can add/edit scores and match details<br>
<h3>🛠️ Issue Reporting & Integration</h3>
📝 Raise issues directly from the application<br>
🔗 Integration with ServiceNow for issue tracking and management<br>
📌 Track status of reported issues (Open / In Progress / Resolved)

<h3>🛠️ Tech Stack</h3>
Backend: Django (Python)<br>
Frontend: HTML, CSS, JavaScript<br>
Database: Oracle<br>
Version Control: Git & GitHub

<h2>📂 Project Structure</h2>
<pre>
cricket/
│
├── access/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── cricket/
│   ├── models.py
│   ├── settings.py
│   ├── views.py
│   └── urls.py
│
├── score/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── servicenow_client.py
│   └── admin.py
│   
└── static/</pre>

<h2>⚙️ Installation & Setup</h2>
<pre>
<h3>Clone the repository</h3>
git clone <a href="https://github.com/HariTharun21/Local-Cricket-Match-Scoring-System.git" target="_blank">repository link</a><br>
cd cricket
<h3>Create virtual environment</h3>
python -m venv venv
venv\Scripts\activate   # Windows
<h3>Install dependencies</h3>
pip install -r requirements.txt
<h3>Apply migrations</h3>
python manage.py makemigrations
python manage.py migrate
<h3>Run server</h3>
python manage.py runserver
<h3>Open in browser</h3>
http://127.0.0.1:8000/</pre>

<h2>Project Demo Video</h2>
 🎥<br>

[![Watch Demo](https://img.shields.io/badge/▶️%20Watch%20Full%20Video-YouTube-red?style=for-the-badge)](https://youtu.be/NTZUaeoIBQ8)
