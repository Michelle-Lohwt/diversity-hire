const menuButton = document.getElementById('menu-button');
const dropdownMenu = document.getElementById('dropdown-menu');
let isMenuOpen = false;

menuButton.addEventListener('click', () => {
  isMenuOpen = !isMenuOpen;
  dropdownMenu.classList.toggle('hidden');
  menuButton.setAttribute('aria-expanded', isMenuOpen);
});

document.addEventListener('click', (event) => {
  const target = event.target;
  if (!dropdownMenu.contains(target) && !menuButton.contains(target)) {
    isMenuOpen = false;
    dropdownMenu.classList.add('hidden');
    menuButton.setAttribute('aria-expanded', false);
  }
});