# 💸 Personal Expense Tracker

A full-stack Python web application to track daily expenses, categorize them, and generate beautiful visual monthly reports.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render)
![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-181717?logo=github)

---

## 🌐 Live Demo

👉 **[https://python-project-bj65.onrender.com](https://python-project-bj65.onrender.com)**

> ⚠️ Hosted on Render free tier — may take ~30 seconds to wake up on first visit.

---

## 📸 Screenshots

| Dashboard | Monthly Report |
|-----------|---------------|
| ![dashboard](screenshots/dashboard.png) | ![report](screenshots/report.png) |

---

## ✨ Features

- ➕ **Add Expenses** — Amount, 10 categories, description & date
- 📋 **Transaction List** — Filter by month, delete entries
- 📊 **Live Dashboard** — Total spent, monthly totals, transaction count & top category
- 🥧 **Category Breakdown** — Animated progress bars with ₹ totals
- 📈 **Visual Monthly Report** — 4-panel chart (pie, bar, trend line, summary)
- ☁️ **Cloud Deployed** — Live on Render with GitHub auto-deploy

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Backend | Flask 3.0 |
| Data Analysis | Pandas 2.1 |
| Charts (Server) | Matplotlib + Seaborn |
| Charts (Browser) | Chart.js 4.4 |
| Frontend | HTML5 + CSS3 + JavaScript |
| Server | Gunicorn |
| Deployment | Render |
| Version Control | GitHub |

---

## 📁 Project Structure

```
Python_Project/
├── app.py                  # Flask backend & REST API
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── .gitignore             # Files to exclude from Git
├── expenses.json          # Data storage (auto-created)
└── static/
    └── index.html         # Frontend UI
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Mayuriwadibhasme/Python_Project.git
cd Python_Project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve frontend |
| GET | `/api/expenses` | Get all expenses |
| POST | `/api/expenses` | Add new expense |
| DELETE | `/api/expenses/<id>` | Delete expense |
| GET | `/api/summary` | Get category summary |
| GET | `/api/report?month=YYYY-MM` | Generate visual report |
| GET | `/api/categories` | Get category list |

---

## 📦 Expense Categories

`Food & Dining` · `Transport` · `Housing & Utilities` · `Health & Medical` · `Shopping` · `Entertainment` · `Education` · `Travel` · `Personal Care` · `Others`

---

## ☁️ Deployment (Render)

1. Push code to GitHub
2. Connect repo on [render.com](https://render.com)
3. Set **Start Command**: `gunicorn app:app`
4. Render auto-deploys on every `git push` ✅

---

## 👩‍💻 Author

**Mayuri Wadibhasme**
- USN: CS24154
- Department of Computer Science & Engineering
- S.B. Jain Institute of Technology, Management & Research, Nagpur
- Guided by: **Mr. Yogesh Katre**

---

## 📄 License

This project is developed for academic purposes as part of **Python Programming Post-Lab (N-SECCS401P)**, 4th Semester B.Tech, 2025-2026.