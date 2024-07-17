   //Placeholder for functionality
//  document.addEventListener("DOMContentLoaded", function () {
//    const findOutButton = document.querySelector("button");
//    findOutButton.addEventListener("click", function () {
//      alert("Find out functionality coming soon!");
//    });
//  })
//  let menu = document.querySelector("#menu-button");
//  let navlinks = document.querySelector(".nav-links")
//  menu.onclick = () =>{
//    menu.classList.toggle("bi bi-x");
//    menu.classList.toggle("active");
 
//  window.onscroll = () =>{
//    menu.classList.remove("bi bi-x");
//    menu.classList.remove("active");
  }



document.addEventListener("DOMContentLoaded", function () {
  const findOutButton = document.querySelector("button");
  findOutButton.addEventListener("click", function () {
    alert("Find out functionality coming soon!");
  });

  const menuButton = document.querySelector("#menu-button");
  const navLinks = document.querySelector(".nav-links");

  menuButton.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    menuButton.classList.toggle("bi-x");
    menuButton.classList.toggle("bi-menu-button-wide-fill");
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) {
      navLinks.classList.remove("active");
      menuButton.classList.remove("bi-x");
      menuButton.classList.add("bi-menu-button-wide-fill");
    }
  });
});
