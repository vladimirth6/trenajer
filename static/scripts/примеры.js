let timerId;
var counters=0
var errores=0
const history = [];
var posit=350
var users=[]

// Случайное целое число в заданном диапазоне
function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Функция для формирования пары случайных чисел и вывода на страницу
function generateNumbers() {
    var operators = ["*", "/"];
  var num1 = getRandomNumber(2, 9);
  var num2 = getRandomNumber(2, 9);
  const f= operators[ Math.floor(Math.random() * operators.length)];
  if (f=="*"){
    ques=`${num1} * ${num2}`;
    res=num1*num2;
  }
  else{
    res = num1;
    num1 = num1 * num2;
    ques=`${num1} / ${num2}`;
  }
  return { num1, num2,ques,res };
}
function showQuestion(ques){
    counters=counters+1
    const question = document.getElementById('question');
    question.textContent = `${ques} = `;
    const zad = document.getElementById('zad');
    zad.textContent = `Завдання-${counters}`;
    const errr = document.getElementById('errr');
    errr.textContent = `Невірно-${errores}`;
}
// Функция для проверки ответа пользователя
function checkAnswer(userAnswer, res) {
  
  if (userAnswer === res) {
    return true;
  } else {
    return false;
  }
}

// Функция для обновления истории ответов
function updateHistory(userAnswer, qwes,res, isCorrect) {
  const historyItem = {
    ques: ques,
    res: res,
    userAnswer: userAnswer,
    isCorrect: isCorrect,
    pos:posit
  };
  
  history.push(historyItem);
  //console.log(history.length);
}
function viewHistory(hist){

      var container = document.getElementById("myContainer");
    var resultText = "";

    for (var i = 0; i < hist.length; i++) {
      //var equation = hist[i].num1;
      //var result = hist[i].isCorrect;

      var resultString = hist[i].ques + " - " + (hist[i].isCorrect ? "правильно" : "неправильно");

      var color = hist[i].isCorrect ? "green":"red";
      var styledResultString = "<span style='color:" + color + "'>" + resultString + "</span>";

      resultText += styledResultString + "<br>";
    }

    container.innerHTML = resultText;
    sendDataToServer(history)
}

// Функция для показа правильного ответа
function showCorrectAnswer(ques, res) {
  //показываем "Понял"
  const nextQuestionBtn=document.getElementById('next-question-btn');
  nextQuestionBtn.classList.remove('hidden'); 
  nextQuestionBtn.focus();
  //скриваем форму
  const form = document.getElementById('answer-form');
  form.classList.add('hidden');
  
  const correctAnswerDiv=document.getElementById('correct-answer');
  correctAnswerDiv.innerHTML=`<span style="color: red;">${ques} = ${res}</span>`; 
  errores=errores+1
  
}

function createImageCopies(users) {
  var container = document.querySelector('.container');
  var image2 = document.querySelector('.image2');
  // Обновляем свойства объекта image2
  if (users.length > 0) {
    image2.title = users[0][0];
    image2.style.top = users[0][1] + "px";
    }

  // Создаем копии объекта image2 для каждого элемента в списке users
  for (var i = 1; i < users.length; i++) {
    var name = users[i][0];
    var posit = users[i][1];

    // Создаем новый объект img
    var img = document.createElement('img');
    img.className = 'image image2';
    img.src = image2.src;
    img.width = image2.width;
    img.height = image2.height;
    img.style.top = posit + "px";
    img.style.left = i*20 + "px";
    img.title = name;

    // Добавляем новый объект img в контейнер
    container.appendChild(img);
    //container.insertBefore(img, container.firstChild);
  }
}

//полет рекеты
function raketa(posit){
    //var name =document.getElementById('username').value
    //var image2 = document.querySelector('.image2');
    //var randomTop=posit;
    //image2.style.top = randomTop + "px";
    //image2.title=name;
    createImageCopies(users)
    console.log(users)
    if (posit>400){//проигрыш
        endSession('/loser');
    }
    if (posit<70){//выигрыш
        endSession('/winer')
    }
}



function endSession(sost){
    window.location.href = sost;
}
//Отправка текущего состояния на сервер, и получение от него инструкций
function sendDataToServer(dataArray) {
  // Создаем новый объект XMLHttpRequest
  const xhr = new XMLHttpRequest();

  // Устанавливаем метод и URL для отправки запроса
  xhr.open('POST', '/ajax', true);

  // Устанавливаем заголовок Content-Type для указания типа данных
  xhr.setRequestHeader('Content-Type', 'application/json');

  // Обработчик события на изменение состояния запроса
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // Запрос успешно выполнен
      const response = JSON.parse(xhr.responseText);
      users = response.users;
      const message = response.message;
      //console.log(xhr.responseText);
      console.log(users.length)
      console.log(users)
    }
  };

  // Преобразуем массив данных в JSON-строку
  const jsonData = JSON.stringify(dataArray);

  // Отправляем запрос на сервер с данными
  xhr.send(jsonData);
}


// Функция для запуска таймера
function startTimer() {
  timerId = setTimeout(function() {
    // Ваш код выполнения действий после истечения таймера
    posit=posit+10
    raketa(posit)
    showCorrectAnswer(currentNumbers.ques, currentNumbers.res);
    updateHistory(0, currentNumbers.ques, currentNumbers.res, currentNumbers.isCorrect);
    currentNumbers=generateNumbers();
  document.getElementById('answer-input').value = ''; // Очистка поля ввода
  showQuestion(currentNumbers.ques)
    viewHistory(history)
    //sendDataToServer(history)
  }, 10000); // 10 секунд
}
  
// Инициализация

//const form = document.getElementById('answer-form');
//form.classList.remove('hidden');
// Сохраняем идентификатор таймера


const form = document.getElementById('answer-form');
const nextQuestionBtn=document.getElementById('next-question-btn');
var currentNumbers=generateNumbers();
showQuestion(ques)
startTimer(); // Запуск нового таймера
//обработчик конопки "понял"

nextQuestionBtn.addEventListener('click',function(){
    const correctAnswerDiv=document.getElementById('correct-answer');
    //скрівае "понял"
    correctAnswerDiv.innerHTML=''    
    nextQuestionBtn.classList.add('hidden')
    //и показіваем основную форму
    const form = document.getElementById('answer-form');
    form.classList.remove('hidden');
    document.getElementById('answer-input').focus();
    clearTimeout(timerId); // Обнуление текущего таймера
    startTimer(); // Запуск нового таймера
  });
  

  


form.addEventListener('submit', function(event) {
  event.preventDefault();
  const userAnswer = parseInt(document.getElementById('answer-input').value);
  const isCorrect = checkAnswer(userAnswer, currentNumbers.res);
  updateHistory(userAnswer, ques, res, isCorrect);
    if (!isCorrect) {
    // Неправильный ответ, показываем правильный ответ
    showCorrectAnswer(currentNumbers.ques, currentNumbers.res);
    posit=posit+10
  }
  else {
    posit=posit-10
  }
  
  raketa(posit)
  currentNumbers=generateNumbers();
  document.getElementById('answer-input').value = ''; // Очистка поля ввода
  showQuestion(currentNumbers.ques)
  viewHistory(history)
  
  clearTimeout(timerId); // Обнуление текущего таймера
  startTimer(); // Запуск нового таймера
  
});

history.pushState(null, null, document.URL);
window.addEventListener('popstate', function(event) {
  history.pushState(null, null, document.URL);
});

            
            
            
