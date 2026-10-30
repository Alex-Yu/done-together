(() => {
  const field = document.querySelector('[name=browser_timezone]');
  if (field && !field.value) {
    try { field.value = Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (_) { /* Keep editable fallback. */ }
  }
})();
