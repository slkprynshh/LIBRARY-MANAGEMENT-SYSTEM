const Auth = {
  async login(email, password) {
    // Try real backend first
    try {
      const res = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (data.success && data.data) {
        const userObj = {
          ...data.data.user,
          user_id: data.data.user.user_id,
          token: data.data.token,
          name: data.data.user.name,
          email: data.data.user.email,
          role: data.data.user.role,
          department: data.data.user.department
        };
        localStorage.setItem('lms_user', JSON.stringify(userObj));
        return { success: true, role: data.data.user.role };
      }
    } catch (_) { /* backend offline — fall through to mock */ }

    // Mock fallback (works without backend)
    const mockMap = {
      'admin@library.com':     { user_id: 1, role: 'admin',     name: 'Admin User', department: 'Administration' },
      'librarian@library.com': { user_id: 2, role: 'librarian', name: 'Librarian Priya', department: 'Library Science' },
      'rahul@student.com':     { user_id: 3, role: 'student',   name: 'Rahul Sharma', department: 'Computer Science' },
      'anjali@student.com':    { user_id: 4, role: 'student',   name: 'Anjali Singh', department: 'Mathematics' },
      'vikram@student.com':    { user_id: 5, role: 'student',   name: 'Vikram Patel', department: 'Physics' },
    };
    const mock = mockMap[email.toLowerCase()];
    if (mock && password) {
      localStorage.setItem('lms_user', JSON.stringify({ email, ...mock, token: null }));
      return { success: true, role: mock.role };
    }
    return { success: false };
  },

  logout() {
    localStorage.removeItem('lms_user');
    window.location.href = 'index.html';
  },

  getUser() {
    const u = localStorage.getItem('lms_user');
    return u ? JSON.parse(u) : null;
  },

  isLoggedIn() { return !!this.getUser(); },

  requireAuth() {
    if (!this.isLoggedIn()) window.location.href = 'index.html';
  },
};

function showToast(msg, type = 'success') {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.className = 'toast';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.className = `toast show ${type}`;
  setTimeout(() => t.className = 'toast', 3500);
}

// Login form handler
function initLogin() {
  const form = document.getElementById('loginForm');
  if (!form) return;
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const email    = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    if (!email || !password) return showError('Please fill in all fields.');

    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right:8px"></i> Signing in...';

    const result = await Auth.login(email, password);
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-sign-in-alt" style="margin-right:8px"></i> Login';

    if (!result.success) return showError('Invalid credentials. Demo: admin@library.com / admin123');

    const routes = { admin: 'admin-dashboard.html', librarian: 'issue-return.html', student: 'student-dashboard.html' };
    window.location.href = routes[result.role] || 'student-dashboard.html';
  });
}

function showError(msg) {
  const el = document.getElementById('loginError');
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
  setTimeout(() => el.style.display = 'none', 4000);
}

function initNavbar() {
  const user = Auth.getUser();
  if (!user) return;
  const nameEl = document.getElementById('navUserName');
  if (nameEl) nameEl.textContent = user.name;
  const avatarEl = document.getElementById('navAvatar');
  if (avatarEl) {
    const initials = user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    avatarEl.innerHTML = `<div style="width:32px;height:32px;border-radius:50%;background:#0EA5E9;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px">${initials}</div>`;
  }
  document.querySelectorAll('.logout-btn').forEach(btn =>
    btn.addEventListener('click', Auth.logout.bind(Auth))
  );

  // Wire Notifications button
  document.querySelectorAll('.nav-icon-btn[title="Notifications"], .nav-icon-btn .fa-bell').forEach(btn => {
    const iconBtn = btn.closest('.nav-icon-btn') || btn;
    iconBtn.addEventListener('click', () => openNotificationsModal());
  });
}

