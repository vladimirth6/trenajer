const Time1=new Date();//получаем время начала игры
const imagesPath=["static/r121.png","static/luz.jpg","static/win.jpg","static/fon.jpg"];
const canvas=document.getElementById('myCanvas');//получаем канву
const div=document.getElementById('canvasContainer');
const ctx=canvas.getContext('2d');//перехватываем управление контентом канвы
const chatText=document.getElementById('forChat');
const chatCont=document.getElementById('forChatCont');
const fpsForce=40;
const maxFrameRate=25;
const zoomForse=10;
const stepPosition=10;
const posLoser=400;
const posWiner=70;
const zadanij=document.getElementById('zad');
const errors=document.getElementById('errr');
let img;
var Time2;
var gameOn=true;
var textFontSize=56;
var cx;
var cy;
var question;
var error='';
var frame=0;
var zoomSize=textFontSize;
var timeForAnswer=level['time'];
var outText;
var oldPosition=position;
var updateOf=true;
var raketFlag=false;
var stepF=false;
var stepPosRak=0;
var socket=io();
var viewResult=false;
var masivRaket;
var masivChat=[];
const input=document.createElement('input');//создаем елемент ввода ответа
input.style.position='absolute';//чтобы вставить куда годно
input.style.left='100px';//куданибудь ставим предварительно
input.style.top='120px';
input.style.background='transparent';//делаем прозрачным
input.style.border='none';//к херам рамку
input.style.color='green';//цвет и ширина рамки
input.style.width='60px';
input.style.fontFamily='Arial';//установим шрифт и размер
input.style.fontSize=textFontSize+'px';
input.style.outline='none';//убираем рамку при фокусе
input.value=''
canvas.parentElement.appendChild(input);

const button=document.createElement('input');//создаем кнопку 
button.type='button';
button.style.position='absolute';//чтобы вставить куда годно
button.style.left='100px';//куданибудь ставим предварительно
button.style.top='120px';
button.value='Закiнчити';

const button1=document.createElement('input');//создаем кнопку 
button1.type='button';
button1.style.position='absolute';//чтобы вставить куда годно
button1.style.left='100px';//куданибудь ставим предварительно
button1.style.top='120px';
button1.value='Грати ще!';

