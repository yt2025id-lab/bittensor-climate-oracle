// ================================================================
// AI Climate Oracle Subnet -- 3 Demo Scripts with Miner/Validator Detail
// ================================================================

const API = '';

// ===== STATE MANAGEMENT =====
function showState(state) {
    document.getElementById('stateEmpty').style.display = state === 'empty' ? 'flex' : 'none';
    document.getElementById('stateLoading').style.display = state === 'loading' ? 'flex' : 'none';
    document.getElementById('stateResult').style.display = state === 'result' ? 'block' : 'none';
}

// ===== LOADING ANIMATION =====
function animateLoading(callback) {
    showState('loading');
    const steps = document.querySelectorAll('#loaderSteps .loader-step');
    const bar = document.getElementById('loaderBarFill');
    let current = 0;

    function nextStep() {
        if (current > 0) {
            steps[current - 1].classList.remove('active');
            steps[current - 1].classList.add('done');
        }
        if (current < steps.length) {
            steps[current].classList.add('active');
            bar.style.width = ((current + 1) / steps.length * 100) + '%';
            current++;
            setTimeout(nextStep, 700 + Math.random() * 500);
        } else {
            setTimeout(callback, 400);
        }
    }

    steps.forEach(s => { s.classList.remove('active', 'done'); });
    bar.style.width = '0%';
    nextStep();
}

// ===== DEMO CARD ACTIVE STATE =====
function setActiveDemo(key) {
    document.querySelectorAll('.demo-card').forEach(c => c.classList.remove('active'));
    const btn = document.getElementById('btnDemo' + key.replace('demo', ''));
    if (btn) btn.classList.add('active');
}

// ===== RUN DEMO SCENARIO =====
function runDemo(key) {
    setActiveDemo(key);

    animateLoading(async () => {
        try {
            const res = await fetch(API + '/api/demo/' + key);
            const data = await res.json();
            renderDemoResult(data);
        } catch (err) {
            renderError(err.message);
        }
    });
}

