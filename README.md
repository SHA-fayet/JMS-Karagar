# JMS-Karagar
Its a project about Jail Management System

🏗️ Project: Jail Management System (Flask + MySQL)
✅ Core Technologies
Backend: Flask (Python)

Database: MySQL
Frontend: HTML, CSS, Bootstrap
Authentication: Session-based
Theme: Dark/jail vibes (styled with custom CSS)

🔐 Authentication and Roles
Session-based login system
Roles: admin, jailer
Unauthorized users are redirected to login

📊 Dashboard (Fully Implemented)
Total active inmates count
Total released inmates count
Today's visitor count
Upcoming releases within 7 days
Chart: Monthly admissions (admission_date group by month)

👮‍♂️ User Management
Only admin can create users (jailers)
Fields: username, password, role
Login/logout system

🔒 Inmate Management
Add, view, edit, delete inmates
Fields include:
name, gender, age, admission_date, release_date, status, crime_details, cell_id
Status: Active / Released
Assignment to cells
Linked with transfers, punishments

🧍‍♂️ Visitor Management
Track each visit to an inmate
Fields: visitor_name, inmate_id, visit_date, relation
View all visitors
Daily visitor count used in dashboard

📆 Visitor Request System (Public Access)
Public-facing form: anyone can apply for a visit
Fields: visitor_name, inmate_name, visit_date, reason
Stored in visit_requests table
Visible to jailers/admins
Option to approve/reject requests

🧳 Inmate Transfer History
Track cell transfers of inmates
Fields: inmate_id, from_cell_id, to_cell_id, transfer_date, reason
View history per inmate

🧨 Punishment Management
Add punishment records for inmates
Fields: inmate_id, punishment_type, description, date_given, duration_days
View history

🚨 Upcoming Release Alerts
Alerts for inmates releasing within next 7 days
Shown on dashboard
Stored in alerts table optionally

🔔 Notifications System
Internal notifications for:
New visitor requests
Upcoming releases
Any critical system status
Only visible to jailer/admin after login

🧠 Advanced Inmate Search
Search inmates by:
Name
Crime
Status (active/released)
Cell number
Release date range

📈 Dashboard Charts
Monthly inmate admissions (bar chart using Chart.js)
Data pulled from admission_date

🏢 Cell Management
View all cells and capacity
Assign inmates to cells
Track which cell is assigned to which inmate

🔧 Tables Used (Summary)
*users (id, username, password, role)
*inmates (name, admission_date, release_date, status, cell_id, crime)
*visitors (inmate_id, visitor_name, visit_date)
*visit_requests (public)
*transfers (inmate_id, from_cell, to_cell, transfer_date)
*punishments (inmate_id, punishment_type, duration)
*cells (id, capacity, status)
*alerts, notifications (optional/derived)

**THE STRUCTURE**

project/
├── run.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   └── db_schema.sql
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── inmates.py
│   │   ├── visitors.py
│   │   ├── punishments.py
│   │   ├── transfers.py
│   │   ├── notifications.py
│   │   ├── cells.py
│   │   ├── search.py
│   │   └── visit_request.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── inmates.html
│   │   ├── visitors.html
│   │   ├── punishments.html
│   │   ├── transfers.html
│   │   ├── notifications.html
│   │   ├── cells.html
│   │   ├── search.html
│   │   └── visit_request_form.html
│   └── static/
│       └── css/
│           └── style.css
