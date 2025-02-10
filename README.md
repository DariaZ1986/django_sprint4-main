Доработка проекта "Блогикум".
Было создано:
- админ-зона для управления сайтом;
- база данных с публикациями;
- публикации в категории;
- публикации подробно;
- публикации на главной странице;
- добавление комментариев;
- добавление публикаций;
- регистрация пользователя;

В админ зоне суперпользователь может:
- добавить автора;
- снять с публикации\добавить в публикацию пост;
- снять с публикации\добавить в публикацию категорию;
- добавить\удалить автора

Пользователи теперь могут сами регистрироваться в проекте. Главную страницу могут видеть все.
Пользвателю доступно:
- создать пост
- создать комментарий
- по желанию прикрепить картинку к посту


Суперпользователь:
логин: admin
пароль: admin

в данном проекте выбраны такие имя пользователя и пароль для облегчения проверки и отладки, в дальнейшем необходимо создать более сложный логин\пароль.

для запуска проекта необходимо выполнить следующие действия:

скачать архив с проектом на свой пк
установить зависимосчти из файла requirements.py
находясь в папке проекта (Django_sprint4-main), запустить терминал (Git Bash) и выполнить команду "pip install Django==3.2.16"
перейти в папку blogicum
выполнить комунду "python manage.py migrate"
выполнить команду в терминале "python manage.py runserver"


