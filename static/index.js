window.addEventListener('load', () => {
  const loader = document.querySelector(".loader");
  loader.classList.add('loader-hidden');
  
  loader.addEventListener('transitionend', () => {
      document.body.removeChild(loader);
  });
});

// window.addEventListener('load', () => {
//   const loader = document.querySelector(".loader");

//   setTimeout(() => {
//       loader.classList.add('loader-hidden');
//   }, 1000); // 1000ms = 1 second delay

//   loader.addEventListener('transitionend', () => {
//       document.body.removeChild(loader);
//   });
// });
