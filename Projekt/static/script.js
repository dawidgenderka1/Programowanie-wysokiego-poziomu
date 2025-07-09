let first = null, second = null;
let cards = [];
let revealed = [];
let rounds = 0;
let roundsElem = document.getElementById('rounds');
const size = parseInt(document.getElementById('board').dataset.size);
let isProcessing = false;

function createBoard() {
    const board = document.getElementById('board');
    board.innerHTML = '';
    for (let x = 0; x < 4; x++) {
        for (let y = 0; y < 4; y++) {
            const div = document.createElement('div');
            div.classList.add('card');
            div.dataset.x = x;
            div.dataset.y = y;
            div.addEventListener('click', handleClick);
            board.appendChild(div);
        }
    }
}

function updateBoard() {
    document.querySelectorAll('.card').forEach(card => {
        const x = card.dataset.x;
        const y = card.dataset.y;
        if (revealed[x][y]) {
            card.textContent = cards[x][y];
            card.classList.add('revealed');
            card.classList.add('removed');
        } else {
            card.textContent = '';
            card.classList.remove('revealed');
        }
    });
}

function handleClick(e) {
    if (isProcessing) return;

    const card = e.target;
    const x = +card.dataset.x;
    const y = +card.dataset.y;

    if (revealed[x][y] || (first && second)) return;

    if (first && first.x === x && first.y === y) return;

    card.textContent = cards[x][y];
    card.classList.add('revealed');

    if (!first) {
        first = {x, y};
    } else {
        second = {x, y};
        isProcessing = true;
        playMove(first, second);
    }
}


function playMove(a, b) {
    fetch('/play', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x1: a.x, y1: a.y, x2: b.x, y2: b.y})
    })
    .then(res => res.json())
    .then(data => {
        revealed = data.revealed;
        rounds = data.rounds;
        roundsElem.textContent = rounds;

        setTimeout(() => {
            updateBoard();
            first = null;
            second = null;
            isProcessing = false;

            if (data.game_over || checkWin()) {
                const username = prompt("Gratulacje! Wpisz swoje imię:");
                if (username) {
                    fetch('/save_result', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username, rounds})
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert("Wynik zapisany!");
                        window.location.href = "/results";
                    });
                }
            }
        }, 1000);
    });
}



function init() {
    fetch('/get_cards')
        .then(res => res.json())
        .then(data => {
            cards = data.cards;
            revealed = data.revealed;
            createBoard();
            updateBoard();
        });
}

init();
