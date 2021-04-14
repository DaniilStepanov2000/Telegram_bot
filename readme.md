# Система цифровой обработки изображений
***
## Проект
***
Данная система предназначена для тех людей, которые хотят на мгновение погрузиться в 
мир цифровой обработки изображений и
попробовать своими руками проделать различные операции по изменению изображений. 
Созданная система позволяет выполнять различные математические операции над изображениями, 
что позволит в конечном итоге получить совершенно новое изображение.
***
## Технические детали
***
На данный момент проект содержит телеграм бота.<br>
__Стек, который используется для разработки:__ python3.7+, aiogram(для создания логики бота), numpy(для удобной работы с пикселями), scipy(для использования интерполяции), matplolib(для создания графиков), Pillow(для работы с изображениями).<br>
Весь список библиотек можно посмотреть в файле _requirements.txt_.
### Телеграм бот
В проекте используется телеграм бот для того, чтобы понять основные концепции по работе с телеграм ботами.<br>
Данный бот написан при помощи фреймворка aiogram для того, чтобы работать с Telegram Bot API.<br>
***
## Развертывание проекта
1. Перейти в директорию ```/bot```. 
2. Создать виртуальную среду. 
   ```
    python3 -m venv env_name
   ```
3. Активировать виртуальную среду, используя команду:<br>
   _Windows:_
   ``` 
   venv/Scripts/activate
   ```
   _Mac OS / Linux:_
   ``` 
   source mypython/bin/activate
   ```
   
4. Установить все пакеты, которые перечислены в файле _requirements.txt_. Для этого использовать команду:
   ```
   pip install -r requirements.txt
   ```
5. Создать файл _config.json_.
6. В файле _config.json_ создать переменные:<br>
__telegram_bot_token__ - содержит токен бота. Тип: __str__.<br>
__project_static_path__ - содержит путь к папке со статическими файлами. Тип: __str__
```json
{
  "telegram_bot_token": "token_bot",
  "project_static_path": "./data"
}
```
7. Запустить файл _main.py_, используя команду:
```
python main.py
```
***
## Пример работы проекта
__Пример:__ осуществим градационное преобразование над изображением и применим линейную интерполяцию к введенным пользователем точкам. 

__Шаг 1:__ Начинаем работу с ботом, для этого отправляем ему команду _/start_.<br><br>
![hN1TxgttZbU](https://user-images.githubusercontent.com/73431786/114615060-e62e4780-9cad-11eb-98eb-6cd38beb325b.jpg) <br><br>

__Шаг 2:__ Выбираем одну из предложенных команд и отправляем боту изображение.<br><br>
![A2KUKqTT3zI](https://user-images.githubusercontent.com/73431786/114615250-1ece2100-9cae-11eb-8dba-37f6af5368b7.jpg) <br><br>

__Шаг 3:__ Получаем гистограммы распределения цветов изображения (срднее, по каналу R, по каналу G и по каналу B) и выбираем операцию, которую хотим выполнить над изображением. <br><br>
![9QJFZPfVp4M](https://user-images.githubusercontent.com/73431786/114615501-74a2c900-9cae-11eb-82eb-9250a82efac6.jpg) <br><br>

__Шаг 4:__ Получаем график функции, которая применилась к изображению, изображение после преобразования и соответствующие гистограммы. <br><br>
![EqcMFrF4yCU](https://user-images.githubusercontent.com/73431786/114615889-e2e78b80-9cae-11eb-9930-16776ac4e4d4.jpg) <br><br>

__Шаг 5:__ Вводим координаты точек, по которым будет осуществляться линейная интерполяция. <br><br>
![RwUCSmzZZmI](https://user-images.githubusercontent.com/73431786/114616340-6608e180-9caf-11eb-9360-b8b0c9d1814b.jpg) <br><br>

__Шаг 6:__ Получаем график, на котором отмечены введенные точки, так же получаем график, на котором показана линейная интерполяция. <br><br>
![fyv6p4aloaY](https://user-images.githubusercontent.com/73431786/114616510-9cdef780-9caf-11eb-9282-c8ed0f13d7ed.jpg) <br><br>

__Щаг 7:__ Получаем преобразованное изображение на основе линейной интерполяции и соответствующие к ней гистограммы. <br><br>
![vqNQXzQi7LU](https://user-images.githubusercontent.com/73431786/114616732-e29bc000-9caf-11eb-939c-4570d4353996.jpg) <br><br>


