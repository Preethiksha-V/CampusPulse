function selectCard(card) {
    document.querySelectorAll('.category-card').forEach(c => {
        c.classList.remove('active');
    });
    card.classList.add('active');
}
