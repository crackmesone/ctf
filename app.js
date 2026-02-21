// Apply configuration on page load
document.addEventListener('DOMContentLoaded', async () => {
    const liveBanner = document.getElementById('live-banner');
    const finishedBanner = document.getElementById('finished-banner');
    const hallOfFame = document.getElementById('hall-of-fame');

    if (CTF_CONFIG.isEventOver) {
        // Event is over - show finished state
        liveBanner.classList.add('hidden');
        finishedBanner.classList.remove('hidden');
        hallOfFame.classList.remove('hidden');

        // Load scoreboard
        await loadScoreboard();
    } else {
        // Event is live
        liveBanner.classList.remove('hidden');
        finishedBanner.classList.add('hidden');
        hallOfFame.classList.add('hidden');
    }
});

async function loadScoreboard() {
    const tbody = document.getElementById('scoreboard-body');

    try {
        const response = await fetch('scoreboard.json');
        if (!response.ok) {
            throw new Error('Scoreboard not found');
        }

        const data = await response.json();
        const players = data.standings || data;

        tbody.innerHTML = players.map((player, index) => {
            const rank = player.rank || index + 1;
            const name = player.name || player.team || player.player || 'Unknown';
            const score = player.score || player.points || 0;

            let rankClass = '';
            if (rank === 1) rankClass = 'rank-1';
            else if (rank === 2) rankClass = 'rank-2';
            else if (rank === 3) rankClass = 'rank-3';

            return `
                <tr class="${rankClass}">
                    <td>${rank}</td>
                    <td>${escapeHtml(name)}</td>
                    <td>${score}</td>
                </tr>
            `;
        }).join('');

    } catch (error) {
        tbody.innerHTML = `
            <tr>
                <td colspan="3" style="text-align: center; color: #888;">
                    Scoreboard data not yet available
                </td>
            </tr>
        `;
        console.log('Scoreboard not loaded:', error.message);
    }
}

// Prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
