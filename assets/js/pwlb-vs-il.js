// PWLB vs index-linked borrowing: NPV cost comparison
// Method ported unchanged from the original Haverly Consulting tool.
(function () {
  // Live rates file, auto-updated daily from DMO PWLB Standard Rates and the
  // Bank of England index-linked gilt real yield curve.
  var RATES_URL = 'https://gist.githubusercontent.com/nhaverly/2221652235336db07f5df927d45ffad5/raw/rates.json';
  var CONTACT_EMAIL = 'info@haverlyconsulting.co.uk';
  // The gist holds DMO's unmodified PWLB Standard Rate; Certainty Rate is this many bps lower.
  var CERTAINTY_RATE_DISCOUNT_BPS = 20;
  var DISPLAY_TERMS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50];
  var RATES = null, chart = null;

  function $(id) { return document.getElementById(id); }
  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  var gbp = function (v) { return '£' + Math.round(v).toLocaleString('en-GB'); };
  var pct = function (v) { return (v * 100).toFixed(2) + '%'; };

  function interp(curve, term) {
    var pts = curve.slice().sort(function (a, b) { return a.term - b.term; });
    if (term <= pts[0].term) return pts[0].rate;
    if (term >= pts[pts.length - 1].term) return pts[pts.length - 1].rate;
    for (var i = 0; i < pts.length - 1; i++) {
      if (term >= pts[i].term && term <= pts[i + 1].term) {
        var t0 = pts[i].term, t1 = pts[i + 1].term, r0 = pts[i].rate, r1 = pts[i + 1].rate;
        return r0 + (r1 - r0) * (term - t0) / (t1 - t0);
      }
    }
    return pts[pts.length - 1].rate;
  }
  function pmt(rate, nper, pv) { return rate === 0 ? pv / nper : pv * rate / (1 - Math.pow(1 + rate, -nper)); }
  function pwlbRatesByType(rates, term) {
    var d = CERTAINTY_RATE_DISCOUNT_BPS / 10000;
    return {
      annuity: interp(rates.pwlbAnnuityCurve, term) - d,
      eip: interp(rates.pwlbEipCurve, term) - d,
      maturity: interp(rates.pwlbMaturityCurve, term) - d
    };
  }
  function scheduleAnnuity(p, r, n) { var bal = p, pay = pmt(r, n, p), a = []; for (var y = 1; y <= n; y++) { var i = bal * r; bal -= (pay - i); a.push(pay); } return a; }
  function scheduleEIP(p, r, n) { var pp = p / n, bal = p, a = []; for (var y = 1; y <= n; y++) { a.push(pp + bal * r); bal -= pp; } return a; }
  function scheduleMaturity(p, r, n) { var a = []; for (var y = 1; y <= n; y++) a.push(p * r + (y === n ? p : 0)); return a; }
  function schedulePP(p, real, rpi, n) { var rp = pmt(real, n, p), a = []; for (var y = 1; y <= n; y++) a.push(rp * Math.pow(1 + rpi, y)); return a; }
  function npv(arr, r) { return arr.reduce(function (t, cf, i) { return t + cf / Math.pow(1 + r, i + 1); }, 0); }
  function total(arr) { return arr.reduce(function (a, b) { return a + b; }, 0); }

  function updateReferenceRates() {
    var term = parseFloat($('term').value) || 40;
    var r = pwlbRatesByType(RATES, term);
    $('pwlbRateDisplay').value = 'Annuity ' + pct(r.annuity) + ' · EIP ' + pct(r.eip) + ' · Maturity ' + pct(r.maturity);
    $('giltRateDisplay').value = pct(interp(RATES.giltRealCurve, term));
    $('discRate').value = (r.annuity * 100).toFixed(2);
  }

  function calculate() {
    try { calculateInner(); }
    catch (err) { $('resultGrid').innerHTML = '<p class="err-msg">Something went wrong: ' + err.message + '</p>'; console.error(err); }
  }

  function calculateInner() {
    var principal = parseFloat($('principal').value);
    var term = Math.round(parseFloat($('term').value));
    var marginBps = parseFloat($('margin').value) || 0;
    var rpi = (parseFloat($('rpi').value) || 0) / 100;
    var discRate = (parseFloat($('discRate').value) || 0) / 100;
    if (!(principal > 0) || !(term >= 1 && term <= 50)) { $('resultGrid').innerHTML = '<p class="err-msg">Enter a principal above zero and a term between 1 and 50 years.</p>'; return; }

    var pr = pwlbRatesByType(RATES, term);
    var realRate = interp(RATES.giltRealCurve, term) + marginBps / 10000;
    var options = [
      { key: 'annuity', label: 'PWLB Annuity', sub: pct(pr.annuity), cf: scheduleAnnuity(principal, pr.annuity, term), color: css('--c-annuity') },
      { key: 'eip', label: 'PWLB EIP', sub: pct(pr.eip), cf: scheduleEIP(principal, pr.eip, term), color: css('--c-eip') },
      { key: 'maturity', label: 'PWLB Maturity', sub: pct(pr.maturity), cf: scheduleMaturity(principal, pr.maturity, term), color: css('--c-maturity') },
      { key: 'pp', label: 'Index-linked private placement', sub: pct(realRate) + ' real', cf: schedulePP(principal, realRate, rpi, term), color: css('--c-pp') }
    ];
    options.forEach(function (o) { o.total = total(o.cf); o.npv = npv(o.cf, discRate); });
    var cheapest = options.reduce(function (a, b) { return a.npv < b.npv ? a : b; });

    $('resultGrid').innerHTML = options.map(function (o) {
      return '<div class="npv-card' + (o.key === cheapest.key ? ' best' : '') + '">' +
        (o.key === cheapest.key ? '<span class="badge">Lowest NPV</span>' : '') +
        '<h4><span class="sw" style="background:' + o.color + '"></span>' + o.label + '</h4>' +
        '<div class="row"><span>Rate</span><b>' + o.sub + '</b></div>' +
        '<div class="row"><span>Total nominal cost</span><b>' + gbp(o.total) + '</b></div>' +
        '<div class="row"><span>NPV cost</span></div><div class="npv">' + gbp(o.npv) + '</div></div>';
    }).join('');

    var callout = $('ctaCallout');
    if (cheapest.key === 'pp') {
      var bestPwlb = options.filter(function (o) { return o.key !== 'pp'; }).reduce(function (a, b) { return a.npv < b.npv ? a : b; });
      var saving = bestPwlb.npv - cheapest.npv, savingPct = saving / bestPwlb.npv;
      $('ctaSaving').textContent = gbp(saving) + ' (' + (savingPct * 100).toFixed(1) + '%)';
      var subject = 'Index-linked financing enquiry: ' + gbp(principal) + ' / ' + term + ' years';
      var body = ['Hi Haverly Consulting,', '', 'I ran the PWLB vs index-linked comparison with the following scenario and would like to discuss it:', '',
        'Loan principal: ' + gbp(principal), 'Term: ' + term + ' years', 'Margin over gilt yield: ' + marginBps + 'bps',
        'RPI assumption: ' + (rpi * 100).toFixed(1) + '%', 'Discount rate used: ' + (discRate * 100).toFixed(2) + '%', '',
        'Cheapest PWLB option: ' + bestPwlb.label + ', NPV cost ' + gbp(bestPwlb.npv),
        'Index-linked private placement: NPV cost ' + gbp(cheapest.npv),
        'Potential NPV saving: ' + gbp(saving) + ' (' + (savingPct * 100).toFixed(1) + '%)', '',
        'Please could we set up a time to talk this through?'].join('\n');
      $('ctaLink').href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      callout.hidden = false;
    } else { callout.hidden = true; }

    var box = $('chartBox');
    if (typeof Chart === 'undefined') { box.innerHTML = '<p class="note">Payment chart unavailable. Figures above are unaffected.</p>'; return; }
    var years = Array.from({ length: term }, function (_, i) { return i + 1; });
    var tick = css('--muted'), grid = css('--rule');
    if (chart) chart.destroy();
    chart = new Chart($('paymentChart').getContext('2d'), {
      type: 'line',
      data: { labels: years, datasets: options.map(function (o) { return { label: o.label, data: o.cf, borderColor: o.color, backgroundColor: o.color, borderWidth: 2, borderDash: o.key === 'pp' ? [7, 5] : [], pointRadius: 0, tension: 0.15 }; }) },
      options: {
        responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, color: tick, font: { size: 11 } } },
          tooltip: { callbacks: { label: function (c) { return c.dataset.label + ': ' + gbp(c.parsed.y); } } } },
        scales: {
          x: { title: { display: true, text: 'Year', color: tick }, ticks: { color: tick }, grid: { color: grid } },
          y: { title: { display: true, text: 'Annual payment', color: tick }, ticks: { color: tick, callback: function (v) { return '£' + (v / 1e6).toFixed(1) + 'm'; } }, grid: { color: grid } }
        }
      }
    });
  }

  function renderRatesPanel() {
    var d = CERTAINTY_RATE_DISCOUNT_BPS / 10000;
    var row = function (label, curve, net) { return '<tr><td>' + label + '</td>' + DISPLAY_TERMS.map(function (t) { return '<td>' + pct(interp(curve, t) - (net ? d : 0)) + '</td>'; }).join('') + '</tr>'; };
    $('ratesAsOf').textContent = RATES.asOf;
    $('ratesSource').textContent = RATES.source || '';
    $('ratesTable').innerHTML = '<thead><tr><th>Term</th>' + DISPLAY_TERMS.map(function (t) { return '<th>' + t + 'yr</th>'; }).join('') + '</tr></thead><tbody>' +
      row('PWLB Annuity', RATES.pwlbAnnuityCurve, true) + row('PWLB EIP', RATES.pwlbEipCurve, true) +
      row('PWLB Maturity', RATES.pwlbMaturityCurve, true) + row('Index-linked gilt real yield', RATES.giltRealCurve, false) + '</tbody>';
  }

  function resetFormDefaults() { $('principal').value = 50000000; $('term').value = 40; $('margin').value = 100; }
  function onRatesLoaded() {
    resetFormDefaults();
    $('rpi').value = ((RATES.rpiAssumption || 0.03) * 100).toFixed(1);
    updateReferenceRates(); renderRatesPanel(); calculate();
  }

  fetch(RATES_URL, { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (j) { RATES = j; onRatesLoaded(); })
    .catch(function (err) {
      console.error('Could not load rates', err);
      RATES = {
        asOf: 'fallback values (live rates could not be loaded)',
        source: 'Using built-in fallback rates because the live rates file failed to load.',
        rpiAssumption: 0.03,
        pwlbAnnuityCurve: [{ term: 5, rate: 0.043 }, { term: 10, rate: 0.045 }, { term: 25, rate: 0.049 }, { term: 40, rate: 0.049 }, { term: 50, rate: 0.048 }],
        pwlbEipCurve: [{ term: 5, rate: 0.042 }, { term: 10, rate: 0.044 }, { term: 25, rate: 0.048 }, { term: 40, rate: 0.048 }, { term: 50, rate: 0.047 }],
        pwlbMaturityCurve: [{ term: 5, rate: 0.043 }, { term: 10, rate: 0.045 }, { term: 25, rate: 0.049 }, { term: 40, rate: 0.048 }, { term: 50, rate: 0.047 }],
        giltRealCurve: [{ term: 5, rate: 0.010 }, { term: 10, rate: 0.017 }, { term: 25, rate: 0.021 }, { term: 40, rate: 0.0223 }, { term: 50, rate: 0.022 }]
      };
      onRatesLoaded();
    });

  $('term').addEventListener('input', function () { if (RATES) updateReferenceRates(); });
  $('calcForm').addEventListener('submit', function (e) { e.preventDefault(); if (RATES) calculate(); });
  window.addEventListener('pageshow', function (e) { if (e.persisted && RATES) { resetFormDefaults(); updateReferenceRates(); calculate(); } });
})();
