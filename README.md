# EVE Corporation Announcer

## Простое приложение для пересылки писем между корпорациями, не состоящими в альянсе

### В приложении используются только стандартные библиотеки **Python**

##### Список команд:
1) **auth** - Первичная авторизация персонажа. Если персонаж уже авторизован, происходит обновление данных
2) **force_update** char_name - Ручное обновление токенов уже авторизованного персонажа (char_name необходимо заменить на никнейм персонажа. Пробелы в никнейме заменяются подчеркиванием)
3) **users_list** - Список всех авторизованных персонажей
4) **delete char_name** - Удаление авторизации указанного персонажа (char_name необходимо заменить на никнейм персонажа. Пробелы в никнейме заменяются подчеркиванием)
5) **delete all** - Удаление авторизации ВСЕХ персонажей

#####Установка, настройка и запуск приложения:
- Создание приложения EVE ESI

- Заполнение файла настроек (settings.py)

- Первичная авторизация персонажей

- Добавление приложения в CronTab

version 0.1.0
