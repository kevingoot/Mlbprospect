async function fetchSummary() {
  try {
    const res = await fetch('/api/summary');
    const data = await res.json();
    document.getElementById('s-strongbuy').textContent = data.strong_buys;
    document.getElementById('s-buyhold').textContent = data.buy_holds;
    document.getElementById('s-hold').textContent = data.holds;
    document.getElementById('s-avoid').textContent = data.avoids;
    document.getElementById('s-risk').textContent = data.avg_risk;
    document.getElementById('s-top').textContent = data.top_prospect + ' (' + data.top_score + ')';
  } catch (e) {
    console.error('Summary fetch failed', e);
  }
}

function scoreClass(score) {
  if (score >= 80) return 'score-high';
  if (score >= 60) return 'score-good';
  if (score >= 40) return 'score-mid';
  return 'score-low';
}

function riskClass(score) {
  if (score <= 35) return 'risk-low';
  if (score <= 60) return 'risk-mid';
  return 'risk-high';
}

function trendClass(trend) {
  if (trend === 'Rising') return 'trend-rising';
  if (trend === 'Declining') return 'trend-declining';
  return 'trend-stable';
}

function trendLabel(trend) {
  if (trend === 'Rising') return '🔥 Rising';
  if (trend === 'Declining') return '📉 Declining';
  return '➡️ Stable';
}

function jumpClass(jump) {
  const map = { 'Extreme': 'jump-extreme', 'Very High': 'jump-very-high', 'High': 'jump-high', 'Medium': 'jump-medium', 'Low': 'jump-low' };
  return map[jump] || 'jump-medium';
}

function recIcon(tag) {
  const map = { 'strong-buy': '🚀', 'buy-hold': '📈', 'hold': '🤔', 'avoid': '⚠️' };
  return map[tag] || '';
}

function recLabel(tag) {
  const map = { 'strong-buy': 'Strong Buy — High Call-up Soon', 'buy-hold': 'Buy / Hold — Watch Closely', 'hold': 'Hold — Moderate Risk', 'avoid': 'Avoid / Sell — High Risk' };
  return map[tag] || '';
}

function buildCard(p) {
  const delta = p.delta >= 0 ? '+' + p.delta.toFixed(2) : p.delta.toFixed(2);
  const risk = p.risk_score;
  const rankBadge = p.rank && p.rank < 999
    ? `<span class="badge badge-rank">#${p.rank}</span>` : '';
  const watchBadge = p.is_watch
    ? `<span class="badge badge-watch">👀 Watch</span>` : '';
  const watchReason = p.is_watch && p.call_up_reason
    ? `<div class="card-row"><span class="card-row-label">Signal</span><span class="card-row-value watch-reason">${p.call_up_reason}</span></div>` : '';

  return `
    <article class="prospect-card${p.is_watch ? ' is-watch' : ''}">
      <div class="card-header">
        <div class="player-info">
          <h3>${p.player_name}</h3>
          <div class="player-meta">
            ${rankBadge}
            <span class="badge badge-pos">${p.position}</span>
            <span class="badge badge-team">${p.team}</span>
            ${watchBadge}
          </div>
        </div>
        <div class="score-ring">
          <span class="score-number ${scoreClass(p.call_up_score)}">${p.call_up_score}</span>
          <span class="score-label">Score</span>
        </div>
      </div>

      <div class="card-body">
        <div class="card-row">
          <span class="card-row-label">Card Price</span>
          <span class="card-row-value">${p.recent_card_price}</span>
        </div>

        <div class="card-row">
          <span class="card-row-label">Upcoming Set</span>
          <span class="card-row-value">${p.upcoming_sets}</span>
        </div>

        <div class="card-row">
          <span class="card-row-label">Call-up Prob.</span>
          <span class="card-row-value">${p.call_up_probability}</span>
        </div>

        <div class="card-row">
          <span class="card-row-label">Trend (Δ ${delta})</span>
          <span class="trend-pill ${trendClass(p.trend)}">${trendLabel(p.trend)}</span>
        </div>

        <div class="card-row">
          <span class="card-row-label">Jump Potential</span>
          <span class="jump-pill ${jumpClass(p.jump_potential)}">${p.jump_potential}</span>
        </div>

        <div class="card-row">
          <span class="card-row-label">Risk Score</span>
          <div class="risk-bar-wrap">
            <span class="card-row-value">${risk}/100</span>
            <div class="risk-bar">
              <div class="risk-bar-fill ${riskClass(risk)}" style="width:${risk}%"></div>
            </div>
          </div>
        </div>
        ${watchReason}
      </div>

      <div class="rec-banner rec-${p.recommendation.tag}">
        ${recIcon(p.recommendation.tag)} ${recLabel(p.recommendation.tag)}
      </div>
    </article>
  `;
}

