## Запуск локально
1. Заходим на [ngrok.com](https://ngrok.com/), регистрируемся, если ещё нет аккаунта.
2. После того, как залогинились, заходим на вкладку "Your Authtoken" и копируем оттуда токен в .env-файл в NGROK_AUTHTOKEN.
3. Далее переходим в "Cloud Edge / Domains" и нажимаем "+ New Domain".
4. Создаём свой постоянный домен и добавляем его в .env-файл в два места:
   * в NGROK_URL в формате "myurl.ngrok-free.app"
   * в BASE_WEBHOOK_URL в формате "https://myurl.ngrok-free.app".
6. Заполняем остальной .env-файл по инструкции из .env.example.
7. Запускаем проект из корневой директории (/backend) командой
  
   ```bash
   docker compose --env-file .env -f infra/docker-compose.local.yml up -d
   ```
