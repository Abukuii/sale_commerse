window.addEventListener('DOMContentLoaded', () => {

    const header = document.querySelector("header");
    const hamburgerBtn = document.querySelector("#hamburger-btn");
    const closeMenuBtn = document.querySelector("#close-menu-btn");
    let section = document.getElementById('section');

    // Toggle mobile menu on hamburger button click
    hamburgerBtn.addEventListener("click", () => header.classList.toggle("show-mobile-menu"));

    // Close mobile menu on close button click
    closeMenuBtn.addEventListener("click", () => hamburgerBtn.click());



})

// Mahsulot qo'shish uchun 
function plusmenu() {
    section.classList.toggle('activ');
    let nevbox = document.getElementById('plus');
    nevbox.classList.toggle('activ');
}

function rename() {
    section.classList.toggle('activ');
    let renamebox = document.getElementById('rename');
    renamebox.classList.toggle('activ');
}

function del() {
    section.classList.toggle('activ');
    let removebox = document.getElementById('remove');
    removebox.classList.toggle('activ');
}