function initSidebar() {
  const page = window.location.pathname.split('/').pop();
  document.querySelectorAll('.sidebar-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === page) {
      link.classList.add('active');
    }
    
    // Wire modal triggers for non-page links
    if (href === '#' || href === '#profile') {
      const text = link.textContent.trim().toLowerCase();
      if (text.includes('profile')) {
        link.addEventListener('click', e => { e.preventDefault(); openProfileModal(); });
      } else if (text.includes('users')) {
        link.addEventListener('click', e => { e.preventDefault(); openUsersModal(); });
      } else if (text.includes('reports') || text.includes('analytics')) {
        link.addEventListener('click', e => { e.preventDefault(); openReportsModal(); });
      } else if (text.includes('settings')) {
        link.addEventListener('click', e => { e.preventDefault(); openSettingsModal(); });
      }
    }
  });
}

// Universal System Modals
function openProfileModal() {
  const user = Auth.getUser() || { name: 'User', email: 'user@library.com', role: 'student', department: 'Computer Science' };
  let modal = document.getElementById('profileModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'profileModal';
    modal.className = 'modal-overlay';
    document.body.appendChild(modal);
  }
  modal.innerHTML = `
    <div class="modal">
      <div class="modal-header">
        <span class="modal-title"><i class="fas fa-user-circle" style="color:#0EA5E9;margin-right:8px"></i>My Profile</span>
        <button class="modal-close" onclick="document.getElementById('profileModal').classList.remove('open')">&times;</button>
      </div>
      <form id="profileForm">
        <div class="form-group" style="margin-bottom:14px">
          <label>Full Name</label>
          <input type="text" id="profName" class="form-control" value="${user.name || ''}" required />
        </div>
        <div class="form-group" style="margin-bottom:14px">
          <label>Email Address</label>
          <input type="email" id="profEmail" class="form-control" value="${user.email || ''}" readonly />
        </div>
        <div class="form-group" style="margin-bottom:14px">
          <label>Role</label>
          <input type="text" class="form-control" value="${user.role ? user.role.toUpperCase() : 'STUDENT'}" readonly />
        </div>
        <div class="form-group" style="margin-bottom:18px">
          <label>Department</label>
          <input type="text" id="profDept" class="form-control" value="${user.department || 'Computer Science'}" />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline" onclick="document.getElementById('profileModal').classList.remove('open')">Cancel</button>
          <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Save Changes</button>
        </div>
      </form>
    </div>`;
  modal.classList.add('open');
  document.getElementById('profileForm').addEventListener('submit', async e => {
    e.preventDefault();
    const updated = { ...user, name: document.getElementById('profName').value, department: document.getElementById('profDept').value };
    localStorage.setItem('lms_user', JSON.stringify(updated));
    if (typeof api !== 'undefined' && user.user_id) {
      await api.updateUser(user.user_id, { name: updated.name, department: updated.department });
    }
    showToast('Profile updated successfully!');
    modal.classList.remove('open');
    initNavbar();
  });
}

