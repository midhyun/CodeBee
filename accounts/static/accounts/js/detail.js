const button1 = document.querySelector('#btn_1');
const button2 = document.querySelector('#btn_2');
      button2.addEventListener('click', function () {
        const tab1 = document.querySelector("#tab-1")
        const tab2 = document.querySelector("#tab-2")
        tab1.classList.add('deactive')
        tab2.classList.remove('deactive')
      });
      button1.addEventListener('click', function () {
        const tab1 = document.querySelector("#tab-1")
        const tab2 = document.querySelector("#tab-2")
        tab1.classList.remove('deactive')
        tab2.classList.add('deactive')
      });