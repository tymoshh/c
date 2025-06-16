document.getElementById("rollBtn").addEventListener("click", () => {
    const bet = parseInt(document.getElementById("bet").value);

    fetch("api.cgi", {
        method: "POST",
        body: JSON.stringify({
            action: "roll",
            bet_value: bet
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert("Błąd: " + data.error);
            return;
        }
        document.getElementById("dice1").textContent = data.dice[0];
        document.getElementById("dice2").textContent = data.dice[1];
        document.getElementById("total").textContent = data.dice[0] + data.dice[1];
        document.getElementById("winvalue").textContent = data.win;
    })
    .catch(err => {
        alert("Błąd połączenia z serwerem.");
        console.error(err);
    });
});