function openUsersModal() {
  let modal = document.getElementById('usersModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'usersModal';
    modal.className = 'modal-overlay';
    document.body.appendChild(modal);
  }
  const mockUsers = [
    { id: 1, name: 'Admin User', email: 'admin@library.com', role: 'admin', dept: 'Library Admin' },
    { id: 2, name: 'Librarian Priya', email: 'librarian@library.com', role: 'librarian', dept: 'Cataloging' },
    { id: 3, name: 'Rahul Sharma', email: 'rahul@student.com', role: 'student', dept: 'Computer Science' },
    { id: 4, name: 'Anjali Singh', email: 'anjali@student.com', role: 'student', dept: 'Mathematics' },
    { id: 5, name: 'Vikram Patel', email: 'vikram@student.com', role: 'student', dept: 'Physics' },
  ];
  modal.innerHTML = `
    <div class="modal" style="max-width:650px">
      <div class="modal-header">
        <span class="modal-title"><i class="fas fa-users" style="color:#0EA5E9;margin-right:8px"></i>Library Users</span>
        <button class="modal-close" onclick="document.getElementById('usersModal').classList.remove('open')">&times;</button>
      </div>
      <div class="table-wrap" style="max-height:350px;overflow-y:auto">
        <table>
          <thead>
            <tr><th>Name</th><th>Email</th><th>Role</th><th>Department</th></tr>
          </thead>
          <tbody>
            ${mockUsers.map(u => `
              <tr>
                <td><strong>${u.name}</strong></td>
                <td>${u.email}</td>
                <td><span class="badge ${u.role === 'admin' ? 'badge-danger' : (u.role === 'librarian' ? 'badge-warning' : 'badge-info')}">${u.role}</span></td>
                <td>${u.dept}</td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
      <div class="modal-footer" style="margin-top:16px">
        <button class="btn btn-outline" onclick="document.getElementById('usersModal').classList.remove('open')">Close</button>
      </div>
    </div>`;
  modal.classList.add('open');
}

function openNotificationsModal() {
  let modal = document.getElementById('notifModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'notifModal';
    modal.className = 'modal-overlay';
    document.body.appendChild(modal);
  }
  const notifs = [
    { title: 'Book Issued', msg: 'You have borrowed "Clean Code". Due in 14 days.', time: '2 hours ago', icon: 'fa-book' },
    { title: 'Fine Notification', msg: 'Overdue fine of ₹16 incurred on "A Brief History of Time".', time: '1 day ago', icon: 'fa-exclamation-triangle' },
    { title: 'AI Recommendation', msg: 'New match: "Design Patterns" recommended for your profile.', time: '3 days ago', icon: 'fa-robot' },
  ];
  modal.innerHTML = `
    <div class="modal" style="max-width:480px">
      <div class="modal-header">
        <span class="modal-title"><i class="fas fa-bell" style="color:#0EA5E9;margin-right:8px"></i>Notifications</span>
        <button class="modal-close" onclick="document.getElementById('notifModal').classList.remove('open')">&times;</button>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px;max-height:350px;overflow-y:auto">
        ${notifs.map(n => `
          <div style="display:flex;gap:12px;padding:12px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid #0EA5E9">
            <i class="fas ${n.icon}" style="color:#0EA5E9;font-size:18px;margin-top:2px"></i>
            <div>
              <div style="font-weight:600;font-size:13px">${n.title}</div>
              <div style="font-size:12px;color:#94A3B8;margin:2px 0">${n.msg}</div>
              <div style="font-size:11px;color:#64748B">${n.time}</div>
            </div>
          </div>`).join('')}
      </div>
      <div class="modal-footer" style="margin-top:16px">
        <button class="btn btn-primary btn-sm" style="width:100%" onclick="showToast('All notifications marked as read!');document.getElementById('notifModal').classList.remove('open')">
          Mark All as Read
        </button>
      </div>
    </div>`;
  modal.classList.add('open');
}

function openReportsModal() {
  showToast('Reports & Analytics summary loaded.', 'info');
  window.location.href = 'admin-dashboard.html';
}

function openSettingsModal() {
  let modal = document.getElementById('settingsModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'settingsModal';
    modal.className = 'modal-overlay';
    document.body.appendChild(modal);
  }
  modal.innerHTML = `
    <div class="modal" style="max-width:480px">
      <div class="modal-header">
        <span class="modal-title"><i class="fas fa-cog" style="color:#0EA5E9;margin-right:8px"></i>System Settings</span>
        <button class="modal-close" onclick="document.getElementById('settingsModal').classList.remove('open')">&times;</button>
      </div>
      <div class="form-group" style="margin-bottom:14px">
        <label>Loan Period (Days)</label>
        <input type="number" class="form-control" value="14" readonly />
      </div>
      <div class="form-group" style="margin-bottom:14px">
        <label>Fine Rate (₹ per day)</label>
        <input type="number" class="form-control" value="2" readonly />
      </div>
      <div class="form-group" style="margin-bottom:18px">
        <label>AI Recommendation Engine</label>
        <select class="form-control"><option>Enabled (Cosine Similarity + TF-IDF)</option></select>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="showToast('System settings saved!');document.getElementById('settingsModal').classList.remove('open')">Save Configuration</button>
      </div>
    </div>`;
  modal.classList.add('open');
}

// ── Audit Logging System ──
const AuditLog = {
  getLogs() {
    return JSON.parse(localStorage.getItem('lms_audit_log') || '[]');
  },
  log(action, details = {}) {
    const user = Auth.getUser() || { name: 'Guest/System', user_id: 0 };
    const logs = this.getLogs();
    const entry = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      user: user.name,
      user_id: user.user_id,
      action,
      details
    };
    logs.unshift(entry);
    localStorage.setItem('lms_audit_log', JSON.stringify(logs.slice(0, 100)));
    console.log(`[Audit Log] ${action}:`, entry);
  }
};

// ── Button State & Loading Indicator Manager ──
const ButtonState = {
  setLoading(btn, isLoading, loadingText = 'Processing...') {
    if (!btn) return;
    if (isLoading) {
      btn.dataset.origHtml = btn.innerHTML;
      btn.disabled = true;
      btn.setAttribute('aria-disabled', 'true');
      btn.innerHTML = `<i class="fas fa-spinner fa-spin" style="margin-right:8px" aria-hidden="true"></i>${loadingText}`;
    } else {
      btn.disabled = false;
      btn.removeAttribute('aria-disabled');
      if (btn.dataset.origHtml) btn.innerHTML = btn.dataset.origHtml;
    }
  },
  setDisabled(btn, isDisabled) {
    if (!btn) return;
    btn.disabled = isDisabled;
    if (isDisabled) btn.setAttribute('aria-disabled', 'true');
    else btn.removeAttribute('aria-disabled');
  }
};

// ── Universal Confirmation Modal for Destructive Actions ──
function showConfirmModal({ title = 'Confirm Action', message = 'Are you sure you want to perform this action?', confirmText = 'Confirm', confirmClass = 'btn-danger', icon = 'fa-exclamation-triangle', onConfirm }) {
  let modal = document.getElementById('confirmModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'confirmModal';
    modal.className = 'modal-overlay';
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="modal" style="max-width:440px" role="dialog" aria-modal="true" aria-labelledby="confirmTitle">
      <div class="modal-header">
        <span class="modal-title" id="confirmTitle"><i class="fas ${icon}" style="color:${confirmClass.includes('danger') ? '#EF4444' : '#0EA5E9'};margin-right:8px"></i>${title}</span>
        <button class="modal-close" id="confirmCloseBtn" aria-label="Close modal">&times;</button>
      </div>
      <div style="font-size:14px;color:#64748B;line-height:1.6;margin-bottom:20px">${message}</div>
      <div class="modal-footer">
        <button type="button" class="btn btn-outline" id="confirmCancelBtn">Cancel</button>
        <button type="button" class="btn ${confirmClass}" id="confirmActionBtn">${confirmText}</button>
      </div>
    </div>`;

  modal.classList.add('open');

  const closeModal = () => modal.classList.remove('open');
  document.getElementById('confirmCloseBtn').onclick = closeModal;
  document.getElementById('confirmCancelBtn').onclick = closeModal;

  document.getElementById('confirmActionBtn').onclick = async () => {
    const btn = document.getElementById('confirmActionBtn');
    ButtonState.setLoading(btn, true, 'Processing...');
    try {
      if (onConfirm) await onConfirm();
      AuditLog.log(`CONFIRMED: ${title}`, { message });
    } catch (err) {
      showToast(err.message || 'Action failed.', 'error');
    } finally {
      closeModal();
    }
  };
}

// Global Audit Click Tracker
document.addEventListener('click', e => {
  const btn = e.target.closest('button, .btn, a.sidebar-link, .ai-chip-btn');
  if (btn) {
    const label = btn.textContent.trim() || btn.getAttribute('title') || btn.getAttribute('aria-label') || 'Button';
    AuditLog.log('BUTTON_CLICK', { label, id: btn.id, class: btn.className });
  }
});

document.addEventListener('DOMContentLoaded', () => {
  initLogin();
  initNavbar();
  initSidebar();
});

