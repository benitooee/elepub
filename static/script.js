
const tabs = document.querySelectorAll(".tab");
const cards = document.querySelectorAll(".grid .card");
const grid = document.querySelector(".grid");
const adoptGraphs = document.querySelector(".adopt-graphs");

/**
 * Show / hide the Adopt Survey graphs block
 */
function toggleAdoptGraphs(filter) {
  if (!adoptGraphs) return;
  if (filter === "adopt" || filter === "adopt survey") {
    adoptGraphs.style.display = "block";
  } else {
    adoptGraphs.style.display = "none";
  }
}

/**
 * Filter portfolio cards based on type
 *   - "pets"    → show only PETS cards
 *   - "people" → show only PEOPLE cards + tall layout
 *   - "adopt"  → hide all cards, show graphs
 */
function applyFilter(filter) {
  cards.forEach(card => {
    const type = card.dataset.type;
    card.style.display = type === filter ? "block" : "none";
  });

  // Toggle vertical layout for 'people'
  if (filter === "people") {
    grid.classList.add("people-mode");
  } else {
    grid.classList.remove("people-mode");
  }

  // Show or hide graphs
  toggleAdoptGraphs(filter);
}

/* -------- Tabs Click Handling -------- */
tabs?.forEach(tab => {
  tab.addEventListener("click", () => {
    tabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");

    const filter = tab.dataset.filter || tab.textContent.trim().toLowerCase();
    applyFilter(filter);
  });
});


window.addEventListener("DOMContentLoaded", () => {
  const activeTab = document.querySelector(".tab.active");
  const filter = activeTab
    ? activeTab.dataset.filter || activeTab.textContent.trim().toLowerCase()
    : "pets";

  applyFilter(filter);
});


const heroPhoto = document.querySelector(".hero-photo");
const dots = document.querySelectorAll(".carousel-dots .dot");

if (heroPhoto && dots.length) {
  const heroImages = [
    "static/pets/cat1.jpg",
    "static/pets/dog7.jpg",
    "static/pets/dog8.jpg"
  ];
  let hIndex = 0;

  setInterval(() => {
    hIndex = (hIndex + 1) % heroImages.length;
    heroPhoto.style.backgroundImage = `url("${heroImages[hIndex]}")`;
    dots.forEach(d => d.classList.remove("active"));
    dots[hIndex].classList.add("active");
  }, 3500);
}

/* -------- Smooth Scrolling for Anchor Links -------- */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    const href = this.getAttribute("href");
    if (!href || href === "#") return; // allow normal click on # or empty

    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});

function applyFilter(filter) {
  cards.forEach(card => {
    const type = card.dataset.type;
    card.style.display = type === filter ? "block" : "none";
  });

  // PEOPLE layout (tall)
  if (filter === "people") {
    grid.classList.add("people-mode");
  } else {
    grid.classList.remove("people-mode");
  }

  // PET layout (3x2)
  if (filter === "pets") {
    grid.classList.add("pet-mode");
  } else {
    grid.classList.remove("pet-mode");
  }

  // ADOPT SURVEY graphs
  toggleAdoptGraphs(filter);
}