function endSession(sost){
    
    socket.on('disconnect',function(){
      console.log('отключено к серверу');
    });
    window.location.href = sost;
}
  function updateCanvasSize(){
    canvas.width=div.offsetWidth;
    canvas.height=div.offsetHeight;
    cx=canvas.width;
    cy=canvas.height;
    console.log('cx= ',cx);
    console.log('cy= ',cy);
  }
  //window.addEventListener('load',updateCanvasSize);// установим размер при загрузке страницы
  //window.addEventListener('resize',updateCanvasSize);//и при изменении ее размера
  function getCenter(text){
      const textX=ctx.measureText(text).width;//получаем геометрию текста задания, размер Х
      const X=Math.ceil((cx-textX)/2);//центруем надпись по центру канвы
      const Y=Math.ceil((cy-25)/2);//
      const I=X+textX+'px';//позиционируем поле ввода
      return {X,Y,I};
  }
  function compareAB(a,b){
    return Math.abs(a-b)<=0.5;
  }
  function showRakets(){
    //прорисовываем фон, стирая при этом все что было до того
    ctx.drawImage(img[3],0,0,cx,cy);
    ctx.font='10px Arial';
    ctx.fillStyle='brown';
    //console.log('ракет- ',masivRaket.length);
    for (let i=0; i<masivRaket.length; i++){    
      let m=masivRaket[i];
      //if (m['name']==='Bot-Vladimir'){
      //  console.log('ok');
      //}
      if (typeof(m['position'])==='string'){m['position']=parseInt(m['position']);};
      if (typeof(m['old'])==='string'){m['old']=parseInt(m['old']);};
      if (typeof(m['step'])==='string'){m['step']=parseInt(m['step']);};
      //console.log('ракета ',i,'-',m['name'],'>',m);
      if (m['flag']){
        //console.log('летим ',m['name']);
        if (m['step']===0){
          m['step']=parseFloat((m['position']-m['old'])/10);
        }
        m['old']=m['old']+m['step'];
        ctx.drawImage(img[0],m['x'],m['old'],32,64);
        ctx.fillText(m['name'],m['x'],m['old']);
        let q=m['old'];
        let p=m['position'];
        if (compareAB(q,p)){
          //console.log('достигли ',m['name']);
          m['old']=m['position'];
          m['flag']=false;
          m['step']=0;
          //let mm=JSON.parse(m);
          socket.emit('Obnova',{'name':m['name'],'data':JSON.stringify(m)});
        }
      }
      else{
        //console.log('статически ',m['name']);
        ctx.drawImage(img[0],m['x'],m['position'],32,64);
        ctx.fillText(m['name'],m['x'],m['position']);
        //socket.emit('Obnova',{'name':m['name'],'data':m})
        //m['step']=0;
      }
      //console.log('сохранимся ',m['name']);
      masivRaket[i]=m;
      raketFlag=false;//если хоть одна ракета еще не долетела, анимируем дальше
      raketFlag=raketFlag || m['flag'];      
     } 
    }
   
 //обмен с сервером  по таймеру для получения сведений о положении ракет соперников 
 function toServer(){
    servId=setTimeout(function(){
      socket.emit('Obmen','1');
    clearTimeout(servId);//перезапуск для нового кадра
    toServer();
 },1000);
 }    
 
 function chatTimer(){
    chatId=setTimeout(function(){
      socket.emit('readChat','1');
    clearTimeout(chatId);//перезапуск для нового кадра
    chatTimer();
 },1000);
 }    
 
 function viewScreen(){
    filmId=setTimeout(function(){
      //екран требует обновления по одной из причин
      //1- новое задание
      //2- обработка мультика ошибки по таймауту или по неверному ответу
      //3- перемещение ракет 
      if ((updateOf || raketFlag)&& masivRaket){
        showRakets();//начинаем из "дальних" позиций
        if (viewResult){
            console.log('Результат польоту')
           ctx.font='36px Arial';
           ctx.fillStyle='#55feef';
           var t;
           if (position<=posWiner){
            t='Результат польоту';
           }
           else{ 
              ctx.fillStyle='red';
              t='Хюстон у нас проблеми';
            }
           ctx.fillText(t,getCenter(t).X,30);
           t='Завданнь- '+zadCount;
           ctx.fillText(t,getCenter(t).X,80);
           t='Помилок- '+erCount;
           ctx.fillText(t,getCenter(t).X,130);
           let i=Math.floor((Time2-Time1)/1000);
           console.log(i);
           let m=Math.trunc(i/60);
           let c=i-(m*60);
           t='Затрачено- '+m+'хв.'+c+'с.';
           ctx.fillText(t,getCenter(t).X,180); 
           //updateOf=false;
           button.style.left='5px';//устанавливаем положение поля ввода
           button.style.top=(cy-25)+'px';
           canvas.parentElement.appendChild(button);//показываем поле ввода и передаем ему фокус
           button1.style.left='100px';//устанавливаем положение поля ввода
           button1.style.top=(cy-25)+'px';
           canvas.parentElement.appendChild(button1);//показываем поле ввода и передаем ему фокус
           //input.focus(); 
        }
        else{
          if(error!=='' && frame<=maxFrameRate){//тут покажем правильную анимацию
            const textX=ctx.measureText(error).width;
            ctx.font=zoomSize+'px Arial';
            ctx.fillStyle='red';
            const pos=getCenter(error);
            ctx.fillText(error,pos.X,pos.Y+zoomSize);  
            frame++;
            zoomSize+=zoomForse;   
          }
          else{
            ctx.font=textFontSize+'px Arial';//шрифт размер и цвет задания
            ctx.fillStyle='black';
            const pos=getCenter(outText);
            ctx.fillText(outText,pos.X,pos.Y+textFontSize);//выводим задание
            //ctx.fillStyle='green';
            //ctx.fillText(Cifer,pos.I,pos.Y+textFontSize);
            input.style.left=`${pos.I}`;//устанавливаем положение поля ввода
            input.style.top=`${pos.Y}px`;
            //canvas.parentElement.appendChild(input);//показываем поле ввода и передаем ему фокус
            //input.focus();
            updateOf=false;//говорим екранному таймеру что все уже обновили
          }
          if (frame>maxFrameRate){
            error='';
            frame=0;
            zoomSize=textFontSize;
            if (gameOn){
              clearTimeout(timerId); // Обнуление игрового таймера
              startTimer(timeForAnswer); // Запуск нового таймера
            }  
          }
       }
      }
      clearTimeout(filmId);//перезапуск для нового кадра
      viewScreen();
    },fpsForce);
 } 
  
  function resultat(){
    clearTimeout(timerId);
    gameOn=false;//остановим игровой таймер
    input.type='hidden';//и отключим поле ввода
    outText='';
    Time2=new Date();
    viewResult=true;
  }
  
  //вычисляем новую позицию ракеты, и все такое
  function updatePosition(f){
    let i;
    let m;
    //console.log('в Упдате имя ',username);
    for(i=0; i<masivRaket.length;i++){
      //console.log('ищем ',masivRaket[i]);
      if (masivRaket[i]['name']===username){
        m=masivRaket[i];
        //console.log('нашли ',m)      
      }
    }
    if(!f){  //падаем!
      m['position']=parseInt(m['position']+stepPosition);
      erCount++;
      m['flag']=true;
    }
    else{
      m['position']=parseInt(m['position']-stepPosition);
      m['flag']=true;//включаем анимацию полета ракеты!
    }
    position=m['position'];
    if (m['position'] >= posLoser || m['position'] <= posWiner){
        console.log('Цыкл игры окончен');
        if (m['position']<=posWiner){
          m['position']=-65;
          m['flag']=true;
        }
        
        resultat();
      }
    masivRaket[i]=m;//обновим для себя
    console.log('m -',m);
    //let mm=JSON.parse(m);
    socket.emit('Obnova',{'name':username,'data':JSON.stringify(m)});
    zadanij.textContent = `Завдання-${zadCount}`;
    errors.textContent = `Невірно-${erCount}`;    
  }
  
  // Функция для запуска таймера таймаута ответа
  function startTimer(delay) {
    timerId = setTimeout(function() {
      error=question.ques+'='+question.res;//
      frame=0;
      updateHistory('timeout', question.ques, question.res, false);
      question=getQuestion();
      outText=question.ques+'=';//готовим задание
      input.value='';
      console.log(outText);
      updateOf=true;//обновим екран
      viewHistory();
      socket.emit('toBase',getLastHistory());
      updatePosition(false);
      clearTimeout(timerId); // Обнуление игрового таймера
      if (gameOn){
        startTimer(timeForAnswer); // переЗапуск нового таймера 
      }
      //console.log('таймер завершен');
    }, delay*1000); // 10 секунд
  }
  function loadImages(imagesPath){
    return new Promise((resolve,reject)=>{
    const images=[];
    let count=0;
    imagesPath.forEach((url,index)=>{
      const img=new Image();
      img.onload=()=>{
        images[index]=img;
        count++;
        if (count===imagesPath.length){
          resolve(images);
        }
      };
      img.onerreor=(error)=>{
        reject(error);
      };
      img.src=url;
    });
   });    
  }
