function menuShow(){
    let menuMobile = document.querySelector('.mobile-menu');
    let iconImg = document.getElementById('menu-icon');
    if(menuMobile.classList.contains('open')){
        menuMobile.classList.remove('open');
        iconImg.src = '../static/imgs/menu_white_36dp.svg';
    } else{
        menuMobile.classList.add('open')
       iconImg.src = '../static/imgs/close_white_36dp.svg';
    }
}