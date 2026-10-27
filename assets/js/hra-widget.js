/* Haverly HRA Assistant. Framework-free; no API keys or chat transcripts in storage.
 * Drop-in configuration is read from this script's data-* attributes. */
(() => {
  'use strict';
  const script = document.currentScript;
  if (!script || customElements.get('hc-hra-assistant')) return;
  const endpoint = script.dataset.endpoint || 'https://haverly-hra-assistant.nick-haverly.workers.dev/';
  const siteRoot = new URL(script.dataset.siteRoot || '/', document.baseURI);
  const cssURL = new URL('../css/hra-widget.css', script.src).href;
  const page = name => new URL(name + (siteRoot.pathname.endsWith('.html') ? '.html' : ''), siteRoot).href;
  const KEY = 'hraChatUsage', LIMIT = 2, MAX = 1000;
  let memory = { day: '', n: 0 };
  const today = () => new Date().toISOString().slice(0, 10);
  function usage() {
    try {
      const value = JSON.parse(localStorage.getItem(KEY) || '{}');
      return value.day === today() && Number.isFinite(value.n) ? Math.max(0, value.n) : 0;
    } catch (_) { return memory.day === today() ? memory.n : 0; }
  }
  function increment() {
    memory = { day: today(), n: usage() + 1 };
    try { localStorage.setItem(KEY, JSON.stringify(memory)); } catch (_) { /* Private storage fallback. */ }
    window.dispatchEvent(new Event('hc-hra-usage'));
  }
  // Safe, small Markdown renderer: all ordinary response text stays in text nodes.
  // Only HTTPS/HTTP links become anchors; HTML and script URLs are never interpreted.
  function inline(text, parent) {
    const rx = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|\*\*([^*]+)\*\*|(https?:\/\/[^\s<>]+)/g;
    let last = 0, m;
    while ((m = rx.exec(text))) {
      parent.append(document.createTextNode(text.slice(last, m.index)));
      if (m[3]) { const b = document.createElement('strong'); b.textContent = m[3]; parent.append(b); }
      else {
        const a = document.createElement('a'); a.textContent = m[1] || m[4];
        try { const u = new URL(m[2] || m[4]); if (!['https:', 'http:'].includes(u.protocol)) throw Error(); a.href = u.href; }
        catch (_) { parent.append(document.createTextNode(m[0])); last = rx.lastIndex; continue; }
        a.target = '_blank'; a.rel = 'noopener noreferrer'; parent.append(a);
      }
      last = rx.lastIndex;
    }
    parent.append(document.createTextNode(text.slice(last)));
  }
  function renderReply(text, parent) {
    let list;
    for (const line of text.replace(/\r/g, '').split('\n')) {
      if (!line.trim()) { list = null; continue; }
      const item = /^\s*(?:[-*•]|\d+\.)\s+(.+)/.exec(line);
      if (item) {
        if (!list) { list = document.createElement('ul'); parent.append(list); }
        const li = document.createElement('li'); inline(item[1], li); list.append(li);
      } else {
        list = null; const p = document.createElement('p');
        inline(line.replace(/^#{1,6}\s+/, ''), p); parent.append(p);
      }
    }
  }
  class HraAssistant extends HTMLElement {
    connectedCallback() {
      if (this.shadowRoot) return;
      this.inlineMode = this.hasAttribute('inline'); this.busy = false; this.history = [];
      const root = this.attachShadow({ mode: 'open' });
      root.innerHTML = `<link rel="stylesheet" href="${cssURL}">
        <button class="launcher" type="button" aria-expanded="false" aria-controls="panel" aria-label="Open HRA assistant"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-6 4V6a2 2 0 0 1 2-2Z"/><path d="M7 9h10M7 13h6"/></svg><span>HRA assistant</span><span class="launcher-plus" aria-hidden="true">+</span></button>
        <section id="panel" class="panel" aria-label="HRA assistant" ${this.inlineMode ? '' : 'role="dialog" hidden'}>
          <header><div><p class="brand">HAVERLY CONSULTING</p><h2>HRA assistant</h2><p class="subline">A clearer starting point.</p></div><button class="close" type="button" aria-label="Close HRA assistant">×</button></header>
          <div class="context"><span class="allowance"></span><a class="full-page" href="${page('hra-assistant')}">Full page ↗</a></div>
          <p class="scope">General HRA guidance for England, as at October 2026. Not legal, financial or accounting advice.</p>
          <div class="messages" role="log" aria-label="Conversation" aria-live="polite" aria-relevant="additions text" tabindex="0"><div class="welcome"><p class="intro">How can we help?</p><p>Ask a question about the Housing Revenue Account. Answers draw on our knowledge base, with sources to check.</p><div class="starters"><button type="button">What can be charged to the HRA?</button><button type="button">How do Right to Buy receipts work?</button><button type="button">What are the rules on rent setting?</button></div></div></div>
          <div class="limit" hidden><p>You’ve used today’s two free questions. For advice on your council’s position, speak to our specialists.</p><a href="${page('advisory-partnership')}">Explore the Advisory Partnership →</a></div>
          <form><label for="question">Your HRA question</label><div class="composer"><textarea id="question" rows="2" maxlength="${MAX}" placeholder="Type your question…" required></textarea><button class="send" type="submit" aria-label="Send question" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 19 0-14M6 11l6-6 6 6"/></svg></button></div><div class="input-meta"><span>Enter to send · Shift + Enter for a new line</span><span class="count">0 / 1000</span></div></form>
          <p class="privacy">Answers can be wrong. Check cited sources before acting. Don’t include personal or confidential information. <a href="${page('privacy')}#hra-assistant">Privacy notice</a></p>
          <p class="status" role="status" aria-live="polite"></p>
        </section>`;
      this.root = root; this.panel = root.querySelector('#panel'); this.launcher = root.querySelector('.launcher');
      this.box = root.querySelector('textarea'); this.send = root.querySelector('.send'); this.log = root.querySelector('.messages');
      if (this.inlineMode) { this.launcher.hidden = true; root.querySelector('.close').hidden = true; root.querySelector('.full-page').hidden = true; }
      this.launcher.addEventListener('click', () => this.panel.hidden ? this.open() : this.close());
      root.querySelector('.close').addEventListener('click', () => this.close());
      root.addEventListener('keydown', e => { if (e.key === 'Escape' && !this.inlineMode) { this.close(); e.stopPropagation(); } });
      root.querySelector('form').addEventListener('submit', e => { e.preventDefault(); this.ask(); });
      this.box.addEventListener('input', () => this.update());
      this.box.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); this.ask(); }
      });
      root.querySelectorAll('.starters button').forEach(b => b.addEventListener('click', () => { this.box.value = b.textContent; this.update(); this.box.focus(); }));
      this.onStorage = () => this.update();
      window.addEventListener('storage', this.onStorage); window.addEventListener('hc-hra-usage', this.onStorage);
      this.update();
    }
    disconnectedCallback() {
      window.removeEventListener('storage', this.onStorage); window.removeEventListener('hc-hra-usage', this.onStorage);
      if (this.controller) this.controller.abort();
    }
    update() {
      const left = Math.max(0, LIMIT - usage());
      this.root.querySelector('.allowance').textContent = `${left} free question${left === 1 ? '' : 's'} left today`;
      this.root.querySelector('.limit').hidden = left > 0;
      this.root.querySelector('form').hidden = left === 0;
      this.root.querySelector('.starters').hidden = left === 0 || this.history.length > 0;
      this.root.querySelector('.count').textContent = `${this.box.value.length} / ${MAX}`;
      this.send.disabled = this.busy || !this.box.value.trim() || left === 0;
      this.box.disabled = this.busy; this.log.setAttribute('aria-busy', String(this.busy));
    }
    open() {
      this.returnFocus = document.activeElement === this ? this.launcher : document.activeElement; this.panel.hidden = false; this.launcher.setAttribute('aria-expanded', 'true');
      this.launcher.setAttribute('aria-label', 'Close HRA assistant'); this.root.querySelector('.launcher-plus').textContent = '−';
      this.update(); (usage() < LIMIT && !this.busy ? this.box : this.root.querySelector('.close')).focus();
    }
    close() {
      if (this.inlineMode) return;
      this.panel.hidden = true; this.launcher.setAttribute('aria-expanded', 'false'); this.launcher.setAttribute('aria-label', 'Open HRA assistant');
      this.root.querySelector('.launcher-plus').textContent = '+';
      if (this.returnFocus && this.returnFocus !== document.body && this.returnFocus.isConnected) this.returnFocus.focus(); else this.launcher.focus();
    }
    message(kind, text) {
      const article = document.createElement('div'); article.className = `message ${kind}`;
      const label = document.createElement('span'); label.className = 'message-label'; label.textContent = kind === 'user' ? 'You' : 'HRA assistant';
      const content = document.createElement('div'); content.className = 'message-content'; content.textContent = text;
      article.append(label, content); this.log.append(article); this.log.scrollTop = this.log.scrollHeight; return content;
    }
    async ask() {
      const q = this.box.value.trim().slice(0, MAX);
      if (!q || this.busy || usage() >= LIMIT) return;
      this.root.querySelector('.welcome').hidden = true; this.message('user', q);
      const reply = this.message('assistant', 'Checking the knowledge base…');
      this.busy = true; this.update(); this.root.querySelector('.status').textContent = 'Finding an answer.';
      this.controller = new AbortController(); const timer = setTimeout(() => this.controller.abort(), 30000);
      try {
        if (location.protocol === 'file:') throw new Error('local-preview');
        const messages = [...this.history, { role: 'user', content: q }].slice(-9);
        const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ messages }), signal: this.controller.signal, credentials: 'omit' });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) { const error = new Error('request-failed'); error.status = response.status; throw error; }
        if (typeof data.reply !== 'string' || !data.reply.trim()) throw new Error('invalid-reply');
        reply.replaceChildren(); renderReply(data.reply, reply);
        this.history.push({ role: 'user', content: q }, { role: 'assistant', content: data.reply });
        this.box.value = ''; increment(); this.root.querySelector('.status').textContent = 'Answer received.';
      } catch (error) {
        reply.closest('.message').classList.add('error');
        reply.textContent = error.message === 'local-preview' ? 'Live answers need a hosted website. The design and pop-up work in this preview; use the current HRA assistant for an answer.' : error.status === 429 ? 'The assistant’s request limit has been reached. Please try again later or contact our team.' : error.name === 'AbortError' ? 'The answer took too long. Your question is still below so you can try again.' : 'We couldn’t connect to the assistant. Your question is still below; please try again or use the current HRA assistant.';
        const p = document.createElement('p'), a = document.createElement('a'); a.href = 'https://www.haverlyconsulting.co.uk/hra-assistant'; a.textContent = 'Open the current HRA assistant ↗'; a.target = '_blank'; a.rel = 'noopener noreferrer'; p.append(a); reply.append(p);
        this.root.querySelector('.status').textContent = 'No answer received. You can try again.';
      } finally {
        clearTimeout(timer); this.busy = false; this.update(); this.log.scrollTop = this.log.scrollHeight;
        if (!this.panel.hidden && usage() < LIMIT && (this.inlineMode || this.contains(document.activeElement) || document.activeElement === this)) this.box.focus();
      }
    }
  }
  customElements.define('hc-hra-assistant', HraAssistant);
  const mount = document.querySelector('[data-hra-inline]');
  const widget = document.createElement('hc-hra-assistant');
  if (mount) { widget.setAttribute('inline', ''); mount.append(widget); } else { document.body.append(widget); }
  document.addEventListener('click', e => {
    const trigger = e.target.closest('[data-open-hra]'); if (!trigger) return;
    e.preventDefault(); if (mount) widget.scrollIntoView({ block: 'center', behavior: 'smooth' }); else widget.open();
  });
})();
