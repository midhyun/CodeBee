const bg = document.getElementById('bg')

window.addEventListener('scroll', () => {
  bg.style.opacity = 0 + +window.pageYOffset / 550 + ''
})