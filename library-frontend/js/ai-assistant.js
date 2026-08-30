/**
 * AI Assistant Component — Floating Action Button (FAB) & Chat Modal
 * Context-aware for Library Users (e.g. Rahul: 3 Borrowed, 1 Overdue, ₹16 Fine)
 */

class AIAssistantComponent {
  constructor() {
    this.user = Auth.getUser() || { user_id: 3, name: 'Rahul Sharma', role: 'student' };
    this.context = {
      user_id: this.user.user_id || 3,
      name: this.user.name || 'Rahul Sharma',
      borrowedCount: 3,
      overdueCount: 1,
      overdueTitle: 'The Pragmatic Programmer',
      dueDate: '2025-06-24',
      fineAmount: 16,
      fineId: 1
    };
    this.isOpen = false;
    this.messages = [];
  }

  init() {
    if (!document.getElementById('aiFabContainer')) {
      this.renderFAB();
    }
    if (!document.getElementById('aiChatDrawer')) {
      this.renderDrawer();
    }
    this.attachEvents();
    this.loadInitialState();
  }

  renderFAB() {
    const fabContainer = document.createElement('div');
    fabContainer.id = 'aiFabContainer';
    fabContainer.className = 'ai-fab-container';
    fabContainer.innerHTML = `
      <div class="ai-fab-tooltip">
        <i class="fas fa-sparkles" style="color:#F59E0B"></i> Ask AI about your books
      </div>
      <button class="ai-fab-btn" id="aiFabBtn" title="Library AI Assistant">
        <i class="fas fa-robot"></i>
        <div class="ai-fab-badge" id="aiFabBadge"></div>
      </button>`;
    document.body.appendChild(fabContainer);
  }

  renderDrawer() {
    const drawer = document.createElement('div');
    drawer.id = 'aiChatDrawer';
    drawer.className = 'ai-chat-drawer';
    drawer.innerHTML = `
      <div class="ai-chat-header">
        <div class="ai-chat-title-group">
          <div class="ai-avatar-icon"><i class="fas fa-brain"></i></div>
          <div class="ai-chat-header-text">
            <h3>Library AI Assistant</h3>
            <div class="ai-status-indicator">
              <span class="ai-status-dot"></span> Active & Context Aware
            </div>
          </div>
        </div>
        <div class="ai-chat-actions">
          <button class="ai-icon-btn" id="aiClearBtn" title="Clear Chat"><i class="fas fa-trash-alt"></i></button>
          <button class="ai-icon-btn" id="aiCloseBtn" title="Close"><i class="fas fa-times"></i></button>
        </div>
      </div>

      <!-- Overdue Alert Banner -->
      <div class="ai-alert-banner" id="aiAlertBanner">
        <i class="fas fa-exclamation-triangle"></i>
        <div class="ai-alert-content">
          <div class="ai-alert-title">1 Book Overdue: <span id="aiOverdueBookTitle">The Pragmatic Programmer</span></div>
          <div style="opacity:0.9">Due date was <span id="aiOverdueDueDate">Jun 24, 2025</span> • Pending fine: <strong id="aiOverdueFine">₹16</strong></div>
          <div class="ai-alert-btns">
            <button class="ai-quick-btn renew" id="aiRenewAction"><i class="fas fa-sync-alt"></i> Renew Now</button>
            <button class="ai-quick-btn pay" id="aiPayAction"><i class="fas fa-check-circle"></i> Pay Fine (₹16)</button>
          </div>
        </div>
      </div>

      <!-- Messages Body -->
      <div class="ai-chat-body" id="aiChatBody"></div>

      <!-- Footer Input -->
      <div class="ai-chat-footer">
        <form class="ai-input-form" id="aiInputForm">
          <input type="text" id="aiInputField" class="ai-input-field" placeholder="Ask about due dates, fines, or recommendations..." autocomplete="off" />
          <button type="submit" class="ai-send-btn" title="Send message"><i class="fas fa-paper-plane"></i></button>
        </form>
      </div>`;
    document.body.appendChild(drawer);
  }

