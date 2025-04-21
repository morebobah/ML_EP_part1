Приложение обертка для модели emelnov/ocr-captcha-v4-mailru.
emelnov/ocr-captcha-v4-mailru — это дообученная версия microsoft/trocr-base-printed (или anuashok/ocr-captcha-v3, если применимо), предназначенная для распознавания текста на CAPTCHA-изображениях. Она была обучена на датасете из 1,000 CAPTCHA-изображений с платформы Mail.ru и достигла 98% точности на этом тестовом наборе.

Для запуска приложения docker должен быть установлен и запущен.
Порядок установки приложения.
1. Создайте каталог для размещения приложения. Например, projecti
2. Используя командную строку Вашей оболочки перейдите в созданный каталог. Например, cd projecti
3. Скачайте приложение с репозитория. Используйте команду git clone https://github.com/morebobah/ML_EP_part1.git
4. Создайте файл для переменных окружения в каталоге app по формату ниже. Например, используя команду:
    cat <<EOF >>.env
    SECRET_KEY=gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt
    ALGORITHM=HS256
    POSTGRES_USER=pguser
    POSTGRES_PASSWORD=pgpassword
    POSTGRES_DB=mydb
    DB_HOST=database
    DB_PORT=5432
    DB_NAME=mydb
    DB_USER=pguser
    DB_PASSWORD=pgpassword
    RABBITMQ_DEFAULT_USER=rbbmq
    RABBITMQ_DEFAULT_PASSWORD=rbbmqpwd
    DATABASE_URL=postgres://user:password@database:5432/mydb
    RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    COOKIE_NAME=users_access_token
    EOF
5. Скопируйте, или создайте симлинк, файла .env в папке mlworker. Например, можно использовать команды:
    cp app/.env mlworker/.env
    или
    ln app/.env mlworker/.env
6. Соберите образ. Используйте команду docker-compose build
7. Запустите приложение. Используйте команду docker-compose up
8. Дождитесь пока все необходимые службы будут запущены.
9. Доступ к web интерфейсу приложения по ссылке http:\\127.0.0.1
10. При запуске приложения создаются тестовый пользователь User@Test.ru с паролем testpwd.
    И администратор по умолчанию admin@test.ru с паролем testadminpwd.
    При необходимости вы можете создать своих пользователей на странице http:\\127.0.0.1\registration
    И сделать их админстраторами на странице административных функций используя для входа в систему администратора по умолчанию.


