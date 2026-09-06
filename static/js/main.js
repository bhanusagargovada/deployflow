// Main frontend JS for interactions and charts
document.addEventListener('DOMContentLoaded', function(){
  // Fetch chart data and render charts
  function fetchJSON(url){ return fetch(url, {credentials: 'same-origin'}).then(r=>r.json()).catch(()=>null); }

  document.querySelectorAll('[data-password-toggle]').forEach(button => {
    const targetId = button.getAttribute('data-target');
    const input = targetId ? document.getElementById(targetId) : null;
    const icon = button.querySelector('i');

    if (!input) {
      return;
    }

    button.addEventListener('click', () => {
      const showing = input.type === 'text';
      input.type = showing ? 'password' : 'text';
      button.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
      if (icon) {
        icon.className = showing ? 'bi bi-eye' : 'bi bi-eye-slash';
      }
    });
  });

  const authShell = document.querySelector('.auth-page-shell');
  if (authShell) {
    const roleCards = Array.from(document.querySelectorAll('[data-login-role]'));
    const roleCardsStage = document.getElementById('role-cards');
    const loginPanel = document.getElementById('role-login-panel');
    const loginForm = document.getElementById('role-login-form');
    const roleKeyInput = document.getElementById('role-key');
    const titleEl = document.getElementById('login-form-title');
    const descriptionEl = document.getElementById('login-form-description');
    const badgeEl = document.getElementById('login-form-badge');
    const backButton = document.getElementById('back-to-cards');
    const activeRole = authShell.getAttribute('data-active-role') || '';

    const hideCards = () => {
      if (roleCardsStage) {
        roleCardsStage.classList.add('fade-out');
        roleCardsStage.classList.add('is-hidden');
        roleCardsStage.classList.remove('is-visible');
        window.setTimeout(() => roleCardsStage.classList.remove('fade-out'), 240);
      }
    };

    const showCards = () => {
      if (roleCardsStage) {
        roleCardsStage.classList.add('fade-up-in');
        roleCardsStage.classList.remove('is-hidden');
        roleCardsStage.classList.add('is-visible');
        window.setTimeout(() => roleCardsStage.classList.remove('fade-up-in'), 320);
      }
    };

    const showPanel = () => {
      if (loginPanel) {
        loginPanel.classList.remove('is-hidden');
        loginPanel.classList.add('slide-up-in');
        loginPanel.classList.add('is-visible');
        loginPanel.setAttribute('aria-hidden', 'false');
        window.setTimeout(() => loginPanel.classList.remove('slide-up-in'), 320);
      }
    };

    const hidePanel = () => {
      if (loginPanel) {
        loginPanel.classList.add('fade-out');
        loginPanel.classList.remove('is-visible');
        loginPanel.setAttribute('aria-hidden', 'true');
        window.setTimeout(() => loginPanel.classList.remove('fade-out'), 220);
      }
    };

    const openPortal = (card) => {
      const title = card.getAttribute('data-login-title') || 'Login';
      const description = card.getAttribute('data-login-description') || '';
      const action = card.getAttribute('data-login-action') || '#';
      const role = card.getAttribute('data-login-role') || '';

      if (titleEl) titleEl.textContent = title;
      if (descriptionEl) descriptionEl.textContent = description;
      if (badgeEl) badgeEl.textContent = title.replace(' Login', '');
      if (loginForm) loginForm.setAttribute('action', action);
      if (roleKeyInput) roleKeyInput.value = role;
      if (loginPanel) loginPanel.dataset.role = role;

      hideCards();
      showPanel();
      loginPanel?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    roleCards.forEach(card => {
      card.addEventListener('click', () => openPortal(card));
    });

    backButton?.addEventListener('click', () => {
      hidePanel();
      showCards();
      if (loginForm) loginForm.reset();
      roleCardsStage?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    if (activeRole) {
      const activeCard = document.querySelector(`[data-login-role="${activeRole}"]`);
      if (activeCard) {
        openPortal(activeCard);
      }
    } else {
      hidePanel();
      showCards();
      if (loginPanel) {
        loginPanel.classList.add('is-hidden');
      }
    }
  }

  fetchJSON('/api/project_status').then(data=>{
    const ctx = document.getElementById('projectStatusChart');
    if (!ctx || !data) return;
    const labels = Object.keys(data);
    const values = Object.values(data);
    new Chart(ctx, { type: 'doughnut', data: { labels, datasets: [{ data: values, backgroundColor: ['#6c757d','#0d6efd','#198754','#ffc107'] }] } });
  });

  fetchJSON('/api/monthly_projects').then(data=>{
    const ctx = document.getElementById('monthlyProjectsChart');
    if (!ctx || !data) return;
    const labels = Object.keys(data).sort((a,b)=>a-b);
    const values = labels.map(k=>data[k]);
    new Chart(ctx, { type: 'bar', data: { labels, datasets: [{ label: 'Projects', data: values, backgroundColor: '#0d6efd' }] } });
  });

  fetchJSON('/api/task_completion').then(data=>{
    const ctx = document.getElementById('taskCompletionChart');
    if (!ctx || !data) return;
    const done = data.done || 0;
    const todo = (data.total || 0) - done;
    new Chart(ctx, { type: 'pie', data: { labels: ['Done','Pending'], datasets: [{ data: [done, todo], backgroundColor: ['#198754','#6c757d'] }] } });
  });

  fetchJSON('/api/user_productivity').then(data=>{
    const ctx = document.getElementById('userProductivityChart');
    if (!ctx || !data) return;
    const labels = data.map(d=>d.user);
    const values = data.map(d=>d.completed);
    new Chart(ctx, { type: 'line', data: { labels, datasets: [{ label: 'Completed Tasks', data: values, borderColor: '#0d6efd', fill: false }] } });
  });

  // Poll unread notifications count every 30 seconds
  function pollNotifications(){
    fetch('/notifications/api/unread_count', {credentials:'same-origin'}).then(r=>r.json()).then(j=>{
      const el = document.getElementById('notif-count');
      if (el) el.textContent = j.unread || '';
    }).catch(()=>{});
  }
  pollNotifications();
  setInterval(pollNotifications, 30000);

  // Reply toggles for comments
  document.querySelectorAll('.reply-toggle').forEach(btn=>{
    btn.addEventListener('click', e=>{
      const id = btn.getAttribute('data-comment-id');
      const form = document.getElementById('reply-form-' + id);
      if (form.style.display === 'none') form.style.display = 'block'; else form.style.display = 'none';
    });
  });

  // Theme toggle: store in localStorage
  const themeToggle = document.getElementById('theme-toggle');
  function setTheme(theme){
    const normalized = theme === 'dark' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', normalized);
    document.documentElement.setAttribute('data-bs-theme', normalized);
    if (themeToggle) {
      themeToggle.textContent = normalized === 'dark' ? 'Light Mode' : 'Dark Mode';
      themeToggle.setAttribute('aria-pressed', normalized === 'dark' ? 'true' : 'false');
    }
  }

  function getStoredTheme(){
    const stored = localStorage.getItem('theme');
    return stored === 'dark' ? 'dark' : 'light';
  }

  if (themeToggle){
    themeToggle.addEventListener('click', (e)=>{
      e.preventDefault();
      const cur = getStoredTheme();
      const next = cur === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', next);
      setTheme(next);
    });
  }
  setTheme(getStoredTheme());
});