async function fetchProspects() {
  const search = document.getElementById('search').value.trim();
  const pos = document.getElementById('filter-pos').value;
  const jump = document.getElementById('filter-jump').value;
  const rec = document.getElementById('filter-rec').value;

  const params = new URLSearchParams();
  if (search) params.set('search', search);
  if (pos) params.set('position', pos);
  if (jump) params.set('jump', jump);
  if (rec) params.set('rec', rec);

  const grid = document.getElementById('cards-grid');
  grid.innerHTML = '<div class="loading">Loading…</div>';

  try {
    const res = await fetch('/api/prospects?' + params.toString());
    const data = await res.json();

    document.getElementById('generated-time').textContent = 'Updated: ' + data.generated;
    document.getElementById('results-count').textContent =
      data.total > 0 ? `Showing ${data.total} prospect${data.total !== 1 ? 's' : ''}` : '';

    if (data.prospects.length === 0) {
      grid.innerHTML = '<div class="empty-state">No prospects match your filters.</div>';
      return;
    }

    grid.innerHTML = data.prospects.map(buildCard).join('');
  } catch (e) {
    grid.innerHTML = '<div class="empty-state">Failed to load prospects. Please refresh.</div>';
    console.error(e);
  }
}

function resetFilters() {
  document.getElementById('search').value = '';
  document.getElementById('filter-pos').value = '';
  document.getElementById('filter-jump').value = '';
  document.getElementById('filter-rec').value = '';
  fetchProspects();
}

async function refreshPrices() {
  const body = document.getElementById('pb-body');
  const btn  = document.getElementById('pb-refresh-btn');
  body.innerHTML = '<span class="pb-loading">🔄 Refreshing all card prices...</span>';
  btn.disabled = true;

  try {
    const res  = await fetch('/api/card-prices/refresh', { method: 'POST' });
    const data = await res.json();

    if (data.success) {
      body.innerHTML = `
        <div class="pb-row ok">
          <span class="pb-row-label">Refresh Complete — ${data.timestamp}</span>
          <span class="pb-row-detail">✅ Updated ${data.updated} prospects</span>
        </div>
        ${data.prices.map(p => `
          <div class="pb-row ok">
            <span class="pb-row-label">${p.player_name}</span>
            <span class="pb-row-detail">${p.recent_card_price}</span>
          </div>`).join('')}
      `;
      // Reload prospect cards to show fresh prices
      fetchProspects();
      fetchSummary();
    }
  } catch (e) {
    body.innerHTML = '<div class="pb-row error"><span class="pb-row-detail">❌ Refresh failed: ' + e.message + '</span></div>';
  } finally {
    btn.disabled = false;
  }
}

async function runPybaseballTest() {
  const body = document.getElementById('pb-body');
  const btn  = document.getElementById('pb-run-btn');
  body.innerHTML = '<span class="pb-loading">⏳ Running tests — fetching from pybaseball...</span>';
  btn.disabled = true;

  try {
    const res  = await fetch('/api/pybaseball-test');
    const data = await res.json();

    body.innerHTML = data.results.map(r => `
      <div class="pb-row ${r.status}">
        <span class="pb-row-label">${r.label}</span>
        <span class="pb-row-detail">${r.detail}</span>
      </div>
    `).join('');
  } catch (e) {
    body.innerHTML = '<div class="pb-row error"><span class="pb-row-detail">❌ Request failed: ' + e.message + '</span></div>';
  } finally {
    btn.disabled = false;
  }
}

// Init
fetchSummary();
fetchProspects();
