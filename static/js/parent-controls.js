(() => {
const controls = document.querySelector("[data-parent-controls]");
if (controls) {
  let deadline = performance.now() + Number(controls.dataset.parentRemaining) * 1000;
  let lastSent = -15000;
  let sending = false;
  const lock = () => {
    if (!document.querySelector('[data-sync]')) window.location.assign(controls.dataset.parentBoard);
    else {
      controls.querySelectorAll('input,select,textarea,button').forEach(el => { el.disabled = true; delete el.dataset.syncDisabled; });
      controls.querySelectorAll('a').forEach(el => { if (el.getAttribute('href') !== controls.dataset.parentBoard) el.dataset.parentLocked = 'true'; });
      const label = document.querySelector('#parent-lock-status');
      if (label) label.textContent = 'Parent controls locked. Reopen the board to unlock.';
    }
  };
  const timer = setInterval(() => { if (performance.now() >= deadline) { clearInterval(timer); lock(); } }, 250);
  const activity = async () => {
    if (document.documentElement.dataset.connected === 'false' || sending || performance.now() - lastSent < 15000 || performance.now() >= deadline) return;
    sending = true;
    lastSent = performance.now();
    try {
      const token = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
      const response = await fetch(controls.dataset.parentActivity, {method:"POST",headers:{"X-CSRFToken":token},credentials:"same-origin"});
      if (!response.ok) { lock(); return; }
      const data = await response.json();
      deadline = performance.now() + data.remaining_seconds * 1000;
    } catch { /* Failed requests cannot extend parent authority. */ }
    finally { sending = false; }
  };
  window.addEventListener('board:dispose', () => { clearInterval(timer); for (const event of ['keydown','input','pointerdown']) controls.removeEventListener(event, activity); }, {once:true});
  // Explicit interaction inside parent controls only; no timer/poll/global/child events.
  for (const event of ["keydown", "input", "pointerdown"]) controls.addEventListener(event, activity);
}

})();
