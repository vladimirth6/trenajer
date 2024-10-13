const history = [];
let position=350;
var zadCount=0;
var erCount=0;
// Случайное целое число в заданном диапазоне
//console.log(username1);
function getRandomNumber(min, max) {
  console.log('min ',min ,'  max ',max)
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Функция для формирования пары случайных чисел и вывода на страницу
function getQuestion() {
    var operators = level['operand'];
  var num1 = getRandomNumber(level['min1'],level['max1'] );
  var num2 = getRandomNumber(level['min2'],level['max2']);
  const f= operators[ Math.floor(Math.random() * operators.length)];
  switch (f) {
    case '*':
      ques=`${num1} * ${num2}`;
      res=num1*num2;
      break;
      
    case '/':
      res = num1;
      num1 = num1 * num2;
      ques=`${num1} / ${num2}`;
      break;
    case '+':
      ques=`${num1} + ${num2}`;
      res=num1+num2;
      break;
    case '-':
      res = num1;
      num1 = num1 + num2;
      ques=`${num1} - ${num2}`;
      break; 
  }

  zadCount++;
  return {ques,res };
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
    pos:position
  };
  
  history.push(historyItem);
  //console.log(history.length);
}
function getLastHistory(){
  return history[history.length-1];
}
function viewHistory(){

      var container = document.getElementById("myContainer");
    var resultText = "";

    for (var i = 0; i < history.length; i++) {
      //var equation = hist[i].num1;
      //var result = hist[i].isCorrect;

      var resultString = history[i].ques + " - " + (history[i].isCorrect ? "правильно" : "неправильно");

      var color = history[i].isCorrect ? "green":"red";
      var styledResultString = "<span style='color:" + color + "'>" + resultString + "</span>";

      resultText += styledResultString + "<br>";
    }

    container.innerHTML = resultText;
    //sendDataToServer(history)
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


