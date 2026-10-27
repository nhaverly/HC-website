// Section 151 hub: floating section menu. Sits under the sticky site header, highlights the section in view,
// and keeps anchor jumps clear of both bars.
(function () {
  var nav = document.getElementById('hubNav');
  if (!nav) return;
  var head = document.querySelector('.site-head');
  function sizes() {
    var h = head ? head.offsetHeight : 0;
    document.documentElement.style.setProperty('--head-h', h + 'px');
    document.documentElement.style.scrollPaddingTop = (h + nav.offsetHeight + 12) + 'px';
  }
  sizes(); window.addEventListener('resize', sizes);
  var links = Array.prototype.slice.call(nav.querySelectorAll('a'));
  var targets = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  function current() {
    var line = (head ? head.offsetHeight : 0) + nav.offsetHeight + 120, idx = -1;
    targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top <= line) idx = i; });
    links.forEach(function (a, i) {
      if (i === idx) {
        if (a.getAttribute('aria-current') !== 'true') {
          a.setAttribute('aria-current', 'true');
          var ul = nav.querySelector('ul'), l = a.parentNode.offsetLeft;
          if (l < ul.scrollLeft || l + a.offsetWidth > ul.scrollLeft + ul.clientWidth) ul.scrollTo({ left: l - 16, behavior: 'smooth' });
        }
      } else a.removeAttribute('aria-current');
    });
  }
  var ticking = false;
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { current(); ticking = false; }); } }, { passive: true });
  current();
})();
