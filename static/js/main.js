// Main frontend JS for interactions and charts
document.addEventListener('DOMContentLoaded', function(){
  // Fetch chart data and render charts
  function fetchJSON(url){ return fetch(url, {credentials: 'same-origin'}).then(r=>r.json()).catch(()=>null); }

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
  function applyTheme(t){
    if (t === 'dark') document.body.classList.add('bg-dark','text-light'); else document.body.classList.remove('bg-dark','text-light');
  }
  if (themeToggle){
    themeToggle.addEventListener('click', ()=>{
      const cur = localStorage.getItem('theme') || 'light';
      const next = cur === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', next);
      applyTheme(next);
    });
  }
  applyTheme(localStorage.getItem('theme') || 'light');
});
