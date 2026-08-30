const BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:5000/api'
  : '/api';

const api = {
  _token() {
    const u = localStorage.getItem('lms_user');
    return u ? JSON.parse(u).token || null : null;
  },

  _headers(extra = {}) {
    const h = { 'Content-Type': 'application/json', ...extra };
    const t = this._token();
    if (t) h['Authorization'] = `Bearer ${t}`;
    return h;
  },

  async get(endpoint) {
    try {
      const res = await fetch(`${BASE}${endpoint}`, { headers: this._headers() });
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  },

  async post(endpoint, body) {
    try {
      const res = await fetch(`${BASE}${endpoint}`, {
        method: 'POST',
        headers: this._headers(),
        body: JSON.stringify(body),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  },

  async put(endpoint, body) {
    try {
      const res = await fetch(`${BASE}${endpoint}`, {
        method: 'PUT',
        headers: this._headers(),
        body: JSON.stringify(body),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  },

  async del(endpoint) {
    try {
      const res = await fetch(`${BASE}${endpoint}`, {
        method: 'DELETE',
        headers: this._headers(),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  },

  // Health
  async health() { return this.get('/health'); },

  // Books
  async getBooks(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.get(`/books${query ? '?' + query : ''}`);
  },
  async searchBooks(q) { return this.get(`/books/search?q=${encodeURIComponent(q)}`); },
  async getBook(id) { return this.get(`/books/${id}`); },
  async addBook(data) { return this.post('/books', data); },
  async updateBook(id, data) { return this.put(`/books/${id}`, data); },
  async deleteBook(id) { return this.del(`/books/${id}`); },

  // Transactions
  async issueBook(userId, bookId) { return this.post('/transactions/issue', { user_id: userId, book_id: bookId }); },
  async returnBook(transactionId) { return this.post('/transactions/return', { transaction_id: transactionId }); },
  async getTransactions() { return this.get('/transactions'); },
  async getUserTransactions(userId) { return this.get(`/transactions/user/${userId}`); },

  // Fines
  async getFines() { return this.get('/fines'); },
  async getUserFines(userId) { return this.get(`/fines/user/${userId}`); },
  async payFine(fineId) { return this.post(`/fines/pay/${fineId}`, {}); },
  async getFineSummary() { return this.get('/fines/summary'); },

  // Users
  async getUsers(role = null) { return this.get(`/users${role ? '?role=' + role : ''}`); },
  async getUser(id) { return this.get(`/users/${id}`); },
  async createUser(data) { return this.post('/users', data); },
  async updateUser(id, data) { return this.put(`/users/${id}`, data); },

  // Reservations
  async reserveBook(bookId, userId = null) { return this.post('/reservations', { book_id: bookId, user_id: userId }); },
  async getUserReservations(userId) { return this.get(`/reservations/user/${userId}`); },

  // AI & Recommendations
  async getRecommendations(userId) { return this.get(`/ai/recommendations/${userId}`); },
  async getTrending() { return this.get('/ai/trending'); },
  async getSimilar(bookId) { return this.get(`/ai/similar/${bookId}`); },
  async getDemandForecast() { return this.get('/ai/demand-forecast'); },
  async aiChat(message, userId = 3) { return this.post('/ai/chat', { message, user_id: userId }); },

  // Analytics
  async getDashboardAnalytics() { return this.get('/analytics/dashboard'); },
  async getMonthlyIssues() { return this.get('/analytics/monthly-issues'); },
  async getGenreDistribution() { return this.get('/analytics/genre-distribution'); },
  async getTopBooks() { return this.get('/analytics/top-books'); },

  // Notifications
  async getNotifications(userId) { return this.get(`/notifications/${userId}`); },
  async markNotificationRead(id) { return this.put(`/notifications/${id}/read`, {}); },
  async markAllNotificationsRead(userId) { return this.put(`/notifications/read-all/${userId}`, {}); },
};
