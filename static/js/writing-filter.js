(() => {
  const filters = document.querySelector('.writing-filters');
  const entries = document.querySelectorAll('.writing-entry');
  const status = document.querySelector('.writing-result-count');
  if (!filters || !entries.length) return;

  const updateStatus = () => {
    if (!status) return;
    const count = [...entries].filter((entry) => !entry.hidden).length;
    status.textContent = `${count} ${count === 1 ? 'piece' : 'pieces'}`;
    status.hidden = false;
  };
  filters.hidden = false;
  updateStatus();
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-filter]');
    if (!button || !filters.contains(button)) return;
    filters.querySelectorAll('button[data-filter]').forEach((item) => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    entries.forEach((entry) => {
      entry.hidden = button.dataset.filter !== 'all' && entry.dataset.topic !== button.dataset.filter;
    });
    updateStatus();
  });
})();
