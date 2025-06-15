import Cookie from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm';
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
    const info = await get_info();
    if (typeof info !== 'undefined') {
        if (!Object.hasOwn(info, "error")) {
            nav.insertAdjacentHTML( 'beforeend', '<div class="nav-balance" style="color: white; font-weight: bold;">' + info.balance + '$</div>');
            nav.insertAdjacentHTML( 'beforeend', info.username);
        }
    }
});
async function get_info() {
    const token = Cookie.get('token');
    console.log(token)
    if (!token) {
        return null;
    }
    const info = await fetch('/c/user/api.cgi', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'info',
      }),
    })
    .then(response => {
      return response.json();
    })
    .catch(err => console.error('Balance fetch failed:', err));
    return info;
}