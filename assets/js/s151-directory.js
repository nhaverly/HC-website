// Section 151 hub: searchable directory of S151 officers.
(function () {
  var root = document.getElementById('dir');
  if (!root) return;
  var base = root.getAttribute('data-base') || '';
  var dv = '?v=' + (root.getAttribute('data-v') || '');
  var body = document.getElementById('dirBody'), q = document.getElementById('dirSearch'),
      typ = document.getElementById('dirType'), count = document.getElementById('dirCount');
  var TYPES = { LB: 'London boroughs', MD: 'Metropolitan districts', UA: 'Unitary authorities', SC: 'County councils', SD: 'District councils' };
  var D = [];
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function when(d) {
    if (!d) return '';
    var p = d.split('-'), m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return (p[2] ? +p[2] + ' ' : '') + (p[1] ? m[+p[1] - 1] + ' ' : '') + p[0];
  }
  function render() {
    var term = q.value.trim().toLowerCase(), t = typ.value;
    var rows = D.filter(function (x) {
      return (!t || x.type === t) && (!term || (x.council + ' ' + (x.name || '')).toLowerCase().indexOf(term) >= 0);
    });
    body.innerHTML = rows.map(function (x) {
      var who = x.vacant ? '<span class="dir-role">Post currently vacant</span>' : x.name
        ? '<b>' + esc(x.name) + '</b>' + (x.interim ? ' <span class="dir-tag">Interim</span>' : '') + '<br><span class="dir-role">' + esc(x.title) + '</span>'
        : '<span class="dir-role">Not yet confirmed from published sources</span>';
      return '<tr><td>' + esc(x.council) + '</td><td>' + who + '</td></tr>';
    }).join('') || '<tr><td colspan="2">No councils match your search.</td></tr>';
    count.textContent = rows.length + ' of ' + D.length + ' councils';
  }
  fetch(base + 'assets/data/s151-directory.json' + dv).then(function (r) { return r.json(); }).then(function (j) {
    D = j.entries.slice().sort(function (a, b) { return a.council.localeCompare(b.council); });
    Object.keys(TYPES).forEach(function (k) {
      if (D.some(function (x) { return x.type === k; })) typ.insertAdjacentHTML('beforeend', '<option value="' + k + '">' + TYPES[k] + '</option>');
    });
    q.addEventListener('input', render); typ.addEventListener('change', render);
    render();
  }).catch(function () { body.innerHTML = '<tr><td colspan="2">The directory could not be loaded. Please try again later.</td></tr>'; });
})();
