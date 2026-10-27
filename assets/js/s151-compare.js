// Section 151 hub: compare a council's reserves and audit status with its peers.
(function () {
  var root = document.getElementById('cmp');
  if (!root) return;
  var base = root.getAttribute('data-base') || '';
  var dv = '?v=' + (root.getAttribute('data-v') || '');
  var input = document.getElementById('cmpCouncil');
  var out = document.getElementById('cmpOut');
  var R, A;
  var PLURAL = { SD: 'shire districts', UA: 'unitary authorities', MD: 'metropolitan districts', LB: 'London boroughs', SC: 'county councils' };
  var AUD = { B: 'Opinion issued by the backstop', L: 'Opinion issued after the backstop', U: 'Not yet issued' };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function m(v) { var x = v / 1000; return '£' + (Math.abs(x) >= 100 ? x.toFixed(0) : x.toFixed(1)) + 'm'; }
  function pct(v) { return v.toFixed(0) + '%'; }
  function median(a) { a = a.slice().sort(function (x, y) { return x - y; }); var n = a.length; return n ? (n % 2 ? a[(n - 1) / 2] : (a[n / 2 - 1] + a[n / 2]) / 2) : null; }
  function share(a, v) { var below = a.filter(function (x) { return x < v; }).length; return Math.round(100 * below / a.length); }
  function date(d) { if (!d) return ''; var p = d.split('-'); var mo = ['January','February','March','April','May','June','July','August','September','October','November','December'][+p[1] - 1]; return +p[2] + ' ' + mo + ' ' + p[0]; }

  function bar(peers, v, label) {
    var sorted = peers.slice().sort(function (x, y) { return x - y; });
    var lo = sorted[Math.floor(sorted.length * 0.05)], hi = sorted[Math.ceil(sorted.length * 0.95) - 1];
    function pos(x) { return Math.max(0, Math.min(100, (x - lo) / (hi - lo) * 100)); }
    var q1 = sorted[Math.floor(sorted.length * 0.25)], q3 = sorted[Math.floor(sorted.length * 0.75)], md = median(sorted);
    return '<div class="cmp-bar" role="img" aria-label="' + esc(label) + '">' +
      '<span class="iqr" style="left:' + pos(q1) + '%;width:' + (pos(q3) - pos(q1)) + '%"></span>' +
      '<span class="med" style="left:' + pos(md) + '%"></span>' +
      '<span class="you" style="left:' + pos(v) + '%"></span></div>' +
      '<p class="cmp-key"><span class="k-you"></span>This council <span class="k-med"></span>Median <span class="k-iqr"></span>Middle half of peers</p>';
  }

  function render(name) {
    var c = R.councils.filter(function (x) { return x.n === name; })[0];
    if (!c) { out.innerHTML = ''; return; }
    var peers = R.councils.filter(function (x) { return x.c === c.c && x.r31; });
    var cls = PLURAL[c.c];
    var h = '<h3>' + esc(c.n) + '</h3><p class="cmp-sub">' + esc(R.classes[c.c]) + '. Compared with ' + peers.length + ' ' + cls + ' that reported data.</p>';
    if (!c.r31) {
      h += c.nd === 'x'
        ? '<p>This council\'s ' + esc(R.year) + ' revenue outturn return was not received in time for MHCLG\'s publication, so reserves data is not available.</p>'
        : '<p>This council\'s ' + esc(R.year) + ' revenue outturn return does not include usable figures for its reserves, so it is not compared here.</p>';
    } else {
      var ratio = peers.map(function (x) { return x.r31 / x.nre * 100; });
      var mine = c.r31 / c.nre * 100;
      var uRatio = peers.map(function (x) { return x.u31 / x.nre * 100; });
      var uMine = c.u31 / c.nre * 100;
      h += '<div class="cmp-grid">';
      h += '<div class="cmp-card"><p class="eyebrow">Non-ringfenced reserves, 31 March 2026</p><p class="num">' + m(c.r31) + '</p>' +
        '<p><b>' + pct(mine) + '</b> of net revenue expenditure. Median for ' + cls + ': <b>' + pct(median(ratio)) + '</b>. Higher than ' + share(ratio, mine) + '% of ' + cls + '.</p>' +
        bar(ratio, mine, 'Reserves as a share of net revenue expenditure compared with peers') + '</div>';
      if (c.r01) {
        var chg = peers.filter(function (x) { return x.r01; }).map(function (x) { return (x.r31 - x.r01) / x.r01 * 100; });
        var cm = (c.r31 - c.r01) / c.r01 * 100;
        h += '<div class="cmp-card"><p class="eyebrow">Change during ' + esc(R.year) + '</p><p class="num">' + (c.r31 >= c.r01 ? '+' : '−') + m(Math.abs(c.r31 - c.r01)) + '</p>' +
          '<p><b>' + (cm >= 0 ? '+' : '') + cm.toFixed(0) + '%</b> in the year. Median for ' + cls + ': <b>' + (median(chg) >= 0 ? '+' : '') + median(chg).toFixed(0) + '%</b>.</p>' +
          bar(chg, cm, 'Change in reserves compared with peers') + '</div>';
      }
      h += '<div class="cmp-card"><p class="eyebrow">Unallocated (general) reserves</p><p class="num">' + m(c.u31) + '</p>' +
        '<p><b>' + pct(uMine) + '</b> of net revenue expenditure. Median for ' + cls + ': <b>' + pct(median(uRatio)) + '</b>.</p>' +
        bar(uRatio, uMine, 'Unallocated reserves compared with peers') + '</div>';
      if (c.hra) h += '<div class="cmp-card"><p class="eyebrow">HRA reserves, 31 March 2026</p><p class="num">' + m(c.hra) + '</p><p>Held in the ring-fenced Housing Revenue Account, separate from the figures above.</p></div>';
      h += '</div>';
    }
    var a = A && A.councils[c.n];
    h += '<h4>External audit</h4>';
    if (a) {
      h += '<div class="table-wrap"><table class="rates cmp-audit"><thead><tr><th scope="col">Accounts</th><th scope="col">Status</th><th scope="col">Signed</th></tr></thead><tbody>';
      A.years.forEach(function (y) { var r = a[y]; if (r) h += '<tr><td>' + y + '</td><td>' + AUD[r[0]] + '</td><td>' + (date(r[1]) || '–') + '</td></tr>'; });
      h += '</tbody></table></div><p class="note">Audit status as at ' + esc(A.asAt) + ', from <a href="' + esc(A.source) + '" rel="noopener">PSAA</a>. PSAA\'s data shows when each opinion was signed, not whether it was unmodified, qualified or disclaimed: the auditor\'s report in the council\'s published accounts says which.</p>';
    } else {
      h += '<p>This council is not audited under PSAA\'s appointing scheme, so no audit status is shown.</p>';
    }
    out.innerHTML = h;
  }

  function onPick() {
    var v = input.value.trim().toLowerCase();
    var hit = R.councils.filter(function (x) { return x.n.toLowerCase() === v; })[0];
    if (hit) { render(hit.n); try { localStorage.setItem('s151Council', hit.n); } catch (e) {} }
  }

  Promise.all([
    fetch(base + 'assets/data/s151-reserves.json' + dv).then(function (r) { return r.json(); }),
    fetch(base + 'assets/data/s151-audit.json' + dv).then(function (r) { return r.json(); }).catch(function () { return null; })
  ]).then(function (res) {
    R = res[0]; A = res[1];
    var dl = document.getElementById('councilList');
    dl.innerHTML = R.councils.map(function (x) { return '<option value="' + esc(x.n) + '"></option>'; }).join('');
    input.disabled = false;
    input.addEventListener('change', onPick);
    input.addEventListener('input', onPick);
    var saved = null; try { saved = localStorage.getItem('s151Council'); } catch (e) {}
    if (saved) { input.value = saved; onPick(); }
  }).catch(function () {
    out.innerHTML = '<p>The comparison data could not be loaded. Please try again later.</p>';
  });
})();
