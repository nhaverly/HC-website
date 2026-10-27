// Section 151 hub: data insights charts (Chart.js). Data from assets/data and an inline trend series.
(function () {
  var root = document.getElementById('insights-data');
  if (!root || !window.Chart) return;
  var base = root.getAttribute('data-base') || '';
  var NAVY = '#090F54', TEAL = '#1A8FA6', GRID = 'rgba(9,15,84,0.10)', INK = '#0B090A', MUTED = '#090F54';
  Chart.defaults.font.family = 'Arial, "Helvetica Neue", sans-serif';
  Chart.defaults.font.size = 13;
  Chart.defaults.color = MUTED;
  var tip = { backgroundColor: '#FFFFFF', titleColor: INK, bodyColor: INK, borderColor: 'rgba(9,15,84,0.25)', borderWidth: 1, padding: 10, displayColors: false };
  function axes(y) { return { grid: { color: GRID, drawTicks: false }, border: { display: false }, ticks: y || {} }; }

  // 1. Audit timeliness
  fetch(base + 'assets/data/s151-audit.json').then(function (r) { return r.json(); }).then(function (A) {
    var s = A.timeliness || [];
    new Chart(document.getElementById('chartAudit'), {
      type: 'bar',
      data: {
        labels: s.map(function (x) { return x.year; }),
        datasets: [{
          data: s.map(function (x) { return x.pct; }),
          backgroundColor: s.map(function (x) { return x.basis === 'backstop' ? TEAL : NAVY; }),
          borderRadius: { topLeft: 4, topRight: 4 }, borderSkipped: 'bottom', maxBarThickness: 56
        }]
      },
      options: {
        maintainAspectRatio: false, animation: false,
        scales: { x: { grid: { display: false }, border: { color: GRID } }, y: Object.assign(axes({ callback: function (v) { return v + '%'; } }), { min: 0, max: 100 }) },
        plugins: {
          legend: { display: false },
          tooltip: Object.assign({}, tip, { callbacks: {
            title: function (i) { return i[0].label + ' accounts'; },
            label: function (i) { var x = s[i.dataIndex]; return x.timely + ' of ' + x.councils + ' council audits (' + x.pct.toFixed(0) + '%) signed by the ' + (x.basis === 'backstop' ? 'backstop date' : 'statutory deadline'); }
          } })
        }
      }
    });
    document.getElementById('tblAudit').innerHTML = s.map(function (x) {
      return '<tr><td>' + x.year + '</td><td>' + (x.basis === 'backstop' ? 'Backstop' : 'Statutory deadline') + '</td><td>' + x.timely + ' of ' + x.councils + '</td><td>' + x.pct.toFixed(1) + '%</td></tr>';
    }).join('');
  });

  // 2. Reserves trend
  var T = JSON.parse(root.getAttribute('data-trend'));
  new Chart(document.getElementById('chartTrend'), {
    type: 'line',
    data: { labels: T.map(function (x) { return x[0].replace('31 March ', 'Mar '); }),
      datasets: [{ data: T.map(function (x) { return +(x[1] / x[2] * 100).toFixed(1); }), borderColor: NAVY, backgroundColor: NAVY, borderWidth: 2, pointRadius: 5, pointHoverRadius: 7, tension: 0 }] },
    options: {
      maintainAspectRatio: false, animation: false, interaction: { mode: 'index', intersect: false },
      scales: { x: { grid: { display: false }, border: { color: GRID } }, y: Object.assign(axes({ callback: function (v) { return v + '%'; } }), { min: 0, max: 60 }) },
      plugins: { legend: { display: false }, tooltip: Object.assign({}, tip, { callbacks: {
        title: function (i) { return T[i[0].dataIndex][0]; },
        label: function (i) { var x = T[i.dataIndex]; return '£' + x[1].toFixed(1) + 'bn, ' + (x[1] / x[2] * 100).toFixed(0) + '% of net revenue expenditure'; }
      } }) }
    }
  });

  // 3. Reserves spread by council type
  fetch(base + 'assets/data/s151-reserves.json').then(function (r) { return r.json(); }).then(function (R) {
    var order = ['SC', 'UA', 'MD', 'LB', 'SD'];
    var narrow = document.getElementById('chartSpread').parentNode.clientWidth < 600;
    var TICKS = narrow ? [1, 10, 100, 800] : [1, 5, 10, 25, 50, 100, 200, 400, 800];
    var SHORT = { SC: 'Counties', UA: 'Unitaries', MD: 'Met districts', LB: 'London boroughs', SD: 'Districts' };
    var pts = [], meds = [];
    function median(a) { a = a.slice().sort(function (x, y) { return x - y; }); var n = a.length; return n % 2 ? a[(n - 1) / 2] : (a[n / 2 - 1] + a[n / 2]) / 2; }
    order.forEach(function (k, row) {
      var vals = [];
      R.councils.forEach(function (c, i) {
        if (c.c !== k || !c.r31) return;
        var v = Math.max(c.r31 / c.nre * 100, 0.9);
        vals.push(v);
        var jitter = (((i * 9301 + 49297) % 233280) / 233280 - 0.5) * 0.5;
        pts.push({ x: v, y: row + jitter, n: c.n });
      });
      meds.push({ x: median(vals), y: row, n: 'Median, ' + R.classes[k].toLowerCase() + 's' });
    });
    new Chart(document.getElementById('chartSpread'), {
      type: 'scatter',
      data: { datasets: [
        { label: 'Council', order: 2, data: pts, backgroundColor: 'rgba(9,15,84,0.45)', borderColor: '#FFFFFF', borderWidth: 1, pointRadius: 4.5, pointHoverRadius: 7 },
        { label: 'Median', order: 1, data: meds, pointStyle: 'line', rotation: 90, pointRadius: 20, pointHoverRadius: 22, borderColor: TEAL, borderWidth: 5, backgroundColor: TEAL }
      ] },
      options: {
        maintainAspectRatio: false, animation: false, indexAxis: 'x',
        scales: {
          x: Object.assign({ grid: { drawTicks: false, color: function (c) { return TICKS.indexOf(c.tick && c.tick.value) >= 0 ? GRID : 'transparent'; } }, border: { display: false }, ticks: { callback: function (v) { return TICKS.indexOf(v) >= 0 ? v + '%' : ''; }, autoSkip: false, maxRotation: 0 } }, { type: 'logarithmic', min: 0.8, max: 1000, title: { display: true, text: narrow ? 'Reserves as % of net revenue expenditure (log scale)' : 'Non-ringfenced reserves as % of net revenue expenditure (log scale)' } }),
          y: { min: -0.6, max: order.length - 0.4, reverse: true, grid: { display: false }, border: { display: false },
            afterBuildTicks: function (ax) { ax.ticks = order.map(function (_, i) { return { value: i }; }); },
            ticks: { callback: function (v) { var k = order[v]; return k ? (narrow ? SHORT[k] : R.classes[k] + 's') : ''; } } }
        },
        plugins: {
          legend: { display: true, position: 'top', align: 'start', labels: { usePointStyle: true, boxWidth: 10, color: INK } },
          tooltip: Object.assign({}, tip, { callbacks: { title: function () { return ''; }, label: function (i) { return i.raw.n + ': ' + i.raw.x.toFixed(0) + '%'; } } })
        }
      }
    });
  });
})();
