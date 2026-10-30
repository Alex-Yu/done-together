(() => {
  const sync = document.querySelector('[data-sync]');
  if (!sync) return;
  const status = sync.querySelector('[data-sync-status]');
  let key = '', busy = false, connected = false, uncertain = false, disposed = false;
  const listeners = new AbortController();
  window.addEventListener('board:dispose', () => { disposed = true; clearInterval(timer); listeners.abort(); }, {once:true});
  const state = (ready, message) => {
    connected = ready;
    document.documentElement.dataset.connected = String(ready);
    status.textContent = message;
    document.querySelectorAll('form[method="post"] button, form[method="post"] input, form[method="post"] select, form[method="post"] textarea').forEach(control => {
      if (!ready || uncertain) {
        if (!control.disabled) { control.dataset.syncDisabled = 'true'; control.disabled = true; }
      } else if (control.dataset.syncDisabled) {
        control.disabled = false; delete control.dataset.syncDisabled;
      }
    });
    document.querySelectorAll('a[href*="/households/"]').forEach(link => {
      if (!ready) link.setAttribute('aria-disabled', 'true');
      else link.removeAttribute('aria-disabled');
    });
  };
  const clear = () => {
    window.dispatchEvent(new Event('board:dispose'));
    document.querySelector('main').replaceChildren();
    const message = document.createElement('p');
    message.textContent = 'Board access ended. Sign in again to view your household.';
    const link = document.createElement('a'); link.href = '/accounts/login/'; link.textContent = 'Sign in';
    document.querySelector('main').append(message, link);
  };
  function replace(selector, html) {
    const old = document.querySelector(selector);
    if (!old || old.outerHTML === html) return;
    // Forms live outside these regions. Restore a focused action by its scoped URL.
    const active = old.contains(document.activeElement) ? document.activeElement.getAttribute('href') : null;
    if (selector === '[data-schedules]') old.innerHTML = html;
    else old.outerHTML = html;
    if (active) [...document.querySelectorAll(`${selector} a`)].find(a => a.getAttribute('href') === active)?.focus({preventScroll:true});
  }
  async function poll(force = false) {
    if (busy || disposed) return;
    busy = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 3500);
    try {
      const response = await fetch(`${sync.dataset.url}?key=${encodeURIComponent(force ? '' : key)}`, {credentials:'same-origin',cache:'no-store',signal:controller.signal});
      if ([401,403,404].includes(response.status)) { clear(); return; }
      if (!response.ok || response.redirected) throw new Error('unavailable');
      const data = await response.json();
      if (disposed) return;
      if (data.columns) {
        replace('.child-columns', data.columns);
        replace('[data-schedules]', data.schedules);
        document.dispatchEvent(new Event('board:updated'));
      }
      if (!data.unlocked) {
        document.querySelectorAll('[data-parent-controls]').forEach(el => {
          el.querySelectorAll('a,button,input,select,textarea').forEach(control => {
            if (control.tagName === 'A' && control.getAttribute('href') === el.dataset.parentBoard) return;
            if (control.tagName === 'A') { control.setAttribute('aria-disabled','true'); control.dataset.parentLocked = 'true'; }
            else { control.disabled = true; delete control.dataset.syncDisabled; }
          });
        });
        const label = document.querySelector('#parent-lock-status');
        if (label) label.textContent = 'Parent controls locked. Reopen the board to unlock.';
      }
      const changed = key && data.key !== key;
      key = data.key;
      state(navigator.onLine, uncertain ? 'Connection restored. The previous action may have committed. Return to the board to check its result before trying again.' : changed && !document.querySelector('.board-page') ? 'Connected. The household changed; your input is preserved. Stale actions will be rejected. Return to the board for current data.' : 'Connected. Board synchronized.');
    } catch { if (!disposed) state(false, 'Disconnected — read only. Last synchronized board retained. Reconnecting…'); }
    finally { clearTimeout(timeout); busy = false; }
  }
  state(false, 'Checking connection — changes disabled until synchronized.');
  document.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (link?.getAttribute('aria-disabled') === 'true' || link?.dataset.parentLocked) event.preventDefault();
  }, {capture:true,signal:listeners.signal});
  document.addEventListener('submit', async event => {
    const form = event.target;
    if (form.method.toLowerCase() !== 'post') return;
    event.preventDefault();
    if (!connected || uncertain) return;
    // No retries and no optimistic updates: a missing response has an unknown outcome.
    const body = new FormData(form);
    if (event.submitter?.name) body.append(event.submitter.name, event.submitter.value);
    uncertain = true;
    state(false, 'Saving… Changes disabled while awaiting confirmation.');
    try {
      const response = await fetch(form.getAttribute('action') || location.href, {method:'POST',body,credentials:'same-origin',cache:'no-store'});
      if ([401,403].includes(response.status)) { state(false, 'Action denied. Checking board access and current data…'); poll(true); return; }
      if (response.status >= 500) throw new Error('unavailable');
      const html = await response.text();
      // fetch already followed the redirect and consumed one-use messages.
      // Render that confirmed document rather than issuing a second GET.
      if (response.redirected) history.replaceState(null, '', response.url);
      window.dispatchEvent(new Event('board:dispose'));
      document.open(); document.write(html); document.close();
    } catch { state(false, 'Action not confirmed. It may have committed. Reconnecting to check current data; no action will be retried.'); poll(true); }
  }, {capture:true,signal:listeners.signal});
  window.addEventListener('offline', () => state(false, 'Disconnected — read only. Last synchronized board retained.'), {signal:listeners.signal});
  window.addEventListener('online', () => poll(true), {signal:listeners.signal});
  window.addEventListener('pageshow', () => { state(false, 'Checking connection…'); poll(true); }, {signal:listeners.signal});
  const timer = setInterval(() => poll(!connected), 2000);
  poll(true);
})();
