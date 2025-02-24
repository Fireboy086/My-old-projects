// Game Selection Logic
function startRockPaperScissors() {
    document.getElementById('game-selection').style.display = 'none';
    document.getElementById('rps-game').style.display = 'block';
}

function startNumberGuessing() {
    document.getElementById('game-selection').style.display = 'none';
    document.getElementById('number-game').style.display = 'block';
}

/* Rock-Paper-Scissors Game Logic */
let rpsCounts = {};
let rpsTotalClicks = 0;
let rpsWins = 0;
let rpsLosses = 0;
let rpsDraws = 0;
let rpsHistory = [];
let rpsUserMoves = [];

function rpsUserChoice(userMove) {
    rpsTotalClicks++;
    document.getElementById('rps-counter').innerText = `Total Clicks: ${rpsTotalClicks}`;

    let aiMove = rpsMakePrediction();

    let result = getRPSResult(aiMove, userMove);
    if (result === 'Win') {
        rpsWins++;
    } else if (result === 'Loss') {
        rpsLosses++;
    } else {
        rpsDraws++;
    }

    let percentage = ((rpsWins / rpsTotalClicks) * 100).toFixed(2);
    document.getElementById('rps-guess-percentage').innerText = `AI Wins: ${rpsWins}, Losses: ${rpsLosses}, Draws: ${rpsDraws} (Win Rate: ${percentage}%)`;

    rpsHistory.push({
        index: rpsHistory.length + 1,
        user: userMove,
        ai: aiMove,
        result: result
    });

    rpsUserMoves.push(userMove);

    // Flash effect
    flashScreen(result);

    // Update history if visible
    if (document.getElementById('rps-history').style.display !== 'none') {
        updateRPSHistory();
    }
}

function rpsMakePrediction() {
    let moves = ['rock', 'paper', 'scissors'];

    if (rpsUserMoves.length >= 5) {
        // Use patterns of the last five moves
        let lastFive = rpsUserMoves.slice(-5).join(',');
        let patternCounts = {};

        for (let i = 0; i <= rpsUserMoves.length - 6; i++) {
            let pattern = rpsUserMoves.slice(i, i + 5).join(',');
            let nextMove = rpsUserMoves[i + 5];
            if (pattern === lastFive) {
                patternCounts[nextMove] = (patternCounts[nextMove] || 0) + 1;
            }
        }

        let predictedUserMove = null;
        let maxCount = 0;
        for (let move in patternCounts) {
            if (patternCounts[move] > maxCount) {
                maxCount = patternCounts[move];
                predictedUserMove = move;
            }
        }

        if (predictedUserMove !== null) {
            return getAIMove(predictedUserMove);
        }
    }

    // If not enough data for last five moves or no pattern found, use frequency analysis
    if (rpsUserMoves.length > 0) {
        let frequency = {};
        for (let i = 0; i < rpsUserMoves.length; i++) {
            let move = rpsUserMoves[i];
            frequency[move] = (frequency[move] || 0) + 1;
        }
        let predictedUserMove = null;
        let maxCount = 0;
        for (let move in frequency) {
            if (frequency[move] > maxCount) {
                maxCount = frequency[move];
                predictedUserMove = move;
            }
        }
        if (predictedUserMove !== null) {
            return getAIMove(predictedUserMove);
        }
    }

    // Random choice
    return moves[Math.floor(Math.random() * 3)];
}

function getAIMove(predictedUserMove) {
    // AI plays the move that beats the predicted user move
    if (predictedUserMove === 'rock') {
        return 'paper';
    } else if (predictedUserMove === 'paper') {
        return 'scissors';
    } else if (predictedUserMove === 'scissors') {
        return 'rock';
    } else {
        // If prediction failed, choose randomly
        let moves = ['rock', 'paper', 'scissors'];
        return moves[Math.floor(Math.random() * 3)];
    }
}

