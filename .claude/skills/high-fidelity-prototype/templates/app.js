const root = () => document.getElementById('modal-root');

async function openModal(name) {
  const html = await (await fetch(`${name}.html`)).text();
  root().innerHTML = html;
}

function closeModal() { root().innerHTML = ''; }

document.addEventListener('click', (e) => {
  const el = e.target.closest('[data-go],[data-modal],[data-close]');
  if (!el) return;
  if (el.dataset.close !== undefined) return closeModal();
  if (el.dataset.modal) return openModal(el.dataset.modal);
  if (el.dataset.go) location.href = `${el.dataset.go}.html`;
});