// ===== RENDER FULL DEMO RESULT =====
function renderDemoResult(data) {
    const el = document.getElementById('stateResult');
    const syn = data.synapse;
    const cond = syn.conditions || {};

    const taskLabels = {
        short_term_forecast: 'SHORT TERM FORECAST',
        risk_index: 'RISK INDEX',
        long_range_trend: 'LONG RANGE TREND',
    };

    const taskBadgeClass = {
        short_term_forecast: 'badge-forecast',
        risk_index: 'badge-risk',
        long_range_trend: 'badge-trend',
    };

    el.innerHTML = `
        <!-- ===== TOP BAR ===== -->
        <div class="result-topbar">
            <div class="result-topbar-left">
                <span class="result-badge ${taskBadgeClass[data.task_type] || 'badge-forecast'}">${taskLabels[data.task_type] || data.task_type}</span>
                <span style="font-size:13px;color:var(--text-secondary)">${syn.location} &mdash; ${syn.forecast_horizon_days}-day forecast</span>
            </div>
            <div class="result-topbar-right">
                <span class="result-meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    ${data.timestamp ? data.timestamp.slice(11, 19) : ''}
                </span>
                <span class="result-meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    ${data.miner_nodes_consulted} miners
                </span>
                <span class="result-meta-item confidence">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                    ${data.consensus_reached ? 'Consensus Reached' : 'Disputed'}
                </span>
            </div>
        </div>

        <!-- ===== CHALLENGE INFO ===== -->
        <div class="challenge-info">
            <div class="challenge-row">
                <span class="challenge-label">Location</span><span class="challenge-value">${syn.location}</span>
            </div>
            <div class="challenge-row">
                <span class="challenge-label">Target Date</span><span class="challenge-value">${syn.target_date}</span>
            </div>
            <div class="challenge-row">
                <span class="challenge-label">Horizon</span><span class="challenge-value">${syn.forecast_horizon_days} days</span>
            </div>
            <div class="challenge-row">
                <span class="challenge-label">Season</span><span class="challenge-value">${(cond.season || 'normal').replace(/_/g, ' ')}</span>
            </div>
            <div class="challenge-row">
                <span class="challenge-label">ENSO State</span><span class="challenge-value">${(cond.enso_state || 'neutral').replace(/_/g, ' ')}</span>
            </div>
            ${cond.mjo_phase ? `
            <div class="challenge-row">
                <span class="challenge-label">MJO Phase</span><span class="challenge-value">${cond.mjo_phase.replace(/_/g, ' ')}</span>
            </div>` : ''}
            ${cond.sst_anomaly ? `
            <div class="challenge-row">
                <span class="challenge-label">SST Anomaly</span><span class="challenge-value">${cond.sst_anomaly.replace(/_/g, ' ')}</span>
            </div>` : ''}
            ${data.ground_truth ? `
            <div class="challenge-row gt">
                <span class="challenge-label">Ground Truth Temp</span><span class="challenge-value gt-val">${data.ground_truth.actual_temp_celsius}&deg;C</span>
            </div>
            <div class="challenge-row gt">
                <span class="challenge-label">Ground Truth Precip</span><span class="challenge-value gt-val">${data.ground_truth.actual_precip_mm} mm</span>
            </div>
            <div class="challenge-row gt">
                <span class="challenge-label">Ground Truth Risk</span><span class="challenge-value gt-val">${data.ground_truth.actual_risk_index}</span>
            </div>
            <div class="challenge-row gt">
                <span class="challenge-label">Extreme Event</span><span class="challenge-value gt-val">${data.ground_truth.had_extreme_event ? 'YES -- ' + (data.ground_truth.extreme_event_type || '').replace(/_/g, ' ') : 'None'}</span>
            </div>
            ` : ''}
        </div>

        <!-- ===== MINER RESPONSES ===== -->
        <div class="result-section">
            <h3 class="result-section-title">
                <span class="section-dot dot-emerald"></span>
                Miner Responses
                <span class="section-count">${data.miner_nodes_consulted} miners</span>
            </h3>
            <div class="miner-list">
                ${data.miner_responses.map((m, i) => `
                    <div class="miner-card ${i === 0 ? 'miner-top' : ''}">
                        <div class="miner-card-header">
                            <div class="miner-rank ${i === 0 ? 'top' : ''}">#${m.rank}</div>
                            <div class="miner-identity">
                                <div class="miner-name">${m.name}</div>
                                <div class="miner-hotkey">${m.hotkey}</div>
                            </div>
                            <span class="miner-tier tier-${m.tier}">${m.tier.toUpperCase()}</span>
                            <div class="miner-score-box">
                                <div class="miner-score">${m.score.toFixed(4)}</div>
                                <div class="miner-tau">${m.tao_earned ? m.tao_earned.toFixed(6) + ' T' : ''}</div>
                            </div>
                        </div>
                        <div class="miner-specialty">${m.specialty}</div>
                        <div class="miner-metrics">
                            <div class="miner-metric">
                                <span class="mm-label">Temp</span>
                                <span class="mm-value">${m.predicted_temp_celsius}&deg;C</span>
                            </div>
                            <div class="miner-metric">
                                <span class="mm-label">Precip</span>
                                <span class="mm-value">${m.predicted_precip_mm} mm</span>
                            </div>
                            <div class="miner-metric">
                                <span class="mm-label">Risk</span>
                                <span class="mm-value ${m.predicted_risk_index > 0.6 ? 'mm-red' : m.predicted_risk_index > 0.35 ? 'mm-amber' : 'mm-green'}">${Math.round(m.predicted_risk_index * 100)}%</span>
                            </div>
                            <div class="miner-metric">
                                <span class="mm-label">Confidence</span>
                                <span class="mm-value">${Math.round(m.confidence * 100)}%</span>
                            </div>
                            <div class="miner-metric">
                                <span class="mm-label">Latency</span>
                                <span class="mm-value">${m.response_time_s}s</span>
                            </div>
                        </div>
                        <div class="miner-analysis">${m.analysis}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- ===== VALIDATOR VERIFICATION ===== -->
        <div class="result-section">
            <h3 class="result-section-title">
                <span class="section-dot dot-green"></span>
                Validator Verification
                <span class="section-count">${data.validator_nodes_consulted} validators</span>
            </h3>
            <div class="validator-list">
                ${data.validator_results.map(v => `
                    <div class="validator-card">
                        <div class="validator-header">
                            <div class="validator-identity">
                                <div class="validator-name">${v.name}</div>
                                <div class="validator-hotkey">${v.hotkey}</div>
                            </div>
                            <div class="validator-stats">
                                <span class="validator-stake">${v.stake_tao.toFixed(0)} T staked</span>
                                <span class="validator-vtrust">vTrust: ${v.vtrust.toFixed(4)}</span>
                            </div>
                        </div>
                        <div class="validator-specialty">${v.specialty}</div>
                        <div class="validator-checks">
                            ${Object.entries(v.check_details).map(([label, passed]) => `
                                <div class="check-item ${passed ? 'check-pass' : 'check-fail'}">
                                    <span class="check-icon">${passed ? '&#10003;' : '&#10007;'}</span>
                                    <span>${label}</span>
                                </div>
                            `).join('')}
                        </div>
                        <div class="validator-consensus">
                            <span class="consensus-label-sm">Verdict:</span>
                            <span class="consensus-result ${v.consensus === 'Approved' ? 'approved' : 'disputed'}">${v.consensus}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- ===== CONSENSUS & REWARD ===== -->
        <div class="result-section">
            <h3 class="result-section-title">
                <span class="section-dot dot-amber"></span>
                Consensus &amp; Reward
            </h3>
            <div class="consensus-box">
                <div class="consensus-row">
                    <span class="consensus-label">Consensus</span>
                    <span class="consensus-value consensus-approved">${data.consensus_reached ? 'Reached' : 'Disputed'}</span>
                </div>
                <div class="consensus-row">
                    <span class="consensus-label">Block Number</span>
                    <span class="consensus-value mono">#${data.block_number ? data.block_number.toLocaleString() : '--'}</span>
                </div>
                <div class="consensus-row">
                    <span class="consensus-label">Tempo</span>
                    <span class="consensus-value mono">${data.tempo || '--'}</span>
                </div>
                <div class="consensus-row">
                    <span class="consensus-label">TAO Reward Pool</span>
                    <span class="consensus-value tao-value">${data.tao_reward_pool ? data.tao_reward_pool.toFixed(4) : '0.0000'} T</span>
                </div>
                <div class="consensus-row">
                    <span class="consensus-label">Subnet Version</span>
                    <span class="consensus-value mono">${data.subnet_version || 'v1.0.0-beta'}</span>
                </div>
            </div>
        </div>

        <!-- ===== FOOTER ===== -->
        <div class="result-footer">
            <span class="result-footer-text">${data.timestamp || ''}</span>
            <button class="btn-new" onclick="resetUI()">+ New Query</button>
        </div>
    `;
    showState('result');
}

// ===== ERROR =====
function renderError(message) {
    const el = document.getElementById('stateResult');
    el.innerHTML = `
        <div class="result-topbar">
            <div class="result-topbar-left">
                <span class="result-badge" style="background:rgba(239,68,68,.15);color:#F87171;border:1px solid rgba(239,68,68,.3)">ERROR</span>
            </div>
        </div>
        <div style="padding:20px;text-align:center;color:var(--text-muted)">
            <p style="margin-bottom:12px">${message}</p>
            <p>Make sure the API server is running: <code style="color:var(--green-300)">uvicorn main:app --reload</code></p>
        </div>
        <div class="result-footer">
            <span class="result-footer-text"></span>
            <button class="btn-new" onclick="resetUI()">+ Try Again</button>
        </div>
    `;
    showState('result');
}

function resetUI() {
    showState('empty');
    document.querySelectorAll('.demo-card').forEach(c => c.classList.remove('active'));
}