function gameBegin(){
  socket.emit('First','1');
  chatTimer();
  updateCanvasSize();
  question=getQuestion();
  outText=question.ques+'=';//готовим задание
  updateOf=true;
  viewScreen(); //запускаем екран!
  startTimer(timeForAnswer);
  toServer();
  zadanij.textContent = `Завдання-${zadCount}`;
  errors.textContent = `Невірно-${erCount}`;
}  
button1.addEventListener('click',function(event){
  endSession('/newGame');
});
button.addEventListener('click',function(event){
  endSession('/endSesion');  
});

/*
document.addEventListener('keydown', function(event){
  if (event.key>='0' && event.key<='9'){
    Cifer+=event.key;
    outText=outText+Cifer;
    console.log('Cifer ',Cifer)
    updateOf=true;
  }
  if (event.key==='Backspace'){
    Cifer=Cifer.slice(0,-1);
    event.preventDefault();
  }
});*/
chatText.addEventListener('keypress',function(event){
  if(event.key==='Enter' && event.shiftKey){
    const cv=this.value;
    const ss=this.selectionStart;
    this.value=cv.substring(0,ss)+'\n'+cv.substring(this.selectionEnd);
    this.selectionStart=this.selectionEnd=ss+1;
    event.preventDefault(); 
    
    
  }else if (event.key==='Enter'){
    event.preventDefault();
    socket.emit('toChat',{'name':username,'text':chatText.value,'time':''})
    chatText.value='';
  }
});
input.addEventListener('keypress', function(event){
  if (event.key==='Enter'){
    //console.log('из канвы');
    const value=input.value;
    console.log(`введено ${value}`)
      if (value!==question.res+''){//НЕ верный ответ
          error=outText+question.res;//подготовка показа верного ответа
          frame=0;
          updatePosition(false);
          updateHistory(value, question.ques, question.res, false);
          //console.log('нев ',outText);
      }
      else{//правильный ответ
          updatePosition(true);
          updateHistory(value, question.ques, question.res, true);
          //console.log('вер ',outText);
      }
      question=getQuestion();
      outText=question.ques+'=';//готовим задание
      //console.log('new ',outText);
      input.value='';
      updateOf=true;//обновим екран
      //console.log('покажем историю');
      viewHistory();
      socket.emit('toBase',getLastHistory());
      clearTimeout(timerId); // Обнуление игрового таймера
      startTimer(timeForAnswer); // Запуск нового таймера
    }
  });
  
  
