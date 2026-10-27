// Section 151 hub: live PWLB maturity rates (same daily feed as the PWLB vs index-linked tool)
(function () {
  var box = document.getElementById('pwlbLive');
  if (!box) return;
  var URL = 'https://gist.githubusercontent.com/nhaverly/2221652235336db07f5df927d45ffad5/raw/rates.json';
  function at(curve, term) {
    if (!curve || !curve.length) return null;
    for (var i = 0; i < curve.length; i++) if (curve[i].term === term) return curve[i].rate;
    for (var j = 1; j < curve.length; j++) {
      var a = curve[j - 1], b = curve[j];
      if (term > a.term && term < b.term) return a.rate + (b.rate - a.rate) * (term - a.term) / (b.term - a.term);
    }
    return null;
  }
  fetch(URL, { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (j) {
      var html = [10, 25, 50].map(function (t) {
        var r = at(j.pwlbMaturityCurve, t);
        return '<span><b>' + (r == null ? '–' : (r * 100).toFixed(2) + '%') + '</b>' + t + ' years</span>';
      }).join('');
      box.innerHTML = html;
      var asof = document.getElementById('pwlbAsOf');
      if (asof && j.asOf) asof.textContent = j.asOf;
    })
    .catch(function () {
      box.innerHTML = '<span>Live rates are unavailable right now. See the <a href="https://dmo.gov.uk/responsibilities/local-authority-lending/lending-arrangements">Debt Management Office</a>.</span>';
    });
})();
