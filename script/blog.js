/* Progressive enhancement: all real article links remain available without JS. */
(() => {
  'use strict';
  const root = document.querySelector('[data-blog]');
  if (!root) return;
  const cards = [...root.querySelectorAll('.blog-card')];
  const search = root.querySelector('input[type="search"]');
  const filters = [...root.querySelectorAll('button[data-category]')];
  const empty = root.querySelector('.blog-empty');
  const count = root.querySelector('.blog-count');
  const pagination = root.querySelector('.blog-pagination');
  const previous = pagination.querySelector('[data-page="previous"]');
  const next = pagination.querySelector('[data-page="next"]');
  const pageSize = 9;
  let category = 'all';
  let page = 1;
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase(document.documentElement.lang).trim();
  function render() {
    const query = normalize(search.value);
    const matches = cards.filter(card => (category === 'all' || card.dataset.category === category) && normalize(card.dataset.search).includes(query));
    const pages = Math.max(1, Math.ceil(matches.length / pageSize));
    page = Math.min(page, pages);
    const visible = new Set(matches.slice((page - 1) * pageSize, page * pageSize));
    cards.forEach(card => { card.hidden = !visible.has(card); });
    empty.hidden = matches.length !== 0;
    count.textContent = `${count.dataset.label}: ${matches.length}`;
    pagination.hidden = pages <= 1;
    previous.disabled = page === 1;
    next.disabled = page === pages;
    pagination.querySelector('span').textContent = `${page} / ${pages}`;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.category;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    page = 1;
    render();
  }));
  search.addEventListener('input', () => { page = 1; render(); });
  function turn(delta) {
    page += delta;
    render();
    const link = cards.find(card => !card.hidden)?.querySelector('a');
    link?.focus();
  }
  previous.addEventListener('click', () => turn(-1));
  next.addEventListener('click', () => turn(1));
  root.querySelector('.blog-tools').hidden = false;
  render();
})();