function getRPSResult(aiMove, userMove) {
    if (aiMove === userMove) {
        return 'Draw';
    } else if (
        (aiMove === 'rock' && userMove === 'scissors') ||
        (aiMove === 'paper' && userMove === 'rock') ||
        (aiMove === 'scissors' && userMove === 'paper')
    ) {
        return 'Win';
    } else {
        return 'Loss';
    }
}

function flashScreen(result) {
    if (result === 'Win') {
        document.body.classList.add('flash');
    } else if (result === 'Loss') {
        document.body.classList.add('flash-wrong');
    } else {
        document.body.classList.add('flash-draw');
    }
    setTimeout(() => {
        document.body.classList.remove('flash', 'flash-wrong', 'flash-draw');
    }, 1000);
}

function toggleRPSHistory() {
    let historyDiv = document.getElementById('rps-history');
    if (historyDiv.style.display === 'none') {
        historyDiv.style.display = 'block';
        updateRPSHistory();
    } else {
        historyDiv.style.display = 'none';
    }
}

function updateRPSHistory() {
    let historyList = document.getElementById('rps-history-list');
    historyList.innerHTML = '';
    for (let i = 0; i < rpsHistory.length; i++) {
        let entry = rpsHistory[i];
        let row = document.createElement('tr');
        let resultClass = entry.result.toLowerCase();
        row.classList.add(resultClass);

        let cellIndex = document.createElement('td');
        cellIndex.innerText = entry.index;
        row.appendChild(cellIndex);

        let cellUser = document.createElement('td');
        cellUser.innerText = entry.user;
        row.appendChild(cellUser);

        let cellAI = document.createElement('td');
        cellAI.innerText = entry.ai;
        row.appendChild(cellAI);

        let cellResult = document.createElement('td');
        cellResult.innerText = entry.result;
        row.appendChild(cellResult);

        historyList.appendChild(row);
    }
}

function resetRPSGame() {
    rpsCounts = {};
    rpsTotalClicks = 0;
    rpsWins = 0;
    rpsLosses = 0;
    rpsDraws = 0;
    rpsHistory = [];
    rpsUserMoves = [];
    document.getElementById('rps-counter').innerText = `Total Clicks: ${rpsTotalClicks}`;
    document.getElementById('rps-guess-percentage').innerText = '';
    document.getElementById('rps-history-list').innerHTML = '';
    document.getElementById('rps-history').style.display = 'none';
    // Return to game selection
    document.getElementById('rps-game').style.display = 'none';
    document.getElementById('game-selection').style.display = 'block';
}

/* Number Guessing Game Logic */
let totalInputs = 0;
let correctGuesses = 0;
let totalGuesses = 0;

let history = [];
let inputHistory = [];
let aiPrediction = null;

function submitInput() {
    let userInput = parseInt(document.getElementById('user-input').value);
    if (isNaN(userInput) || userInput < 1 || userInput > 100) {
        alert('Please enter a valid number between 1 and 100.');
        return;
    }

    totalInputs++;
    document.getElementById('counter').innerText = `Total Inputs: ${totalInputs}`;

    aiPrediction = makePrediction();

    let isCorrect = (aiPrediction === userInput);
    totalGuesses++;
    if (isCorrect) {
        correctGuesses++;
    }

    let percentage = ((correctGuesses / totalGuesses) * 100).toFixed(2);
    document.getElementById('guess-percentage').innerText = `AI guessed correctly ${correctGuesses} out of ${totalGuesses} times (${percentage}%)`;

    history.push({
        index: history.length + 1,
        input: userInput,
        ai: aiPrediction,
        difference: Math.abs(userInput - aiPrediction),
        correct: isCorrect,
        timestamp: new Date()
    });

    inputHistory.push(userInput);
    document.getElementById('user-input').value = '';

    // Update history if it's visible
    if (document.getElementById('history').style.display !== 'none') {
        updateHistory();
    }
}

