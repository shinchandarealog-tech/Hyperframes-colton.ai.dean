// Loads each video only when it scrolls into view. If the file isn't there yet,
// the pink/sage placeholder stays, so the page never looks broken.
(function () {
  const slots = document.querySelectorAll(".vid[data-src]");
  const hoverable = window.matchMedia("(hover: hover)").matches;

  function load(slot) {
    if (slot.dataset.loaded) return;
    slot.dataset.loaded = "1";
    const v = document.createElement("video");
    v.muted = true; v.loop = true; v.playsInline = true; v.preload = "metadata";
    v.setAttribute("muted", ""); v.setAttribute("playsinline", "");
    if (slot.dataset.poster) v.poster = slot.dataset.poster;
    v.addEventListener("loadeddata", () => {
      slot.classList.add("has-video");
      if (slot.hasAttribute("data-autoplay")) v.play().catch(() => {});
    });
    v.addEventListener("error", () => v.remove(), true);
    v.src = slot.dataset.src;
    slot.prepend(v);
    if (hoverable && !slot.hasAttribute("data-autoplay")) {
      slot.addEventListener("mouseenter", () => v.play().catch(() => {}));
      slot.addEventListener("mouseleave", () => { v.pause(); });
    }
  }

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { load(e.target); io.unobserve(e.target); } });
    }, { rootMargin: "200px" });
    slots.forEach((s) => io.observe(s));
  } else {
    slots.forEach(load);
  }

  // Click a card to watch it bigger, with sound.
  const box = document.getElementById("lightbox");
  const big = document.getElementById("lightbox-video");
  function close() { big.pause(); big.removeAttribute("src"); big.load(); box.hidden = true; }
  document.querySelectorAll("button.vid").forEach((b) => {
    b.addEventListener("click", () => {
      if (!b.classList.contains("has-video")) return; // nothing to play yet
      big.src = b.dataset.src;
      box.hidden = false;
      big.play().catch(() => {});
    });
  });
  box.addEventListener("click", (e) => { if (e.target === box || e.target.closest(".close")) close(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !box.hidden) close(); });

  // Copy email button
  const copyBtn = document.getElementById("copy-email");
  copyBtn.addEventListener("click", () => {
    const done = () => { copyBtn.textContent = "Copied ♡"; setTimeout(() => (copyBtn.textContent = "Copy email"), 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText("arya@gmail.com").then(done, () => {});
  });
})();
