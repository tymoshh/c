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

// Main slot spin function with 850ms cooldown on the button with id "zakrec"
function spin() {
  const spinButton = document.getElementById("zakrec");
  if (!spinButton) {
    console.error("Spin button with id 'zakrec' not found");
    return;
  }

  // Disable button immediately to prevent spamming
  spinButton.disabled = true;

  // Re-enable after cooldown
  setTimeout(() => {
    spinButton.disabled = false;
  }, 850);

  const token = getCookie("token");
  if (!token) {
    Swal.fire({
      icon: "error",
      title: "nie jestes zalogowany",
      confirmButtonText: "cholibka"
    });
    return;
  }

  const payload = {
    token: token,
    bet_value: 10
  };

  const symbolElements = [
    document.getElementById("symbol1"),
    document.getElementById("symbol2"),
    document.getElementById("symbol3")
  ];

  const keys = Object.keys(slotMap);

  // Start spinning animation (random emojis)
  const intervalId = setInterval(() => {
    symbolElements.forEach(el => {
      const randomKey = keys[Math.floor(Math.random() * keys.length)];
      el.textContent = slotMap[randomKey];
    });
  }, 100);

  let result = null;
  let requestFailed = false;

  fetch("/c/games/slotsy2/api.cgi", {
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

  // After 800ms, stop animation and show results
  setTimeout(() => {
    clearInterval(intervalId);

    if (requestFailed || !result || Object.hasOwn(result, "error")) {
      Swal.fire({
        icon: "error",
        title: result.error || "cos sie sypie",
        confirmButtonText: "klops"
      });
      return;
    }

    symbolElements[0].textContent = getSymbol(result.symbols[0]);
    symbolElements[1].textContent = getSymbol(result.symbols[1]);
    symbolElements[2].textContent = getSymbol(result.symbols[2]);

    const winAmount = Number(result.winvalue);
    var navBalanceElement = document.querySelector('.nav-balance');
    var currentValue = parseInt(navBalanceElement.textContent);
    var newValue = currentValue + winAmount - 10;
    navBalanceElement.textContent = newValue.toString() + "$";

    if (winAmount > 0) {
      Swal.fire({
        icon: "success",
        title: `${winAmount}$`,
        showConfirmButton: true,
        confirmButtonText: "kozak"
      });
    }
  }, 800);
}
