
(() => {
  // Elements
  const input1 = document.getElementById('input1');
  const input2 = document.getElementById('input2');
  const searchBtn = document.getElementById('searchBtn');
  const generateBtn = document.getElementById('generateBtn');
  const profileArea = document.getElementById('profileArea');
  const status = document.getElementById('status');
  const compareToggle = document.getElementById('compareToggle');
  const reposList = document.getElementById('reposList');
  const settingsBtn = document.getElementById('settingsBtn');
  const settingsModal = document.getElementById('settingsModal');
  const tokenInput = document.getElementById('tokenInput');
  const saveSettings = document.getElementById('saveSettings');
  const closeSettings = document.getElementById('closeSettings');

  // Chart contexts
  const langCtx = document.getElementById('langChart').getContext('2d');
  const starsCtx = document.getElementById('starsChart').getContext('2d');

  // Templates
  const userCardT = document.getElementById('userCardT');

  // State
  let token = sessionStorage.getItem('gd_token') || '';
  if (token) tokenInput.value = token;

  // Chart instances
  let langChart = null;
  let starsChart = null;

  async function ghFetch(url) {
    const headers = token ? { Authorization: `token ${token}` } : {};
    const res = await fetch(url, { headers });
    if (!res.ok) {
      const text = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(text.message || 'GitHub API error');
    }
    return res.json();
  }

  // Fetch user + repos
  async function fetchUserAndRepos(username) {
    const [user, repos] = await Promise.all([
      ghFetch(`https://api.github.com/users/${encodeURIComponent(username)}`),
      ghFetch(`https://api.github.com/users/${encodeURIComponent(username)}/repos?per_page=100&type=owner&sort=updated`)
    ]);
    return { user, repos };
  }

  // Compute language breakdown
  function computeLanguages(repos) {
    const map = {};
    repos.forEach(r => {
      if (!r.language) return;
      map[r.language] = (map[r.language] || 0) + 1;
    });
    const labels = Object.keys(map);
    const values = labels.map(l => map[l]);
    return { labels, values, raw: map };
  }

  // Compute top repos by stars
  function computeTopRepos(repos, n = 6) {
    const sorted = [...repos].sort((a,b) => b.stargazers_count - a.stargazers_count);
    return sorted.slice(0,n);
  }

  // UI: create user card
  function makeUserCard(data) {
    const clone = userCardT.content.firstElementChild.cloneNode(true);
    const img = clone.querySelector('.avatar');
    const nameEl = clone.querySelector('.name');
    const usernameEl = clone.querySelector('.username');
    const bio = clone.querySelector('.bio');
    const reposCount = clone.querySelector('.reposCount');
    const followersCount = clone.querySelector('.followersCount');
    const followingCount = clone.querySelector('.followingCount');
    const locationEl = clone.querySelector('.location');
    const website = clone.querySelector('.website');
    const starsCount = clone.querySelector('.starsCount');

    img.src = data.user.avatar_url;
    nameEl.textContent = data.user.name || data.user.login;
    usernameEl.textContent = '@' + data.user.login;
    usernameEl.href = data.user.html_url;
    bio.textContent = data.user.bio || '';
    reposCount.textContent = data.user.public_repos;
    followersCount.textContent = data.user.followers;
    followingCount.textContent = data.user.following;

    const totalStars = data.repos.reduce((s, r) => s + (r.stargazers_count || 0), 0);
    starsCount.textContent = totalStars;

    locationEl.textContent = data.user.location || '';
    website.textContent = data.user.blog || '';
    website.href = data.user.blog || '#';

    return clone;
  }

  // Render charts
  function renderLanguageChart(labels, values) {
    if (langChart) langChart.destroy();
    langChart = new Chart(langCtx, {
      type: 'pie',
      data: {
        labels,
        datasets: [{
          data: values,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
      }
    });
  }

  function renderStarsChart(repoNames, starCounts) {
    if (starsChart) starsChart.destroy();
    starsChart = new Chart(starsCtx, {
      type: 'bar',
      data: {
        labels: repoNames,
        datasets: [{
          label: 'Stars',
          data: starCounts
        }]
      },
      options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } } }
    });
  }

  // Display top repos list
  function showTopRepos(repos) {
    reposList.innerHTML = '';
    repos.forEach(r => {
      const el = document.createElement('div');
      el.className = 'repo';
      el.innerHTML = `<h4><a href="${r.html_url}" target="_blank" rel="noopener noreferrer">${r.name}</a></h4>
        <p class="muted">${r.description || ''}</p>
        <p class="muted">⭐ ${r.stargazers_count} • Forks: ${r.forks_count} • ${r.language || '—'}</p>`;
      reposList.appendChild(el);
    });
  }

  // Build combined analytics for display
  function combineAnalytics(usersData) {
    if (usersData.length === 0) return;

    if (usersData.length === 1) {
      const { repos } = usersData[0];
      const lang = computeLanguages(repos);
      renderLanguageChart(lang.labels, lang.values);

      const top = computeTopRepos(repos);
      showTopRepos(top);
      renderStarsChart(top.map(r => r.name), top.map(r => r.stargazers_count));

    } else {
      const combinedMap = {};
      usersData.forEach(d => {
        const lmap = computeLanguages(d.repos).raw;
        Object.entries(lmap).forEach(([k,v]) => combinedMap[k] = (combinedMap[k]||0)+v);
      });
      const labels = Object.keys(combinedMap);
      const values = labels.map(l => combinedMap[l]);
      renderLanguageChart(labels, values);

      const allRepos = usersData.flatMap(d => d.repos.map(r => ({...r, owner: d.user.login})));
      const top = computeTopRepos(allRepos, 10);
      showTopRepos(top);
      renderStarsChart(top.map(r => `${r.owner}/${r.name}`), top.map(r => r.stargazers_count));
    }
  }

  // Main search handler
  async function handleSearch() {
    const u1 = input1.value.trim();
    const u2 = input2.value.trim();
    if (!u1) {
      status.textContent = 'Enter at least one GitHub username.';
      return;
    }
    profileArea.innerHTML = '';
    reposList.innerHTML = '';
    status.textContent = 'Loading...';

    const usernames = compareToggle.checked && u2 ? [u1, u2] : [u1];

    try {
      const results = [];
      for (const u of usernames) {
        const data = await fetchUserAndRepos(u);
        results.push({ user: data.user, repos: data.repos });
      }

      profileArea.innerHTML = '';
      results.forEach(r => {
        const card = makeUserCard(r);
        profileArea.appendChild(card);
      });

      combineAnalytics(results);

      sessionStorage.setItem('gd_last', JSON.stringify(results));
      status.textContent = 'Done.';
    } catch (err) {
      console.error(err);
      status.textContent = `Error: ${err.message}`;
    }
  }

  // Portfolio generation + footer updated to GitVerse
  function generatePortfolio() {
    const raw = sessionStorage.getItem('gd_last');
    if (!raw) {
      status.textContent = 'Search a user first to generate portfolio.';
      return;
    }
    const data = JSON.parse(raw);
    const html = buildPortfolioHTML(data);
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data[0].user.login}_portfolio.html`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    status.textContent = 'Portfolio downloaded.';
  }

  function escapeHtml(s) {
    if (!s) return '';
    return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  }

  function buildPortfolioHTML(data) {
    const primary = data[0];
    const name = escapeHtml(primary.user.name || primary.user.login);
    const login = escapeHtml(primary.user.login);
    const bio = escapeHtml(primary.user.bio || '');
    const avatar = primary.user.avatar_url;

    const repoItems = primary.repos
      .sort((a,b)=>b.stargazers_count - a.stargazers_count)
      .slice(0,8)
      .map(r => `<li><a href="${r.html_url}">${escapeHtml(r.name)}</a> — ${escapeHtml(r.description || '')} (⭐ ${r.stargazers_count})</li>`)
      .join('\n');

    const topLangs = Object.entries(computeLanguages(primary.repos).raw)
      .sort((a,b)=>b[1]-a[1])
      .slice(0,6)
      .map(t=>`<span style="display:inline-block;padding:6px;margin:4px;background:#f1f1f1;border-radius:6px">${escapeHtml(t[0])}</span>`)
      .join(' ');

    const html = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${name} — GitVerse Portfolio</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;padding:20px;color:#111;background:#fff}
.header{display:flex;gap:16px;align-items:center}
.avatar{width:96px;border-radius:12px}
h1{margin:0}
.meta{color:#555}
.repos{margin-top:18px}
.langs{margin-top:12px}
</style>
</head>
<body>
<div class="header">
  <img src="${avatar}" class="avatar" />
  <div>
    <h1>${name} <small class="meta">@${login}</small></h1>
    <p>${bio}</p>
    <p class="meta">Followers: ${primary.user.followers} • Repos: ${primary.user.public_repos}</p>
  </div>
</div>

<h3>Top Languages</h3>
<div class="langs">${topLangs}</div>

<h3>Top Repositories</h3>
<ul class="repos">${repoItems}</ul>

<footer style="margin-top:30px;color:#777">
  Portfolio generated by GitVerse.
</footer>
</body>
</html>`;
    return html;
  }

  searchBtn.addEventListener('click', handleSearch);
  generateBtn.addEventListener('click', generatePortfolio);

  [input1, input2].forEach(i => i.addEventListener('keydown', e => {
    if (e.key === 'Enter') handleSearch();
  }));

  renderLanguageChart([], []);
  renderStarsChart([], []);
})();
