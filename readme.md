# Тестовое задание Блог

### Использованные технологии
 * Django 4.2
 * Django Rest Framework
 * Django templates
 * Docker

### Инструкция по установке и запуску
Для запуска нужно ввести следующую команду находясь в директории проекта
```shell
docker compose up --build
```
После завершения сборки образа и его запуска приложение будет доступно по адресу ``127.0.0.1:8000``
При переходе будет открыта страница со списком пользователей

## Основные запросы

### Пользователи (Users)

#### Получение списка пользователей (User List)

- Метод: GET
- URL: http://127.0.0.1:8000/api/users/list/

#### Регистрация нового пользователя (Sign up)

- Метод: POST
- URL: http://127.0.0.1:8000/api/users/signup/
- Тело запроса (JSON):
  ```json
  {
    "email": "alla3@alla.com",
    "name": "Alla3",
    "password": "AllaAlla200000"
  }
  ```

#### Вход пользователя (Login)

- Метод: POST
- URL: http://127.0.0.1:8000/api/users/login/
- Тело запроса (JSON):
  ```json
  {
    "username": "alla3@alla.com",
    "password": "AllaAlla200000"
  }
  ```

### Посты (Posts)

#### Создание нового поста (Create post)

- Метод: POST
- URL: http://127.0.0.1:8000/api/posts/
- Тело запроса (JSON):
  ```json
  {
    "title": "Post 675",
    "body": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
  }
  ```

#### Получение списка постов (Get posts)

- Метод: GET
- URL: http://127.0.0.1:8000/api/posts/user/<int:user_pk>/
- Заголовки: отсутствуют

#### Удаление поста (Delete post)

- Метод: DELETE
- URL: http://127.0.0.1:8000/api/posts/5/
- Заголовки:
  ```
  Authorization: Token 84932a15dd58f408cfdff4d328b4d4029d2a89be
  ```
  (вместо `84932a15dd58f408cfdff4d328b4d4029d2a89be` необходимо указать токен авторизации)

## Замечания

- Для выполнения некоторых запросов, требуется предварительная авторизация с помощью токена указываемого в заголовках.
- Вместо `127.0.0.1:8000` следует указать соответствующий адрес хоста, где развернуто приложение.
- Передаваемые данные в запросах указаны в формате JSON.
- Данные для запросов могут быть изменены в соответствии с требованиями приложения.
