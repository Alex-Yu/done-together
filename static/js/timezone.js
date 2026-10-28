const timezoneSelect = document.getElementById("id_timezone");
try {
  const suggestion = Intl.DateTimeFormat().resolvedOptions().timeZone;
  if (timezoneSelect && [...timezoneSelect.options].some(option => option.value === suggestion)) {
    timezoneSelect.value = suggestion;
  }
} catch { /* UTC remains the visible fallback when Intl is unavailable. */ }
