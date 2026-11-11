// Example data only. These are not real scholarship schemes.
const SCHOLARSHIPS = [
  {
    name: "Merit Excellence Award",
    provider: "Example Education Trust",
    amount: "₹50,000 / year",
    minMarks: 75,
    maxIncome: 800000,
    courses: ["Engineering", "Science", "Commerce"],
    state: null,
    categories: null,
    deadline: "2026-11-20",
  },
  {
    name: "Karnataka Merit Fellowship",
    provider: "Example State Council",
    amount: "₹40,000 / year",
    minMarks: 70,
    maxIncome: 700000,
    courses: ["Engineering", "Science", "Arts", "Commerce"],
    state: "Karnataka",
    categories: null,
    deadline: "2026-11-28",
  },
  {
    name: "Women in Technology Grant",
    provider: "Example Tech Foundation",
    amount: "₹75,000 one time",
    minMarks: 70,
    maxIncome: 600000,
    courses: ["Engineering", "Science"],
    state: null,
    categories: null,
    deadline: "2026-12-05",
  },
  {
    name: "Inclusive Learning Scholarship",
    provider: "Example Community Fund",
    amount: "₹30,000 / year",
    minMarks: 50,
    maxIncome: 250000,
    courses: ["Engineering", "Medicine", "Science", "Commerce", "Arts"],
    state: null,
    categories: ["SC", "ST", "OBC"],
    deadline: "2026-12-15",
  },
  {
    name: "Future Doctors Support",
    provider: "Example Health Trust",
    amount: "₹60,000 / year",
    minMarks: 80,
    maxIncome: 500000,
    courses: ["Medicine"],
    state: null,
    categories: null,
    deadline: "2026-12-30",
  },
];
 
const form = document.getElementById("matcher-form");
const resultsEl = document.getElementById("results");
const titleEl = document.getElementById("results-title");
const subEl = document.getElementById("results-sub");
 
const rupeeShort = (n) => {
  if (n >= 100000) {
    const l = n / 100000;
    return "₹" + (Number.isInteger(l) ? l : l.toFixed(1)) + "L";
  }
  return "₹" + n.toLocaleString("en-IN");
};
 
const formatDate = (iso) =>
  new Date(iso + "T00:00:00").toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
 
const daysUntil = (iso) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.round((new Date(iso + "T00:00:00") - today) / 86400000);
};
 
function getProfile() {
  const marks = parseFloat(document.getElementById("marks").value);
  const income = parseFloat(document.getElementById("income").value);
  return {
    course: document.getElementById("course").value,
    category: document.getElementById("category").value,
    state: document.getElementById("state").value,
    marks: Number.isFinite(marks) ? marks : 0,
    income: Number.isFinite(income) ? income : 0,
  };
}
 
function matches(s, p) {
  if (p.marks < s.minMarks) return false;
  if (p.income > s.maxIncome) return false;
  if (!s.courses.includes(p.course)) return false;
  if (s.state && s.state !== p.state) return false;
  if (s.categories && !s.categories.includes(p.category)) return false;
  return true;
}
 
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
 
function renderCard(s) {
  const days = daysUntil(s.deadline);
  const closed = days < 0;
 
  const card = el("article", "result" + (closed ? " closed" : ""));
  card.append(el("h4", "", s.name));
  card.append(el("p", "provider", s.provider));
  card.append(el("p", "amount", s.amount));
 
  const tags = el("div", "tags");
  tags.append(el("span", "tag", "Min " + s.minMarks + "% marks"));
  tags.append(el("span", "tag", "Income up to " + rupeeShort(s.maxIncome)));
  tags.append(el("span", "tag", s.courses.join(", ")));
  if (s.state) tags.append(el("span", "tag", s.state));
  if (s.categories) tags.append(el("span", "tag", s.categories.join(", ")));
  card.append(tags);
 
  const label = closed ? "Closed " + formatDate(s.deadline) : "Closes " + formatDate(s.deadline);
  card.append(el("p", "deadline" + (!closed && days <= 14 ? " soon" : ""), label));
  return card;
}
 
function render() {
  const profile = getProfile();
  const found = SCHOLARSHIPS.filter((s) => matches(s, profile)).sort((a, b) => {
    const ca = daysUntil(a.deadline) < 0;
    const cb = daysUntil(b.deadline) < 0;
    if (ca !== cb) return ca ? 1 : -1; // open ones first
    return a.deadline.localeCompare(b.deadline);
  });
 
  resultsEl.replaceChildren();
 
  if (found.length === 0) {
    titleEl.textContent = "No matches yet";
    subEl.textContent = "Try a different course, state or income to see more example schemes.";
    resultsEl.append(el("p", "empty", "No example scholarships match this profile."));
    return;
  }
 
  titleEl.textContent =
    found.length + (found.length === 1 ? " scholarship matches" : " scholarships match") + " your profile";
  subEl.textContent = "Sorted by nearest deadline.";
  found.forEach((s) => resultsEl.append(renderCard(s)));
}
 
form.addEventListener("submit", (e) => {
  e.preventDefault();
  render();
});
 
// Mobile nav
const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("nav");
toggle.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
});
nav.addEventListener("click", (e) => {
  if (e.target.tagName === "A") {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }
});
 
render();