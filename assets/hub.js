(function () {
  'use strict';

  const STORAGE_KEY = 'jd-hub-active-tab';
  const DEFAULT_TAB = 'registers';

  const tabs = Array.from(document.querySelectorAll('.tab'));
  const panels = Array.from(document.querySelectorAll('.panel'));
  const tablist = document.querySelector('[role="tablist"]');

  function readStored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (_) {
      return null;
    }
  }

  function writeStored(name) {
    try {
      localStorage.setItem(STORAGE_KEY, name);
    } catch (_) {}
  }

  function setActiveTab(name, opts) {
    const focus = !!(opts && opts.focus);
    const persist = !opts || opts.persist !== false;

    let matched = false;
    tabs.forEach(function (tab) {
      const active = tab.dataset.tab === name;
      if (active) matched = true;
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
      tab.tabIndex = active ? 0 : -1;
      if (focus && active) tab.focus();
    });
    if (!matched) return;

    panels.forEach(function (panel) {
      if (panel.dataset.panel === name) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', '');
      }
    });

    if (persist) writeStored(name);
  }

  function initTabs() {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        setActiveTab(tab.dataset.tab);
      });
    });

    if (tablist) {
      tablist.addEventListener('keydown', function (e) {
        const currentIndex = tabs.findIndex(function (t) {
          return t.getAttribute('aria-selected') === 'true';
        });
        let nextIndex = -1;
        switch (e.key) {
          case 'ArrowRight':
          case 'ArrowDown':
            nextIndex = (currentIndex + 1) % tabs.length;
            break;
          case 'ArrowLeft':
          case 'ArrowUp':
            nextIndex = (currentIndex - 1 + tabs.length) % tabs.length;
            break;
          case 'Home':
            nextIndex = 0;
            break;
          case 'End':
            nextIndex = tabs.length - 1;
            break;
        }
        if (nextIndex >= 0) {
          e.preventDefault();
          setActiveTab(tabs[nextIndex].dataset.tab, { focus: true });
        }
      });
    }

    const stored = readStored();
    const valid = stored && tabs.some(function (t) { return t.dataset.tab === stored; });
    setActiveTab(valid ? stored : DEFAULT_TAB, { persist: false });
  }

  function initCards() {
    const toggles = document.querySelectorAll('.card-toggle:not(.is-static)');
    toggles.forEach(function (toggle) {
      toggle.addEventListener('click', function () {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        const next = !expanded;
        toggle.setAttribute('aria-expanded', next ? 'true' : 'false');
        const detailsId = toggle.getAttribute('aria-controls');
        if (!detailsId) return;
        const details = document.getElementById(detailsId);
        if (!details) return;
        if (next) {
          details.removeAttribute('hidden');
        } else {
          details.setAttribute('hidden', '');
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initTabs();
      initCards();
    });
  } else {
    initTabs();
    initCards();
  }
})();