input.addEventListener('focus',function(){//переключаем виртуальные клавы в только цыфры
  input.setAttribute("inputmode","numeric");
  });
canvas.addEventListener('click',function(){
  input.focus();
});
socket.on('connect',function(){//создаем сокет соединение
  console.log('подключено к серверу');
  });
  
//получение от сервера списка всех учасников и их ракет  
socket.on('response',function(data){
    masivRaket=JSON.parse(data);
    raketFlag=true;
  });
socket.on('getChat',function(chatBufer){
  //chatCont;
  var t='';
  chatCont.innerHTML='';
  if(chatBufer){
    for( let i=0; i<chatBufer.length;i++){
      const zg=document.createElement('span');
      zg.innerHTML=chatBufer[i]['name']+':';
      zg.style.fontFamily='Arial';
      zg.style.fontSize='10px';
      if (chatBufer[i]['name']==='Система'){
        zg.style.color='red';
      } else{
        for(let i=0;i<masivRaket.length;i++){
          if(masivRaket[i]['name']===username){
            zg.style.color=masivRaket[i]['color'];
          }
        }
      }
      
      t=chatBufer[i]['text'].replace(/\n/g,'<br>');
      const ne=document.createElement('span');
      ne.innerHTML="("+chatBufer[i]['time']+")<br>"+t+"<br>";
      ne.style.fontFamily='Arial';
      ne.style.fontSize='10px';
      ne.style.color='gray';
      ne.style.padding='10px';
      //t="<span style='color:" + "#4f4f4f" + "'>"+chatBufer[i]+"</span>";
      //i=innerHTML=t;
       chatCont.appendChild(zg);
      chatCont.appendChild(ne);
    }
  } 
});
 

loadImages(imagesPath)
  .then((images)=>{
    img=images;
    //console.log(img);
    gameBegin();
  })
  .catch((error)=>{
    console.error(error);
  });

