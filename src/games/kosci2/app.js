document.getElementById("rollBtn").addEventListener("click", () => {
    const bet = parseInt(document.getElementById("bet").value);

    fetch("api.cgi", {
        method: "POST",
        body: JSON.stringify({
            action: "roll",
            betvalue: bet
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert("Błąd: " + data.error);
            return;
        }
        document.getElementById("dice1").textContent = data.dice1;
        document.getElementById("dice2").textContent = data.dice2;
        document.getElementById("total").textContent = data.total;
        document.getElementById("winvalue").textContent = data.winvalue;
    })
    .catch(err => {
        alert("Błąd połączenia z serwerem.");
        console.error(err);
    });
});
