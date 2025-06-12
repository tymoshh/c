function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }
  
  function spin() {
    const token = getCookie("token");
  
    if (!token) {
      alert("No token found in cookies.");
      return;
    }
  
    const payload = {
      action: "bet",
      token: token,
      betvalue: 10
    };
  
    fetch("https://cebularz7.w.staszic.waw.pl/c/games/slotsy2/api.cgi", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("symbols").textContent =
        `${data.symbol1} | ${data.symbol2} | ${data.symbol3}`;
      document.getElementById("win").textContent =
        `You won: ${data.win}`;
    })
    .catch(err => {
      console.error("Error:", err);
      document.getElementById("win").textContent = "An error occurred.";
    });
  }
  