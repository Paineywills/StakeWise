# 🎲 Stakewise

Stakewise is a sports betting web application built with **Django**.  
It allows users to register, deposit funds, place bets, and track their wins in real-time.

---

## 🚀 Features

- 🔐 **User Authentication** (Register, Login, Logout)
- 🏦 **Deposit & Withdraw** system
- 📊 **Dashboard**
  - Logged-in users: personalized betting stats
  - Visitors: preview of games & promotions
- 🎯 **Betting System** with outcomes
- 🛡️ **Secure sessions & CSRF protection**
- 📱 **Responsive UI** (desktop & mobile friendly)
- 🍪 **Cookie Consent Banner** (GDPR-ready)
- 📄 **Terms & Privacy Page**

---

## 🛠️ Tech Stack

- **Backend**: Django 5.x (Python 3.13)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Database**: SQLite (default, can switch to PostgreSQL/MySQL)
- **Auth**: Django’s built-in authentication
- **Styling**: Custom CSS (extendable with Tailwind/Bootstrap)

---

## 🚀 Getting Started  

Follow these steps to run the project locally.  

### 1. Clone the Repository  
If you don’t have the project yet:  
```bash
git clone https://github.com/your-username/stakewise.git
cd stakewise
```

If you already have it but want the latest changes:  
```bash
git pull origin main
```

---

### 2. Create & Activate a Virtual Environment  

On **Windows (PowerShell)**:
```bash
python -m venv venv
venv\Scripts\activate
```

On **macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

---

### 4. Apply Migrations (Set Up Database)  
```bash
python manage.py migrate
```

---

### 5. Create a Superuser (Admin Account)  
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.  

---

### 6. Run the Development Server  
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  

---

## 🛠️ Features  

- User registration & login  
- Secure deposits & withdrawals  
- Dashboard with bets & balances  
- Terms & Privacy page  
- Dynamic homepage with feature highlights  

---

## 📦 Tech Stack  

- **Backend:** Django 5+  
- **Frontend:** HTML, CSS (with Django templates)  
- **Database:** SQLite (default, but can be swapped for PostgreSQL/MySQL)  
- **Auth:** Django’s built-in authentication  

---

## 📝 Notes  

- Always activate your virtual environment (`venv`) before running commands.  
- If you reset the database, you’ll need to run `migrate` again and create a new superuser.  
- For production, set `DEBUG = False` in `settings.py` and configure allowed hosts.  

---

## 📄 License  
This project is for learning purposes. Modify and extend as you like!  
