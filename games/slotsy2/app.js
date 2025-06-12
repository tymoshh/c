// Symbol map with emojis
const slotMap = {
  1: "🍒", // Cherry
  2: "🔔", // Bell
  3: "🍇", // Grape
  4: "🍒", // Cherry
  6: "🍋"  // Lemon
};

// Function to get the cookie
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

// Function to spin the slots
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

  // Get the elements where symbols will be displayed
  const symbolElements = [
    document.getElementById("symbol1"),
    document.getElementById("symbol2"),
    document.getElementById("symbol3")
  ];

  // Disable the spin button to prevent multiple spins
  document.getElementById("spinButton").disabled = true;

  // Start animating symbols
  let intervalId = setInterval(() => {
    symbolElements.forEach(el => {
      // Randomly select a symbol from the slotMap
      const randomSymbol = slotMap[Math.floor(Math.random() * Object.keys(slotMap).length + 1)];
      el.textContent = randomSymbol;
    });
  }, 100); // Change symbol every 100ms

  // Make the API request
  fetch("https://cebularz7.w.staszic.waw.pl/c/games/slotsy2/api.cgi", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    // Stop the animation
    clearInterval(intervalId);

    // Display the final symbols
    symbolElements[0].textContent = slotMap[data.symbol1];
    symbolElements[1].textContent = slotMap[data.symbol2];
    symbolElements[2].textContent = slotMap[data.symbol3];

    // Show the win amount
    document.getElementById("win").textContent = `${Number(data.winvalue)}$`;

    // Re-enable the spin button to allow another spin
    document.getElementById("spinButton").disabled = false;
  })
  .catch(err => {
    console.error("Error:", err);
    clearInterval(intervalId);
    document.getElementById("win").textContent = "Coś się wysypało!";

    // Re-enable the spin button in case of error
    document.getElementById("spinButton").disabled = false;
  });
}

// You can add a reset function if needed to clear the symbols
function resetSlot() {
  const symbolElements = [
    document.getElementById("symbol1"),
    document.getElementById("symbol2"),
    document.getElementById("symbol3")
  ];

  // Reset the symbols to a default state (e.g., empty or initial symbols)
  symbolElements.forEach(el => el.textContent = "🔲"); // Empty block for reset

  // Reset the win value
  document.getElementById("win").textContent = "";
}
