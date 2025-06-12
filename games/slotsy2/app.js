function spin() {
  const token = getCookie("token");

  if (!token) {
    alert("Nie jesteś zalogowany!");
    return;
  }

  const payload = {
    action: "bet",
    token: token,
    betvalue: 10
  };

  const symbolElements = [
    document.getElementById("symbol1"),
    document.getElementById("symbol2"),
    document.getElementById("symbol3")
  ];

  const keys = Object.keys(slotMap);

  // Start spinning
  let intervalId = setInterval(() => {
    symbolElements.forEach(el => {
      const randomKey = keys[Math.floor(Math.random() * keys.length)];
      el.textContent = slotMap[randomKey];
    });
  }, 100);

  // Track when spin started
  const spinStartTime = Date.now();

  // Call API
  fetch("https://cebularz7.w.staszic.waw.pl/c/games/slotsy2/api.cgi", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    // Calculate how long the spin lasted
    const elapsed = Date.now() - spinStartTime;
    const remaining = Math.max(0, 1000 - elapsed); // ensure at least 1s of spinning

    // Wait if necessary to show full spin
    setTimeout(() => {
      clearInterval(intervalId);

      // Show final result
      symbolElements[0].textContent = slotMap[data.symbol1];
      symbolElements[1].textContent = slotMap[data.symbol2];
      symbolElements[2].textContent = slotMap[data.symbol3];

      document.getElementById("win").textContent = `${Number(data.winvalue)}$`;
    }, remaining);
  })
  .catch(err => {
    console.error("Error:", err);
    clearInterval(intervalId);
    document.getElementById("win").textContent = "Coś się wysypało!";
  });
}
