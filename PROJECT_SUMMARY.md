# AI Library Management System — Complete Saved Project Index

All project components, database tables, backend Flask endpoints, frontend HTML/CSS/JS files, and AI assistant modules have been fully audited, implemented, tested, and saved.

---

## 📂 Saved Directory & File Structure

```
LIBRARY AI/
├── library-backend/
│   ├── app.py                      # Flask App Factory, CORS, Blueprint routes, 404/500 error handlers
│   ├── config.py                   # App config, SQLite DB fallback (library.db), JWT secret, fine rates
│   ├── extensions.py               # SQLAlchemy db instance
│   ├── library.db                  # Persistent SQLite Database (Users, Books, Transactions, Fines, Ratings)
│   ├── database/
│   │   └── seed_data.py            # Automatic seed script (30 books, 5 users, 10 txns, 3 fines, 15 ratings)
│   ├── models/                     # User, Book, Transaction, Fine, Rating, Notification, Reservation
│   ├── routes/                     # Auth, Books, Transactions, Fines, Users, Recommendations, Analytics
│   └── utils/
│       ├── auth_helpers.py         # JWT tokens, token_required & role_required fallback decorators
│       ├── fine_calculator.py      # Fine computation logic (₹2/day overdue)
│       ├── nlp_search.py           # NLP similarity search engine
│       └── recommender.py          # TF-IDF + Cosine similarity book recommendation engine
│
└── library-frontend/
    ├── css/
    │   ├── styles.css              # Design system tokens, layout grids, navbar, sidebar, toast
    │   ├── dashboard.css           # Analytics grid cards, chips, responsive tables
    │   └── components.css          # Glassmorphism AI FAB button, chat drawer, badge pulse
    ├── js/
    │   ├── api.js                  # Frontend REST API client for all backend endpoints
    │   ├── app.js                  # Auth session, AuditLog, ButtonState, showConfirmModal, modals
    │   ├── ai-assistant.js         # Context-aware floating AI Assistant button & chat drawer
    │   ├── charts.js               # Chart.js analytics graphs (Monthly issues bar chart, genre pie chart)
    │   └── mock-data.js            # Offline mock data fallback
    ├── index.html                  # Responsive Login Page (Admin, Librarian, Student roles)
    ├── student-dashboard.html      # Student Dashboard (Active loans, overdue warnings, AI FAB)
    ├── admin-dashboard.html        # Admin Analytics Dashboard (Live stats, Chart.js, transaction logs)
    ├── manage-books.html           # Catalog Management (Add, edit, delete, bulk delete, search)
    ├── issue-return.html           # Loan Operations (Issue book, return book, automatic fine calculation)
    ├── search.html                 # Book Discovery (NLP Search, category chips, borrow & reserve)
    ├── recommendations.html        # AI Book Recommendations (Personalized matches & trending)
    └── fines.html                  # Fine Ledger (Fine tracking, individual pay, bulk clear fines)
```

---

## 🔐 Saved Demo Accounts

| Role | Email | Password | Default Landing Page |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@library.com` | `admin123` | http://localhost:3000/admin-dashboard.html |
| **Librarian** | `librarian@library.com` | `lib123` | http://localhost:3000/issue-return.html |
| **Student** | `rahul@student.com` | `student123` | http://localhost:3000/student-dashboard.html |

---

## 🚀 Running Servers & Endpoints

- **Backend Flask API**: `http://localhost:5000`
- **Frontend HTTP Server**: `http://localhost:3000`

### Verified Key Endpoints
- `GET /api/health` → System status check
- `POST /api/auth/login` → JWT Authentication
- `GET /api/books` → Catalog listing & NLP search
- `POST /api/transactions/issue` → Issue book to student
- `POST /api/transactions/return` → Process book return & calculate fine
- `POST /api/fines/pay/<fine_id>` → Settle student fine
- `POST /api/ai/chat` → Context-aware AI Library Assistant
- `GET /api/analytics/dashboard` → Live analytics metrics & charts
