"""
IMDb Dashboard Generator
-------------------------
Reads imdb_movies.csv (produced by final_scraper.py) and generates
a self-contained, interactive HTML dashboard (imdb_dashboard.html)
with the data already embedded — no manual upload needed.

Run this AFTER final_scraper.py has created imdb_movies.csv.
"""

import json
import webbrowser
import pandas as pd


CSV_FILE = "imdb_movies.csv"
OUTPUT_HTML = "imdb_dashboard.html"


def load_data(csv_file):
    df = pd.read_csv(csv_file)

    # Basic cleanup
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce").fillna(0).astype(int)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
    df["year"] = df["year"].astype(str)

    return df.to_dict(orient="records")


def build_html(movies_data):
    movies_json = json.dumps(movies_data)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>IMDb Top 250 Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #f4f5f7; --card-bg: #ffffff; --text: #1a1a2e; --text-muted: #6b7280;
    --accent: #d4af37; --accent-2: #e50914; --border: #e5e7eb;
    --shadow: 0 4px 14px rgba(0,0,0,0.06); --row-hover: #fafafa;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #0f1117; --card-bg: #1a1d29; --text: #f0f0f5; --text-muted: #9ca3af;
      --accent: #f2c14e; --accent-2: #ff3344; --border: #2a2d3a;
      --shadow: 0 4px 20px rgba(0,0,0,0.4); --row-hover: #21242f;
    }
  }
  :root[data-theme="dark"] {
    --bg: #0f1117; --card-bg: #1a1d29; --text: #f0f0f5; --text-muted: #9ca3af;
    --accent: #f2c14e; --accent-2: #ff3344; --border: #2a2d3a;
    --shadow: 0 4px 20px rgba(0,0,0,0.4); --row-hover: #21242f;
  }
  * { box-sizing: border-box; }
  body { margin:0; background: var(--bg); color: var(--text); font-family:'Segoe UI',system-ui,sans-serif; padding:24px; }
  .header { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:24px; }
  h1 { font-size:clamp(1.4rem,4vw,2rem); margin:0; background:linear-gradient(90deg,var(--accent),var(--accent-2)); -webkit-background-clip:text; background-clip:text; color:transparent; font-weight:800; }
  .subtitle { color: var(--text-muted); font-size:0.9rem; margin-top:4px; }
  .stats-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:16px; margin-bottom:24px; }
  .stat-card { background: var(--card-bg); border-radius:14px; padding:18px 20px; box-shadow: var(--shadow); border:1px solid var(--border); }
  .stat-card .label { color: var(--text-muted); font-size:0.8rem; text-transform:uppercase; letter-spacing:0.05em; }
  .stat-card .value { font-size:1.8rem; font-weight:800; margin-top:4px; color: var(--accent); }
  .charts-grid { display:grid; grid-template-columns:2fr 1fr; gap:16px; margin-bottom:24px; }
  @media (max-width:800px) { .charts-grid { grid-template-columns:1fr; } }
  .chart-card { background: var(--card-bg); border-radius:14px; padding:18px; box-shadow: var(--shadow); border:1px solid var(--border); }
  .chart-card h3 { margin:0 0 12px 0; font-size:1rem; }
  .chart-wrap { position:relative; height:260px; }
  .controls { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px; }
  .controls input, .controls select { background: var(--card-bg); border:1px solid var(--border); color: var(--text); padding:10px 14px; border-radius:10px; font-size:0.9rem; }
  .controls input { flex:1; min-width:180px; }
  .table-card { background: var(--card-bg); border-radius:14px; box-shadow: var(--shadow); border:1px solid var(--border); overflow-x:auto; }
  table { width:100%; border-collapse:collapse; min-width:500px; }
  th, td { padding:12px 16px; text-align:left; border-bottom:1px solid var(--border); font-size:0.9rem; }
  th { color: var(--text-muted); text-transform:uppercase; font-size:0.72rem; letter-spacing:0.05em; cursor:pointer; user-select:none; white-space:nowrap; }
  th:hover { color: var(--accent); }
  tbody tr:hover { background: var(--row-hover); }
  .rank-badge { display:inline-block; background: var(--accent); color:#111; font-weight:700; border-radius:50%; width:28px; height:28px; line-height:28px; text-align:center; font-size:0.8rem; }
  .rating-pill { background: rgba(212,175,55,0.15); color: var(--accent); padding:3px 10px; border-radius:20px; font-weight:700; font-size:0.85rem; }
  .theme-toggle { background: var(--card-bg); border:1px solid var(--border); color: var(--text); border-radius:20px; padding:8px 16px; cursor:pointer; font-size:0.85rem; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>🎬 IMDb Top 250 Dashboard</h1>
    <div class="subtitle" id="subtitle"></div>
  </div>
  <button class="theme-toggle" onclick="toggleTheme()">🌓 Toggle Theme</button>
</div>

<div class="stats-grid">
  <div class="stat-card"><div class="label">Total Movies</div><div class="value" id="statTotal">0</div></div>
  <div class="stat-card"><div class="label">Avg Rating</div><div class="value" id="statAvg">0.0</div></div>
  <div class="stat-card"><div class="label">Top Rated</div><div class="value" id="statTop">-</div></div>
  <div class="stat-card"><div class="label">Year Range</div><div class="value" id="statYears">-</div></div>
</div>

<div class="charts-grid">
  <div class="chart-card"><h3>Movies by Decade</h3><div class="chart-wrap"><canvas id="decadeChart"></canvas></div></div>
  <div class="chart-card"><h3>Rating Distribution</h3><div class="chart-wrap"><canvas id="ratingChart"></canvas></div></div>
</div>

<div class="controls">
  <input type="text" id="searchBox" placeholder="Search by movie title..." />
  <select id="decadeFilter"><option value="">All Decades</option></select>
</div>

<div class="table-card">
  <table>
    <thead><tr>
      <th data-key="rank">Rank</th>
      <th data-key="title">Title</th>
      <th data-key="year">Year</th>
      <th data-key="rating">Rating</th>
    </tr></thead>
    <tbody id="tableBody"></tbody>
  </table>
</div>

<script>
const movies = MOVIES_JSON_PLACEHOLDER;
let sortKey = 'rank', sortAsc = true;
let decadeChartInstance = null, ratingChartInstance = null;

function getDecade(year) {
  const y = parseInt(year);
  if (isNaN(y)) return 'Unknown';
  return Math.floor(y / 10) * 10 + 's';
}

function buildDecadeFilter() {
  const decades = [...new Set(movies.map(m => getDecade(m.year)))].sort();
  document.getElementById('decadeFilter').innerHTML =
    '<option value="">All Decades</option>' + decades.map(d => `<option value="${d}">${d}</option>`).join('');
}

function renderStats() {
  const total = movies.length;
  const avgRating = total ? (movies.reduce((s, m) => s + m.rating, 0) / total).toFixed(2) : '0.0';
  const top = movies.reduce((best, m) => (m.rating > (best?.rating || 0) ? m : best), null);
  const years = movies.map(m => parseInt(m.year)).filter(y => !isNaN(y));
  const yearRange = years.length ? `${Math.min(...years)}-${Math.max(...years)}` : '-';

  document.getElementById('statTotal').textContent = total;
  document.getElementById('statAvg').textContent = avgRating;
  document.getElementById('statTop').textContent = top ? top.title.slice(0, 18) + (top.title.length > 18 ? '...' : '') : '-';
  document.getElementById('statYears').textContent = yearRange;
  document.getElementById('subtitle').textContent = `${total} movies loaded from imdb_movies.csv`;
}

function renderCharts() {
  const decadeCounts = {};
  movies.forEach(m => { const d = getDecade(m.year); decadeCounts[d] = (decadeCounts[d] || 0) + 1; });
  const decadeLabels = Object.keys(decadeCounts).sort();
  const decadeData = decadeLabels.map(d => decadeCounts[d]);

  const ratingBuckets = {'<7': 0, '7-8': 0, '8-9': 0, '9+': 0};
  movies.forEach(m => {
    if (m.rating < 7) ratingBuckets['<7']++;
    else if (m.rating < 8) ratingBuckets['7-8']++;
    else if (m.rating < 9) ratingBuckets['8-9']++;
    else ratingBuckets['9+']++;
  });

  const style = getComputedStyle(document.documentElement);
  const accent = style.getPropertyValue('--accent').trim();
  const accent2 = style.getPropertyValue('--accent-2').trim();
  const textColor = style.getPropertyValue('--text').trim();

  if (decadeChartInstance) decadeChartInstance.destroy();
  if (ratingChartInstance) ratingChartInstance.destroy();

  decadeChartInstance = new Chart(document.getElementById('decadeChart'), {
    type: 'bar',
    data: { labels: decadeLabels, datasets: [{ label: 'Movies', data: decadeData, backgroundColor: accent, borderRadius: 6 }] },
    options: { responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}},
      scales: { x: { ticks:{color:textColor}, grid:{display:false} }, y: { ticks:{color:textColor}, grid:{color:'rgba(128,128,128,0.15)'} } } }
  });

  ratingChartInstance = new Chart(document.getElementById('ratingChart'), {
    type: 'doughnut',
    data: { labels: Object.keys(ratingBuckets), datasets: [{ data: Object.values(ratingBuckets), backgroundColor:[accent2, accent, '#4ade80', '#60a5fa'] }] },
    options: { responsive:true, maintainAspectRatio:false, plugins:{legend:{position:'bottom', labels:{color:textColor}}} }
  });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function renderTable() {
  const search = document.getElementById('searchBox').value.toLowerCase();
  const decadeFilter = document.getElementById('decadeFilter').value;

  let filtered = movies.filter(m =>
    m.title.toLowerCase().includes(search) &&
    (decadeFilter === '' || getDecade(m.year) === decadeFilter)
  );

  filtered.sort((a, b) => {
    let va = a[sortKey], vb = b[sortKey];
    if (typeof va === 'string') { va = va.toLowerCase(); vb = vb.toLowerCase(); }
    if (va < vb) return sortAsc ? -1 : 1;
    if (va > vb) return sortAsc ? 1 : -1;
    return 0;
  });

  document.getElementById('tableBody').innerHTML = filtered.map(m => `
    <tr>
      <td><span class="rank-badge">${m.rank}</span></td>
      <td>${escapeHtml(m.title)}</td>
      <td>${m.year}</td>
      <td><span class="rating-pill">* ${m.rating.toFixed(1)}</span></td>
    </tr>
  `).join('') || '<tr><td colspan="4" style="text-align:center;color:var(--text-muted);padding:30px;">No movies match your search.</td></tr>';
}

document.getElementById('searchBox').addEventListener('input', renderTable);
document.getElementById('decadeFilter').addEventListener('change', renderTable);
document.querySelectorAll('th[data-key]').forEach(th => {
  th.addEventListener('click', () => {
    const key = th.getAttribute('data-key');
    if (sortKey === key) sortAsc = !sortAsc; else { sortKey = key; sortAsc = true; }
    renderTable();
  });
});

function toggleTheme() {
  const root = document.documentElement;
  const current = root.getAttribute('data-theme');
  if (current === 'dark') root.setAttribute('data-theme', 'light');
  else if (current === 'light') root.removeAttribute('data-theme');
  else root.setAttribute('data-theme', 'dark');
  renderCharts();
}

buildDecadeFilter();
renderStats();
renderCharts();
renderTable();
</script>

</body>
</html>
"""
    html = html.replace("MOVIES_JSON_PLACEHOLDER", movies_json)
    return html


def main():
    print("Reading data from", CSV_FILE, "...")
    movies_data = load_data(CSV_FILE)
    print(f"Loaded {len(movies_data)} movies.")

    html = build_html(movies_data)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard generated: {OUTPUT_HTML}")

    # Automatically open it in the default browser
    webbrowser.open(OUTPUT_HTML)S


if __name__ == "__main__":
    main()