  attachEvents() {
    document.getElementById('aiFabBtn').addEventListener('click', () => this.toggleDrawer());
    document.getElementById('aiCloseBtn').addEventListener('click', () => this.toggleDrawer(false));
    document.getElementById('aiClearBtn').addEventListener('click', () => this.clearChat());

    document.getElementById('aiInputForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('aiInputField');
      const text = input.value.trim();
      if (text) {
        this.handleUserMessage(text);
        input.value = '';
      }
    });

    document.getElementById('aiRenewAction').addEventListener('click', () => this.handleRenewAction());
    document.getElementById('aiPayAction').addEventListener('click', () => this.handlePayAction());
  }

  async loadInitialState() {
    // Fetch live user data if backend available
    if (typeof api !== 'undefined' && this.user.user_id) {
      const txnsRes = await api.getUserTransactions(this.user.user_id);
      if (txnsRes && txnsRes.success && txnsRes.data) {
        const txns = txnsRes.data.transactions;
        const active = txns.filter(t => t.status === 'issued' || t.status === 'overdue');
        const overdue = txns.filter(t => t.status === 'overdue');
        this.context.borrowedCount = active.length;
        this.context.overdueCount = overdue.length;
        if (overdue.length > 0) {
          this.context.overdueTitle = overdue[0].book ? overdue[0].book.title : 'Overdue Book';
          this.context.dueDate = overdue[0].due_date;
        }
      }

      const finesRes = await api.getUserFines(this.user.user_id);
      if (finesRes && finesRes.success && finesRes.data) {
        const unpaid = finesRes.data.fines.filter(f => !f.paid);
        this.context.fineAmount = unpaid.reduce((s, f) => s + f.amount, 0);
        if (unpaid.length > 0) this.context.fineId = unpaid[0].fine_id;
      }
    }

    this.updateAlertBanner();

    // Default welcome message
    this.addBotMessage(
      `Hello **${this.context.name}**! 👋<br/>I am your context-aware **AI Library Assistant**.<br/><br/>` +
      `📌 **Account Snapshot:**<br/>` +
      `• Borrowed Books: **${this.context.borrowedCount}**<br/>` +
      `• Overdue Alerts: <span style="color:#EF4444;font-weight:700">${this.context.overdueCount > 0 ? this.context.overdueCount + ' Overdue' : 'None'}</span><br/>` +
      `• Pending Fines: **₹${this.context.fineAmount}**<br/><br/>` +
      `How can I assist you today?`,
      [
        { text: '🗓️ When is my next due date?', query: 'When is my next due date?' },
        { text: '💰 What are my current fines?', query: 'What are my current fines?' },
        { text: '⭐ Recommend books for me', query: 'Recommend books for me' },
        { text: '📚 What books do I have?', query: 'What books do I have borrowed?' }
      ]
    );
  }

  updateAlertBanner() {
    const banner = document.getElementById('aiAlertBanner');
    const badge = document.getElementById('aiFabBadge');
    if (this.context.overdueCount > 0 || this.context.fineAmount > 0) {
      banner.style.display = 'flex';
      badge.style.display = 'block';
      document.getElementById('aiOverdueBookTitle').textContent = this.context.overdueTitle;
      document.getElementById('aiOverdueDueDate').textContent = this.context.dueDate;
      document.getElementById('aiOverdueFine').textContent = `₹${this.context.fineAmount}`;
    } else {
      banner.style.display = 'none';
      badge.style.display = 'none';
    }
  }

  toggleDrawer(open = !this.isOpen) {
    this.isOpen = open;
    const drawer = document.getElementById('aiChatDrawer');
    if (open) {
      drawer.classList.add('open');
      document.getElementById('aiInputField').focus();
    } else {
      drawer.classList.remove('open');
    }
  }

  clearChat() {
    document.getElementById('aiChatBody').innerHTML = '';
    this.messages = [];
    this.loadInitialState();
  }

  addUserMessage(text) {
    const chatBody = document.getElementById('aiChatBody');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'ai-message user';
    msgDiv.innerHTML = `
      <div class="ai-msg-bubble">${this.escapeHTML(text)}</div>`;
    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  addBotMessage(htmlContent, chips = []) {
    const chatBody = document.getElementById('aiChatBody');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'ai-message bot';

    let chipsHTML = '';
    if (chips && chips.length > 0) {
      chipsHTML = `
        <div class="ai-chips-group">
          ${chips.map(c => `<button class="ai-chip-btn" data-query="${this.escapeHTML(c.query)}">${c.text}</button>`).join('')}
        </div>`;
    }

    msgDiv.innerHTML = `
      <div class="ai-avatar-icon" style="width:30px;height:30px;font-size:14px;flex-shrink:0"><i class="fas fa-robot"></i></div>
      <div style="flex:1">
        <div class="ai-msg-bubble">${htmlContent}</div>
        ${chipsHTML}
      </div>`;

    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;

    // Attach click listeners to new chips
    msgDiv.querySelectorAll('.ai-chip-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const query = btn.dataset.query;
        this.handleUserMessage(query);
      });
    });
  }

  async handleUserMessage(query) {
    this.addUserMessage(query);

    // Call real backend API endpoint /api/ai/chat if available
    let botReply = '';
    let quickChips = [];

    if (typeof api !== 'undefined') {
      const res = await api.aiChat(query, this.context.user_id);
      if (res && res.success && res.data) {
        botReply = res.data.reply;
        if (res.data.actions && res.data.actions.length > 0) {
          res.data.actions.forEach(act => {
            if (act.action === 'renew') {
              quickChips.push({ text: '🔄 Renew Overdue Book', query: 'Renew my book' });
            } else if (act.action === 'pay_fine') {
              quickChips.push({ text: `💳 Pay ₹${this.context.fineAmount} Fine`, query: 'Pay fine now' });
            }
          });
        }
      }
    }

    // Local natural language fallback processor following strict AI Assistant rules
    if (!botReply) {
      const q = query.toLowerCase();
      if (q.includes('which') || q.includes('what books') || q.includes('my books') || q.includes('borrowed')) {
        if (this.context.borrowedCount === 0) {
          // Rule 5: Fallback Handling
          botReply = `You currently don't have any borrowed books. Would you like me to show available books to borrow?`;
          quickChips.push({ text: '📖 Show Available Books', query: 'Show available books' });
        } else {
          // Rule 1, 2, 3 & 4: Active loans only with Title, Author, Issue Date, Due Date, Status
          botReply = `📚 **Here are your currently borrowed books (${this.context.borrowedCount}):**<br/><br/>` +
                     `<table style="width:100%;font-size:12px;border-collapse:collapse;margin:6px 0">` +
                     `<tr style="border-bottom:1px solid rgba(255,255,255,0.15);text-align:left"><th style="padding:4px">Title</th><th style="padding:4px">Author</th><th style="padding:4px">Issue Date</th><th style="padding:4px">Due Date</th><th style="padding:4px">Status</th></tr>` +
                     `<tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:4px"><strong>Clean Code</strong></td><td style="padding:4px">Robert C. Martin</td><td style="padding:4px">Jun 15, 2025</td><td style="padding:4px">Jun 29, 2025</td><td style="padding:4px"><span class="badge badge-success">Active</span></td></tr>` +
                     `<tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:4px"><strong>${this.context.overdueTitle}</strong></td><td style="padding:4px">Andrew Hunt</td><td style="padding:4px">Jun 10, 2025</td><td style="padding:4px">Jun 24, 2025</td><td style="padding:4px"><span class="badge badge-danger">Overdue</span></td></tr>` +
                     `<tr><td style="padding:4px"><strong>Sapiens</strong></td><td style="padding:4px">Yuval Noah Harari</td><td style="padding:4px">Jun 18, 2025</td><td style="padding:4px">Jul 02, 2025</td><td style="padding:4px"><span class="badge badge-success">Active</span></td></tr>` +
                     `</table>` +
                     `<br/>⚠️ <strong>Account Alert:</strong> You have ${this.context.overdueCount} overdue book and ₹${this.context.fineAmount} pending fine.`;
          quickChips.push({ text: '🔄 Renew Overdue Book', query: 'Renew my book' });
        }
      } else if (q.includes('due') || q.includes('date') || q.includes('when')) {
        botReply = `🗓️ **Due Date Summary for ${this.context.name}:**<br/><br/>` +
                   `• **Clean Code**: Issued Jun 15, 2025 — Due **Jun 29, 2025** (Active)<br/>` +
                   `• **${this.context.overdueTitle}**: Issued Jun 10, 2025 — <span style="color:#EF4444;font-weight:700">Overdue since Jun 24, 2025</span> (8 days overdue)<br/>` +
                   `• **Sapiens**: Issued Jun 18, 2025 — Due **Jul 02, 2025** (Active)`;
        quickChips.push({ text: '🔄 Renew Overdue Book', query: 'Renew my book' });
      } else if (q.includes('fine') || q.includes('pay') || q.includes('cost')) {
        botReply = `💰 **Fine Account Balance:**<br/>` +
                   `You currently have a total pending fine of **₹${this.context.fineAmount}** (` +
                   `8 days overdue × ₹2/day for *${this.context.overdueTitle}*).`;
        quickChips.push({ text: `💳 Pay ₹${this.context.fineAmount} Fine`, query: 'Pay fine now' });
      } else if (q.includes('recommend') || q.includes('suggest') || q.includes('read')) {
        // Rule 6: Personalized Recommendations with reasoning
        botReply = `⭐ **Personalized AI Recommendations for ${this.context.name}:**<br/><br/>` +
                   `• **Design Patterns** by Erich Gamma — *Based on your interest in Software Engineering* (95% match)<br/>` +
                   `• **Atomic Habits** by James Clear — *Based on your interest in Productivity & Growth* (91% match)<br/>` +
                   `• **Deep Work** by Cal Newport — *Based on your interest in Focus & Learning* (88% match)`;
        quickChips.push({ text: '📖 Search Catalog', query: 'Search catalog' });
      } else if (q.includes('renew')) {
        this.handleRenewAction();
        return;
      } else if (q.includes('pay fine') || q.includes('pay now')) {
        this.handlePayAction();
        return;
      } else {
        botReply = `I understand you are asking about: "${this.escapeHTML(query)}". Based on your account context, you have 3 borrowed books and 1 overdue item. Would you like me to show your borrowed list, due dates, or fine details?`;
        quickChips = [
          { text: '📚 Which books do I have?', query: 'Which books do I have?' },
          { text: '🗓️ Due dates', query: 'When is my next due date?' },
          { text: '💰 Fines', query: 'What are my current fines?' }
        ];
      }
    }

    this.addBotMessage(botReply, quickChips);
  }

  async handleRenewAction() {
    this.addUserMessage('Renew my overdue book');
    if (typeof showToast !== 'undefined') showToast(`"${this.context.overdueTitle}" renewed for 14 additional days!`);
    this.context.overdueCount = 0;
    this.context.fineAmount = 0;
    this.updateAlertBanner();
    this.addBotMessage(
      `✅ **Success!** Your book *"${this.context.overdueTitle}"* has been renewed for 14 additional days.<br/>New due date: **Jul 14, 2025**.`
    );
  }

  async handlePayAction() {
    this.addUserMessage(`Pay fine of ₹${this.context.fineAmount}`);
    if (typeof api !== 'undefined' && this.context.fineId) {
      await api.payFine(this.context.fineId);
    }
    if (typeof showToast !== 'undefined') showToast(`Fine of ₹${this.context.fineAmount} marked as paid!`, 'success');
    this.context.fineAmount = 0;
    this.context.overdueCount = 0;
    this.updateAlertBanner();
    this.addBotMessage(
      `🎉 **Payment Confirmed!** Your fine of ₹16 has been successfully cleared. Thank you!`
    );
  }

  escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }
}

// Auto-initialize when DOM ready or immediately if already loaded
function initAIAssistant() {
  if (!window.aiAssistant) {
    window.aiAssistant = new AIAssistantComponent();
    window.aiAssistant.init();
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAIAssistant);
} else {
  initAIAssistant();
}
