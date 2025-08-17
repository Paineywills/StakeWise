// dashboard.js

// -------------------------
// Profile Dropdown Handler
// -------------------------
const profileBtn = document.getElementById('profile-btn');
const profileMenu = document.getElementById('profile-menu');

profileBtn.addEventListener('click', () => {
  profileMenu.classList.toggle('hidden');
});

document.addEventListener('click', (e) => {
  if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
    profileMenu.classList.add('hidden');
  }
});

// -------------------------
// Picture Slider
// -------------------------
const slides = document.querySelector('#picture-slider .slides');
if (slides) {
  const totalSlides = slides.children.length;
  let index = 0;

  setInterval(() => {
    index = (index + 1) % totalSlides;
    slides.style.transform = `translateX(-${index * 100}%)`;
  }, 5000);
}

// -------------------------
// Game Tabs Switching
// -------------------------
const gameTabs = document.querySelectorAll('.game-tab');
const gameList = document.getElementById('game-list');

gameTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    // Remove active class from all tabs
    gameTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');

    // Optional: Load different game categories
    // Here we just log for now; you can fetch via AJAX or update innerHTML
    console.log(`Selected tab: ${tab.textContent}`);
    // Example: gameList.innerHTML = renderGames(tab.textContent);
  });
});

// -------------------------
// Bet Slip Functionality
// -------------------------
const betForm = document.getElementById('bet-form');
const betSlipList = document.getElementById('bet-slip-list');
const clearSlipBtn = document.getElementById('clear-slip');

if (betForm) {
  betForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const stake = betForm.stake.value;
    if (!stake) return;
    const li = document.createElement('li');
    li.textContent = `Stake: ${stake}`;
    betSlipList.appendChild(li);
    betForm.reset();
  });
}

if (clearSlipBtn) {
  clearSlipBtn.addEventListener('click', () => {
    betSlipList.innerHTML = '';
  });
}

// -------------------------
// Betting Events (optional dynamic adding)
// -------------------------
const marketButtons = document.querySelectorAll('#betting-panel .market button');
marketButtons.forEach(button => {
  button.addEventListener('click', () => {
    const event = button.dataset.event;
    const market = button.dataset.market;
    const outcome = button.dataset.outcome;
    const odds = button.dataset.odds;

    const li = document.createElement('li');
    li.textContent = `${event} - ${market}: ${outcome} @ ${odds}`;
    betSlipList.appendChild(li);
  });
});
