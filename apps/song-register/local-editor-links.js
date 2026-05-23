(() => {
  if (document.querySelector('script[data-song-register-atoms="true"]')) return;
  const s = document.createElement('script');
  s.src = 'app-atoms.js';
  s.dataset.songRegisterAtoms = 'true';
  document.body.appendChild(s);
})();
