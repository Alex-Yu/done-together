(() => {
  function update() {
    const now = new Date();
    const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
    document.querySelectorAll('[data-local-due]').forEach(card => {
      const overdue = card.dataset.state === 'to_do' && card.dataset.localDue < today;
      card.classList.toggle('is-overdue', overdue);
      card.querySelector('[data-overdue]').hidden = !overdue;
    });
  }
  update();
  setInterval(update, 30000);
})();
