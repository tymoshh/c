// Map server symbol names to emojis
const slotMap = {
  Seven: "7️⃣",
  Bell: "🔔",
  Grape: "🍇",
  Cherry: "🍒",
  Lemon: "🍋"
};

// Fallback in case of unknown symbol
function getSymbol(name) {
  return slotMap[name] || "❓";
}

// Read cookie by name
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

// Main slot spin function
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

  const keys = Object.keys(slotMap); // ["Seven", "Bell", "Grape", "Cherry", "Lemon"]

  // Start fake spinning animation
  const intervalId = setInterval(() => {
    symbolElements.forEach(el => {
      const randomKey = keys[Math.floor(Math.random() * keys.length)];
      el.textContent = slotMap[randomKey];
    });
  }, 100);

  // Start request immediately
  let result = null;
  let requestFailed = false;

  fetch("https://cebularz7.w.staszic.waw.pl/c/games/slotsy2/api.cgi", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      result = data;
    })
    .catch(err => {
      console.error("Error:", err);
      requestFailed = true;
    });

  // Stop animation after 1.5 seconds and show result
  setTimeout(() => {
    clearInterval(intervalId);

    if (requestFailed || !result) {
      document.getElementById("win").textContent = "Coś się wysypało!";
      return;
    }

    symbolElements[0].textContent = getSymbol(result.symbol1);
    symbolElements[1].textContent = getSymbol(result.symbol2);
    symbolElements[2].textContent = getSymbol(result.symbol3);
    document.getElementById("win").textContent = `${Number(result.winvalue)}$`;
  }, 1500);
}
