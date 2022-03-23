function genererNuages(number) {
    for(var i = 0; i < number; i ++){
      var xMax = window.innerWidth||document.documentElement.clientWidth||document.getElementsByTagName('body')[0].clientWidth;
      var yMax = (window.innerHeight||document.documentElement.clientHeight||document.getElementsByTagName('body')[0].clientHeight) / 1.5;
      var coordX = Math.floor((Math.random() * xMax) + 1);
      var coordY = Math.floor((Math.random() * yMax) + 1);
      var delay = (Math.floor((Math.random() * 10) + 1));
      var anim = i % 2 == 0 ? "move_d" : "move_g";
      window.nuages.innerHTML += '<div style="z-index: 999; animation: '+anim+' '+(delay * 10)+ 's '+(delay / 10)+'s alternate infinite; left: '+coordX+'px; top: '+coordY+'px;" class="nuage"></div>'
    }
  }
  
  var isDay = true;
  
  var dayOk = '[ Day ] - Night';
  var dayKo = 'Day - [ Night ]';
  
  window.toggleDarkMode.innerHTML = dayOk;
  
  function suppressionNuages() {
    window.nuages.innerHTML = "";
  }
  
  function createNuages() {
    genererNuages(10);
  }
  
  function onResize() {
    createNuages();
  };
  var doit;
  doit = setTimeout(onResize, 400);
  
  window.addEventListener("resize", function(){
    suppressionNuages();
    clearTimeout(doit);
    doit = setTimeout(onResize, 400);
  });
  
  function setDay() {
    window.ciel.classList.remove('night');
    window.soleil.classList.remove('night');
    window.herbe.classList.remove('night');
    window.main.classList.remove('night');
  }
  
  function setNight() {
    window.ciel.classList.add('night');
    window.soleil.classList.add('night');
    window.herbe.classList.add('night');
    window.main.classList.add('night');
  }
  
  window.toggleDarkMode.addEventListener('click', function (event) {
    if(isDay) {
      isDay = false;
      window.toggleDarkMode.innerHTML = dayKo;
      setNight();
    }else{
      isDay = true;
      window.toggleDarkMode.innerHTML = dayOk;
      setDay();
    }
  }, false);
  
  setInterval(function(){ 
    if(isDay) {
      isDay = false;
      window.toggleDarkMode.innerHTML = dayKo;
      setNight();
    }else{
      isDay = true;
      window.toggleDarkMode.innerHTML = dayOk;
      setDay();
    }
  }, 4000);
  
  