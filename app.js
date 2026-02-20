document.addEventListener('DOMContentLoaded', () => {
    let stockData = {};
    let currentRenderIndex = 0;
    let renderInterval = null;
    const CHUNK_SIZE = 10;

    const tableBody = document.getElementById('table-body');
    const themeTitle = document.getElementById('current-theme-title');
    const navButtons = document.querySelectorAll('.nav-btn');
    const timeDisplay = document.getElementById('data-retrieval-time');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Initialization using the global STOCK_DATA from data.js
    if (typeof STOCK_DATA !== 'undefined') {
        stockData = STOCK_DATA.rankings;
        timeDisplay.textContent = `データ取得時間: ${STOCK_DATA.retrieval_time}`;
        renderRanking('値上がり率');
    } else {
        console.error('STOCK_DATA is not defined. Make sure data.js is loaded.');
        tableBody.innerHTML = '<tr><td colspan="9" style="text-align:center;">データの読み込みに失敗しました。</td></tr>';
    }

    // Sidebar navigation logic
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const theme = btn.getAttribute('data-theme');
            renderRanking(theme);
        });
    });

    /**
     * Renders the ranking data in chunks to keep the UI responsive.
     */
    function renderRanking(theme) {
        if (!stockData[theme]) {
            tableBody.innerHTML = '<tr><td colspan="9" style="text-align:center;">データがありません。</td></tr>';
            return;
        }

        // Reset state for new theme
        if (renderInterval) clearInterval(renderInterval);
        themeTitle.textContent = theme;
        tableBody.innerHTML = '';
        currentRenderIndex = 0;

        const data = stockData[theme];
        const totalItems = data.length;

        // Function to render a single chunk
        const renderChunk = () => {
            const end = Math.min(currentRenderIndex + CHUNK_SIZE, totalItems);
            const fragment = document.createDocumentFragment();

            for (let i = currentRenderIndex; i < end; i++) {
                const stock = data[i];
                const tr = document.createElement('tr');

                // Styling for price change
                const changeStr = stock['change_pct'] ? String(stock['change_pct']) : (stock['change'] || '');
                const changeClass = changeStr.includes('+') ? 'up' : changeStr.includes('-') ? 'down' : '';

                // Handle different data formats from extraction
                const yieldVal = stock['yield'] || stock['配当利回り'] || '-';
                const perVal = stock['per'] || stock['PER'] || '-';
                const pbrVal = stock['pbr'] || stock['PBR'] || '-';
                const priceVal = stock['price'] || stock['株価'] || '-';
                const volVal = stock['volume'] || stock['出来高'] || '-';

                tr.innerHTML = `
                    <td class="rank-cell">${stock['rank'] || (i + 1)}</td>
                    <td class="code-cell">${stock['code'] || stock['コード']}</td>
                    <td class="name-cell">${stock['name'] || stock['銘柄名']}</td>
                    <td class="price-cell num-cell">${priceVal}</td>
                    <td class="change-cell num-cell ${changeClass}">${changeStr}</td>
                    <td class="yield-cell num-cell">${yieldVal}</td>
                    <td class="num-cell">${perVal}</td>
                    <td class="num-cell">${pbrVal}</td>
                    <td class="num-cell">${volVal}</td>
                `;
                fragment.appendChild(tr);
            }

            tableBody.appendChild(fragment);
            currentRenderIndex = end;

            if (currentRenderIndex >= totalItems) {
                clearInterval(renderInterval);
                loadingIndicator.style.display = 'none';
            } else {
                loadingIndicator.style.display = 'block';
            }
        };

        // Render first chunk immediately
        renderChunk();

        // If more items remain, render them at intervals
        if (currentRenderIndex < totalItems) {
            renderInterval = setInterval(renderChunk, 50); // Fast but async
        }

        // Component animation
        const card = document.querySelector('.table-card');
        card.style.animation = 'none';
        card.offsetHeight;
        card.style.animation = 'fadeInUp 0.6s ease-out';
    }
});
