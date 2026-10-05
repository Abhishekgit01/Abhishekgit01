// SPDX-License-Identifier: GPL-3.0-only
"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const projects = JSON.parse(
    document.getElementById("project-data").textContent,
  );
  const scene = document.querySelector(".star-map");
  const targets = Array.from(document.querySelectorAll(".project-target"));
  const details = document.getElementById("project-details");
  const hoverInput = window.matchMedia("(hover: hover) and (pointer: fine)");
  scene.classList.add("interactive-ready");
  let current = null;
  let pinned = false;
  let hoverTimer = null;
  let closeTimer = null;

  function positionDetails() {
    if (current === null || details.hidden) return;
    const anchor = current.getBoundingClientRect();
    const bounds = scene.getBoundingClientRect();
    const x = anchor.left - bounds.left + anchor.width / 2;
    const y = anchor.top - bounds.top + anchor.height / 2;
    const panel = details.getBoundingClientRect();
    const left = Math.min(
      Math.max(12, x - panel.width / 2),
      bounds.width - panel.width - 12,
    );
    let top = y - panel.height - 25;
    if (top < 12) top = y + 25;
    top = Math.min(
      Math.max(12, top),
      Math.max(12, bounds.height - panel.height - 12),
    );
    details.style.left = `${left}px`;
    details.style.top = `${top}px`;
  }

  function clearTimers() {
    window.clearTimeout(hoverTimer);
    window.clearTimeout(closeTimer);
  }

  function showDetails(target) {
    clearTimers();
    const project = projects[Number(target.dataset.project)];
    if (!project) throw new Error("The selected repository is missing.");
    targets.forEach((item) =>
      item.setAttribute("aria-expanded", String(item === target)),
    );
    document.getElementById("project-name").textContent = project.name;
    document.getElementById("project-description").textContent =
      project.description;
    document.getElementById("project-link").href = project.url;
    current = target;
    details.hidden = false;
    positionDetails();
  }

  function hideDetails(restoreFocus = false) {
    clearTimers();
    const previous = current;
    current = null;
    pinned = false;
    details.hidden = true;
    targets.forEach((item) => item.setAttribute("aria-expanded", "false"));
    if (restoreFocus && previous) {
      previous.focus();
      // Focus normally opens details; dismiss again after restoring focus.
      details.hidden = true;
      current = null;
      previous.setAttribute("aria-expanded", "false");
    }
  }

  function scheduleClose() {
    window.clearTimeout(hoverTimer);
    if (pinned) return;
    window.clearTimeout(closeTimer);
    closeTimer = window.setTimeout(() => {
      if (
        details.contains(document.activeElement) ||
        current === document.activeElement
      )
        return;
      hideDetails();
    }, 180);
  }

  targets.forEach((target) => {
    target.addEventListener("pointerenter", () => {
      if (!hoverInput.matches || pinned) return;
      const delay = details.hidden ? 150 : 0;
      clearTimers();
      hoverTimer = window.setTimeout(() => showDetails(target), delay);
    });
    target.addEventListener("pointerleave", scheduleClose);
    target.addEventListener("focus", () => {
      pinned = false;
      showDetails(target);
    });
    target.addEventListener("click", () => {
      if (current === target && pinned) hideDetails();
      else {
        showDetails(target);
        pinned = true;
      }
    });
  });

  details.addEventListener("pointerenter", clearTimers);
  details.addEventListener("pointerleave", scheduleClose);
  scene.addEventListener("focusout", () => {
    window.setTimeout(() => {
      if (!scene.contains(document.activeElement)) hideDetails();
    }, 0);
  });
  document
    .querySelector(".close-details")
    .addEventListener("click", () => hideDetails(true));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !details.hidden) hideDetails(true);
  });
  document.addEventListener("pointerdown", (event) => {
    if (
      !details.contains(event.target) &&
      !targets.some((target) => target.contains(event.target))
    ) {
      hideDetails();
    }
  });
  window.addEventListener("resize", positionDetails);
});