function makePrediction() {
    if (inputHistory.length >= 5) {
        // Use patterns of the last five inputs
        let lastFive = inputHistory.slice(-5).join(',');
        let patternCounts = {};

        for (let i = 0; i <= inputHistory.length - 6; i++) {
            let pattern = inputHistory.slice(i, i + 5).join(',');
            let nextNumber = inputHistory[i + 5];
            if (pattern === lastFive) {
                patternCounts[nextNumber] = (patternCounts[nextNumber] || 0) + 1;
            }
        }

        let prediction = null;
        let maxCount = 0;
        for (let number in patternCounts) {
            if (patternCounts[number] > maxCount) {
                maxCount = patternCounts[number];
                prediction = parseInt(number);
            }
        }

        if (prediction !== null) {
            return prediction;
        }
    }

    // If not enough data for last five inputs or no pattern found, use frequency analysis
    if (inputHistory.length > 0) {
        let frequency = {};
        for (let i = 0; i < inputHistory.length; i++) {
            let number = inputHistory[i];
            frequency[number] = (frequency[number] || 0) + 1;
        }
        let prediction = null;
        let maxCount = 0;
        for (let number in frequency) {
            if (frequency[number] > maxCount) {
                maxCount = frequency[number];
                prediction = parseInt(number);
            }
        }
        if (prediction !== null) {
            return prediction;
        }
    }

    // If no data, return a random number between 1 and 100
    return Math.floor(Math.random() * 100) + 1;
}

function toggleHistory() {
    let historyDiv = document.getElementById('history');
    if (historyDiv.style.display === 'none') {
        historyDiv.style.display = 'block';
        updateHistory();
    } else {
        historyDiv.style.display = 'none';
    }
}

function updateHistory() {
    let historyList = document.getElementById('history-list');
    historyList.innerHTML = '';

    // Get selected sort option
    let sortOption = document.getElementById('sort-select').value;

    // Copy history array to avoid mutating original
    let sortedHistory = history.slice();

    // Sort based on selected option
    if (sortOption === 'latest') {
        // Latest first (default)
        sortedHistory.sort((a, b) => b.timestamp - a.timestamp);
    } else if (sortOption === 'oldest') {
        // Oldest first
        sortedHistory.sort((a, b) => a.timestamp - b.timestamp);
    } else if (sortOption === 'correct') {
        // Correct first
        sortedHistory.sort((a, b) => {
            if (a.correct === b.correct) {
                return b.timestamp - a.timestamp; // Then sort by latest
            }
            return (a.correct === true) ? -1 : 1;
        });
    } else if (sortOption === 'closest') {
        // Closest difference first
        sortedHistory.sort((a, b) => a.difference - b.difference);
    }

    for (let i = 0; i < sortedHistory.length; i++) {
        let entry = sortedHistory[i];
        let row = document.createElement('tr');
        row.classList.add(entry.correct ? 'correct' : 'incorrect');

        let cellIndex = document.createElement('td');
        cellIndex.innerText = entry.index;
        row.appendChild(cellIndex);

        let cellInput = document.createElement('td');
        cellInput.innerText = entry.input;
        row.appendChild(cellInput);

        let cellAI = document.createElement('td');
        cellAI.innerText = entry.ai;
        row.appendChild(cellAI);

        let cellDifference = document.createElement('td');
        cellDifference.innerText = entry.difference;
        row.appendChild(cellDifference);

        let cellResult = document.createElement('td');
        cellResult.innerText = entry.correct ? 'Correct' : 'Incorrect';
        row.appendChild(cellResult);

        historyList.appendChild(row);
    }
}

function resetGame() {
    totalInputs = 0;
    correctGuesses = 0;
    totalGuesses = 0;
    history = [];
    inputHistory = [];
    aiPrediction = null;
    document.getElementById('counter').innerText = `Total Inputs: ${totalInputs}`;
    document.getElementById('guess-percentage').innerText = '';
    document.getElementById('history-list').innerHTML = '';
    document.getElementById('history').style.display = 'none';
    document.getElementById('user-input').value = '';
    document.getElementById('sort-select').value = 'latest';
    // Return to game selection
    document.getElementById('number-game').style.display = 'none';
    document.getElementById('game-selection').style.display = 'block';
}

document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        submitInput();
    }
});
