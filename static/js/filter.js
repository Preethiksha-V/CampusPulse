function toggleFilter() {
    document.getElementById("filterPanel").classList.toggle("open");
    document.getElementById("filterOverlay").classList.toggle("show");
}

function applyFilters() {
    const category = document.getElementById("categoryFilter").value;
    const date = document.getElementById("dateFilter").value;
    const timeSlot = document.getElementById("timeFilter").value;

    const cards = document.querySelectorAll(".event-card");

    cards.forEach(card => {
        let visible = true;

        const cardCategory = card.dataset.category;
        const cardDate = card.dataset.date;
        const cardTime = card.dataset.time;

        if (category !== "all" && cardCategory !== category) {
            visible = false;
        }

        if (date && cardDate !== date) {
            visible = false;
        }

        if (timeSlot) {
            if (timeSlot === "Morning" && !cardTime.includes("AM")) visible = false;
            if (timeSlot === "Afternoon" && !cardTime.includes("PM")) visible = false;
            if (timeSlot === "Evening" && !cardTime.includes("PM")) visible = false;
        }

        card.style.display = visible ? "block" : "none";
    });

    toggleFilter(); // close after applying
}
