import Cookie from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm'
const nav = document.getElementsByTagName("nav")[0];
document.addEventListener('DOMContentLoaded', async () => {
  fetch('/c/navbar/navbar.html')
    .then(response => {
      return response.text();
    })
    .then(html => {
      nav.innerHTML = html;
    })
    .catch(err => console.error('Navbar fetch failed:', err));
    const bal = await getBal();
    if (typeof bal !== 'undefined') {
        nav.insertAdjacentHTML( 'beforeend', '<div class="nav-balance" style="color: white; margin-left: auto; padding-right: 15px; font-weight: bold;">' + bal + '$</div>');
    }
});
async function getBal() {
    const token = Cookie.get('token');
    console.log(token)
    if (!token) {
        return null;
    }
    const bal = await fetch('/c/user/api.cgi', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'getbal',
        token: token,
      }),
    })
    .then(response => {
      return response.json();
    })
    .then(data => {
      return data.balance;
    })
    .catch(err => console.error('Balance fetch failed:', err));
    return bal;
}