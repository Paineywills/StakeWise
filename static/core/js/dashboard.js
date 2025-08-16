// ===== PROFILE MENU TOGGLE =====
document.addEventListener("DOMContentLoaded", function () {
    const profileBtn = document.querySelector("#profile-btn");
    const profileMenu = document.querySelector("#profile-menu");

    if (profileBtn && profileMenu) {
        profileBtn.addEventListener("click", () => {
            profileMenu.classList.toggle("show");
        });

        document.addEventListener("click", (e) => {
            if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
                profileMenu.classList.remove("show");
            }
        });
    }

    // ===== BET SLIP FUNCTIONALITY =====
    const betSlipList = document.querySelector("#bet-slip-list");
    const clearSlipBtn = document.querySelector("#clear-slip");
    const betForm = document.querySelector("#bet-form");

    function addBetToSlip(eventName, marketName, outcomeName, odds) {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <strong>${eventName}</strong><br>
            ${marketName}: ${outcomeName} @ <span class="odds">${odds}</span>
        `;
        betSlipList.appendChild(listItem);
    }

    document.querySelectorAll(".market button").forEach(button => {
        button.addEventListener("click", () => {
            const eventName = button.dataset.event;
            const marketName = button.dataset.market;
            const outcomeName = button.dataset.outcome;
            const odds = button.dataset.odds;
            addBetToSlip(eventName, marketName, outcomeName, odds);
        });
    });

    if (clearSlipBtn) {
        clearSlipBtn.addEventListener("click", () => {
            betSlipList.innerHTML = "";
        });
    }

    if (betForm) {
        betForm.addEventListener("submit", (e) => {
            e.preventDefault();
            alert("Bet submitted! (You can hook this to Django via AJAX)");
            betSlipList.innerHTML = "";
        });
    }
});
